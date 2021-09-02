import json
import uuid

from django.http import HttpResponseRedirect

from order.models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import send_sms
from .serializers import *
from .models import *
from rest_framework import generics
from yandex_checkout import Configuration, Payment
from technique.serializers import TechniqueUnitSerializer
import settings
from django.core.mail import send_mail,EmailMessage


from django.core.mail import send_mail
from django.template.loader import render_to_string



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


class UserUpdateNotificationID(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(request.data)
        user.notification_id = request.data['token']
        user.save()
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
        phone = request.data.get('phone')
        result = send_sms(phone, 'Код подтверждения')
        return Response(result, status=200)



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
                "return_url": f'{settings.HOST}/profile/balance?pay_id={pay_id}'
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
            print(payment)
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
        print('request.query_params.get', self.request.query_params.get('user_id'))
        return PaymentObj.objects.filter(user=self.request.query_params.get('user_id')).order_by('-created_at')


class GetAllPaymentsTypes(generics.ListAPIView):
    queryset = PaymentType.objects.filter()
    serializer_class = PaymentsTypesSerializer


class SendLink(APIView):
    def post(self, request):
        #https://play.google.com/store/apps/details?id=ru.pandiga.app
        # text = ''
        # if request.data.get('device')=='android':
        text = 'https://play.google.com/store/apps/details?id=ru.pandiga.app'
        send_sms(request.data.get('phone'),'',text)
        print(request.data)
        return Response(status=200)


class BonusesToMoney(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        request.user.partner_balance -= amount
        request.user.balance += amount
        request.user.save()
        return Response( status=200)


class UserRecoverPassword(APIView):
    def post(self,request):
        user = None
        try:
            user = User.objects.get(phone=request.data['phone'])
        except:
            user = None
        if user:
            phone = request.data.get('phone')
            password = create_random_string(digits=True, num=8)

            user.set_password(password)
            user.save()

            send_sms(phone, 'Ваш новый пароль', password)

            return Response({'result': True, 'email': user.email}, status=200)
        else:
            return Response({'result': False}, status=200)

class SendTestMail(APIView):
    def post(self,request):
        print(request.FILES)

        title=''

        file = None
        msg = f'Имя :{request.data.get("name")}\n'\
              f'Телефон:{request.data.get("phone")}\n' \
              f'Email :{request.data.get("email")}\n' \
              f'Комментарий :{request.data.get("comment")}' \

        if request.data.get("type") == 'f':
            title= 'Форма с сайта'
        else:
            title = 'Резюме с сайта'

        if request.FILES.get('file'):
            file = request.FILES.get('file')
        mail = EmailMessage(title, msg, 'info@pandiga.ru', ('dimon.skiborg@gmail.com','Malkon.zakaz@yandex.ru'))
        if file:
            mail.attach(file.name, file.read(), file.content_type)
        mail.send()
        return Response({'result':'ok'})


class IgorQuiz(APIView):
    def post(self,request):
        print(request.data)
        quiz = request.data.get('data')
        url = request.data.get('url')

        msg_html = render_to_string('igor_quiz.html', {
                                                    'quiz': quiz,
                                                    'url': url,
                                                    })
        send_mail('Заполнен квиз на сайте', None, 'info@pandiga.ru', ['dimon.skiborg@gmail.com'],
                  fail_silently=False, html_message=msg_html)

        return Response({'result': 'ok'})

class LQuiz(APIView):
    def post(self,request):
        print(request.data)

        quiz = request.data.get('data')


        msg_html = render_to_string('l_quiz.html', {'quiz': quiz,
                                                    })
        send_mail('Заполнен квиз на сайте', None, 'info@pandiga.ru', ['igor@astrapromo.ru'],
                  fail_silently=False, html_message=msg_html)

        return Response({'result':'ok'})

class LForm(APIView):
    def post(self,request):

        data = request.data
        phone = data.get("phone")
        msg_html = render_to_string('l_form.html', {
                                                    'phone': phone,
                                                    })
        send_mail('Заполнена форма на сайте', None, 'info@pandiga.ru', ['igor@astrapromo.ru'],
                  fail_silently=False, html_message=msg_html)
        return Response({'result':'ok'})


class LandingAstra(APIView):
    def post(self,request):
        msg = ''
        title = ''
        if request.data.get("type") == 'callBack':
            msg = f'Телефон :{request.data.get("phone")} | Имя :{request.data.get("name")}'
            title = 'Форма обратной связи (АСТРА)'
        if request.data.get("type") == 'quiz':
            msg = f'Телефон :{request.data.get("phone")} | Имя :{request.data.get("name")} | Ответы : {request.data.get("quiz")}'
            title = 'Форма квиза (АСТРА)'
        mail = EmailMessage(title, msg, 'info@pandiga.ru', ('dimon.skiborg@gmail.com','igor@astrapromo.ru'))

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
        mail = EmailMessage(title, msg, 'info@pandiga.ru', ('greshnik.im@gmail.com',))

        mail.send()
        return HttpResponseRedirect('/')


class LandingTest(APIView):
    def post(self,request):
        print(request.data)
        msg_html = render_to_string('test.html', {'name': request.data.get('name'),
                                                  'email': request.data.get('email'),
                                                  'phone': request.data.get('phone')}
                                    )
        send_mail('Заполнена форма', None, 'info@pandiga.ru', ('dimon.skiborg@gmail.com',),
                  fail_silently=False, html_message=msg_html)
        return Response(status=200)