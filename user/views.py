import json
import uuid

from django.http import HttpResponseRedirect

from order.models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from twilio.rest import Client
from .services import create_random_string
from .serializers import *
from .models import *
from rest_framework import generics
from yandex_checkout import Configuration, Payment
from technique.serializers import TechniqueUnitSerializer
import settings
from django.core.mail import send_mail,EmailMessage


class UserAddFeedback(APIView):
    def post(self,request):
        data = request.data
        print(data['data']['rate_value'])
        order = Order.objects.get(id=data['order'])
        UserFeedback.objects.create(user=order.owner,
                                    author=request.user,
                                    text=data['data']['rate_text'],
                                    value=data['data']['rate_value']
                                    )
        order.worker_feedback = True
        order.save()
        return Response(status=201)


class FavGet(generics.ListAPIView):
    serializer_class = TechniqueUnitSerializer

    def get_queryset(self):
        return self.request.user.favorites

class FavDel(APIView):
    def post(self,request,unit_id):
        request.user.favorites.remove(unit_id)
        return Response(status=200)


class FavAdd(APIView):
    def post(self,request,unit_id):
        print(unit_id)
        request.user.favorites.add(unit_id)
        return Response(status=200)


class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(json.loads(request.data['userData']))
        print(request.FILES)
        serializer = UserSerializer(user, data=json.loads(request.data['userData']))
        if serializer.is_valid():
            serializer.save()
            for f in request.FILES.getlist('avatar'):
                user.avatar = f
                user.save(force_update=True)
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=400)

class GetUserFeedbacks(generics.ListAPIView):
    serializer_class = UserFeedbackSerializer

    def get_queryset(self):
        queryset = UserFeedback.objects.filter(user=self.request.query_params.get('user_id'))
        return queryset

class GetUserByID(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter()

class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user
    # def get(self, request):
    #     user = request.user
    #     serializer = UserSerializer(user, many=False)
    #     return Response(serializer.data)

class getUserEmailbyPhone(APIView):
    def post(self,request):
        print(request.data)
        user = None
        try:
            user = User.objects.get(phone=request.data['phone'])
        except:
            user= None
        if user:
            return Response({'result': True, 'email': user.email},status=200)
        else:
            return Response({'result': False},status=200)


class sendSMS(APIView):
    def post(self,request):
        account_sid = settings.TWILLO_ACCOUNT_SID
        auth_token = settings.TWILLO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        sms_number = create_random_string(digits=True,num=4)
        # messageSend = False
        messageSend = True
        try:
            message = client.messages.create(
                to=request.data['phone'],
                from_="test",
                body=f'PANDIGA. Код подтверждения: {sms_number}')
            print('message.sid=', message.sid)
            messageSend = True
        except:
            messageSend = False
        if messageSend:
            return Response({'result': True, 'code': sms_number})
        else:
            return Response({'result': False, 'code': sms_number})

class UserNewPayment(APIView):
    def post(self,request):
        print(request.data)
        amount = request.data.get('amount')
        payment_type = request.data.get('pay_type')

        Configuration.account_id = settings.YA_SHOP_ID
        Configuration.secret_key = settings.YA_API
        pay_id = uuid.uuid4()
        payment = Payment.create({
            "amount": {
                "value": amount,
                "currency": "RUB"
            },
            "payment_method": {
                "type": payment_type,
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f'{settings.HOST}/lk/balance?pay_id={pay_id}'
            },
            "capture": True,
            "description": f'Пополнение баланса пользователя ID {request.user.id}. {request.user.get_full_name()}'
        }, pay_id)

        pt = PaymentType.objects.get(method=payment_type)
        PaymentObj.objects.create(user=request.user,
                               pay_id=payment.id,
                               pay_code=pay_id,
                               amount=int(amount),
                               type=pt,
                               status='Не оплачен')

        return Response(payment.confirmation.confirmation_url)


# class GetRefferalsMoney(generics.ListAPIView):
#     serializer_class = RefferalsMoneySerializer
#
#     def get_queryset(self):
#         return RefferalMoney.objects.filter(master=self.request.user)

class GetRefferals(generics.ListAPIView):
    serializer_class = RefferalsSerializer
    def get_queryset(self):
        return Refferal.objects.filter(master=self.request.user)

class NewPartner(APIView):
    def post(self, request):
        print(request.data)
        user=None
        refferal = None
        try:
            user = User.objects.get(partner_code=request.data.get('code'))
            print(user)
        except:
            pass

        try:
            refferal = Refferal.objects.get(master=user,refferal=request.user)
            print('refferal found')
        except:
            print('refferal not found')

        if not refferal and user:
            Refferal.objects.create(master=user, refferal=request.user)

            return Response({'status':True}, status=200)
        else:
            return Response({'status':False},status=200)


class UserCheckPayment(APIView):
    def post(self, request):
        print(request.data)
        pay_id = request.data.get('pay_id')
        Configuration.account_id = settings.YA_SHOP_ID
        Configuration.secret_key = settings.YA_API

        paymentObj = PaymentObj.objects.get(pay_code=pay_id)
        print(paymentObj)
        if not paymentObj.is_payed:
            payment = Payment.find_one(paymentObj.pay_id)
            if payment.status == 'succeeded':
                paymentObj.is_payed = True
                paymentObj.status = 'Оплачен'
                paymentObj.save()
                paymentObj.user.balance += paymentObj.amount
                paymentObj.user.save(force_update=True)


            all_refferals = Refferal.objects.filter(refferal=paymentObj.user)

            print(all_refferals)
            if all_refferals.exists():
                for reffreal in all_refferals:
                    print(reffreal.master)
                    reffreal.master.partner_balance += int(paymentObj.amount * 10 / 100)
                    reffreal.master.save()
                    reffreal.earned += int(paymentObj.amount * 10 / 100)
                    reffreal.save()


        return Response(status=200)


class GetAllPayments(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    def get_queryset(self):
        return PaymentObj.objects.filter(user=self.request.query_params.get('user_id')).order_by('-created_at')


class GetAllPaymentsTypes(generics.ListAPIView):
    queryset = PaymentType.objects.filter()
    serializer_class = PaymentsTypesSerializer


class UserRecoverPassword(APIView):
    def post(self,request):
        user = None
        try:
            user = User.objects.get(phone=request.data['phone'])
        except:
            user = None
        if user:
            account_sid = settings.TWILLO_ACCOUNT_SID
            auth_token = settings.TWILLO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            sms_number = create_random_string(digits=True, num=8)
            # messageSend = False
            messageSend = True
            try:
                message = client.messages.create(
                    to=request.data['phone'],
                    from_="test",
                    body=f'PANDIGA. Ваш новый пароль: {sms_number}')
                user.set_password(sms_number)
                user.save()

                messageSend = True
            except:
                messageSend = False
            return Response({'result': True, 'email': user.email}, status=200)
        else:
            return Response({'result': False}, status=200)

class SendTestMail(APIView):
    def post(self,request):
        print(request.data)
        msg = ''
        title = ''
        if request.data.get("type") == 'callBack':
            msg = f'Телефон :{request.data.get("phone")}'
            title = 'Форма обратной связи (кухни)'
        if request.data.get("type") == 'quiz':
            msg = f'Телефон :{request.data.get("phone")} | Ответы : {request.data.get("quiz")}'
            title = 'Форма квиза (кухни)'

        file = None
        if request.FILES.get('file'):
            file = request.FILES.get('file')
        mail = EmailMessage(title, msg, 'd@skib.org', ('d@skib.org',))
        if file:
            mail.attach(file.name, file.read(), file.content_type)
        mail.send()
        return Response({'result':'ok'})


class BflQuiz(APIView):
    def post(self,request):
        msg = ''
        title = ''
        if request.data.get("type") == 'callBack':
            msg = f'Телефон :{request.data.get("phone")}'
            title = 'Форма обратной связи (БФЛ)'
        if request.data.get("type") == 'quiz':
            msg = f'Телефон :{request.data.get("phone")} | Ответы : {request.data.get("quiz")}'
            title = 'Форма квиза (БФЛ)'
        mail = EmailMessage(title, msg, 'd@skib.org', ('d@skib.org',))

        mail.send()
        return Response({'result':'ok'})

class LandingMail(APIView):
    def post(self,request):
        print(request.data)
        title = 'Форма обратной связи '
        msg = f'Email :{request.data.get("email")} | Name :{request.data.get("name")} |' \
              f' Phone :{request.data.get("phone")} | Сompany :{request.data.get("company")} | ' \
              f'Manager :{request.data.get("manager")} | Budget :{request.data.get("budget")} |' \
              f'Message :{request.data.get("message")} '
        mail = EmailMessage(title, msg, 'd@skib.org', ('d@skib.org',))

        mail.send()
        return HttpResponseRedirect('/')