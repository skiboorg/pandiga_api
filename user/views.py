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
from yookassa import Configuration, Payment
from technique.serializers import TechniqueUnitSerializer
import settings
from django.core.mail import send_mail,EmailMessage


from django.core.mail import send_mail
from django.template.loader import render_to_string

Configuration.account_id = settings.YA_SHOP
Configuration.secret_key = settings.YA_KEY

class UserAddFeedback(APIView):
    def post(self,request):
        data = request.data
        #print(data)
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
        #print(json.loads(request.data['userData']))
        data = json.loads(request.data['userData'])

        serializer = UserSerializer(user, data=json.loads(request.data['userData']))
        if serializer.is_valid():
            serializer.save()
            for f in request.FILES.getlist('avatar'):
                user.avatar = f
                user.save(force_update=True)
            if data.get('password'):
                print(data.get('password'))
                user.set_password(data.get('password'))
                user.save(force_update=True)
            return Response(status=200)
        else:
            #print(serializer.errors)
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
        result = send_sms(phone)
        return Response(result, status=200)



class UserNewPayment(APIView):
    def post(self,request):
        print(request.data)
        amount = request.data.get('amount')

        pay_id = uuid.uuid4()
        payment = Payment.create({
            "amount": {
                "value": amount,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f'{settings.HOST}/profile/balance'
            },
            "tax_system_code":2,

            "receipt": {
                "customer": {
                    "full_name": request.user.organization_name if request.user.organization_name else f'{request.user.first_name} {request.user.last_name}',
                    # "phone": str(request.user.phone).replace('+','').replace('(','').replace(')','').replace('-','')
                    "email": request.user.email
                },
                "items": [
                    {
                        "description": "Пополнение баланса",
                        "quantity": "1.00",
                        "amount": {
                            "value": amount,
                            "currency": "RUB"
                        },
                        "vat_code": "1",
                        "payment_mode": "full_payment",
                        "payment_subject": "service"
                    },
                ]
            },
            "capture": True,
            "description": f'Пополнение баланса пользователя ID {request.user.id}. {request.user.get_full_name()}'
        }, uuid.uuid4())

        response = json.loads(payment.json())

        if response.get('type') == 'error':
            result = {"success":False, "message": response.get('description')}
        else:

            PaymentObj.objects.create(user=request.user,
                                      pay_id=response.get('id'),
                                      pay_code=pay_id,
                                      amount=int(amount),
                                      status='Не оплачен')

            result = {"success": True, "message": response.get('confirmation')}

        return Response(result, status=200)

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
            user.partner_balance += 1000
            user.save(update_fields=['partner_balance'])
            request.user.used_partner_code = request.data.get('code')
            request.user.is_ref_code_entered = True
            request.user.save(update_fields=['is_ref_code_entered','used_partner_code'])

            return Response({'status':True}, status=200)
        else:
            return Response({'status':False},status=200)





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
        send_sms(request.data.get('phone'),'')
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
            password = create_random_string(digits=True, num=3)

            user.set_password(password)
            user.save()
            print('password',password)
            send_sms(phone, text=password)

            return Response({'result': True, 'email': user.email}, status=200)
        else:
            return Response({'result': False}, status=200)



class YooHook(APIView):
    def post(self, request):
        status = request.data['object']['status']
        if status == 'succeeded':
            payment = PaymentObj.objects.get(pay_id=request.data['object']['id'])
            if not payment.is_payed:
                payment.status = 'Оплачен'
                payment.is_payed = True
                payment.save()
                payment.user.balance += payment.amount
                payment.user.save(force_update=True)

                all_refferals = Refferal.objects.filter(refferal=payment.user)

                if all_refferals.exists():
                    for reffreal in all_refferals:
                        reffreal.master.partner_balance += int(payment.amount * 10 / 100)
                        reffreal.master.save()
                        reffreal.earned += int(payment.amount * 10 / 100)
                        reffreal.save()

        return Response(status=200)

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