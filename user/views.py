import json
import uuid
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
import settings

class UserAddFeedback(APIView):
    def post(self,request):
        data = request.data
        print(data['data']['rate_value'])
        UserFeedback.objects.create(user_id=data['to'],
                                    author=request.user,
                                    text=data['data']['rate_text'],
                                    value=data['data']['rate_value']
                                    )
        order = Order.objects.get(id=data['order'])
        order.worker_feedback = True
        order.save()
        return Response(status=201)

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
        messageSend = False
        # messageSend = True
        # try:
        #     message = client.messages.create(
        #         to=request.data['phone'],
        #         from_="test",
        #         body=f'PANDIGA. Код подтверждения: {sms_number}')
        #     print('message.sid=', message.sid)
        #     messageSend = True
        # except:
        #     messageSend = False
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


class GetRefferals(APIView):
    def get(self, request):
        pass

class NewPartner(APIView):
    def post(self, request):
        print(request.data)
        user=None
        try:
            user = User.objects.get(partner_code=request.data.get('code'))
        except:
            pass
        if user:
            try:
                master = Refferals.objects.get(master=user)
                master.slaves.add(request.user)
            except:
                master = Refferals.objects.create(master=user)
                master.slaves.add(request.user)

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


            all_partners = User.objects.filter(refferals__in=[paymentObj.user])
            print(all_partners)
            if all_partners.exists():
                for partner in all_partners:

                    partner.partner_balance += int(paymentObj.amount * 10 / 100)
                    partner.save()
                    RefferalMoney.objects.create(refferal=paymentObj.user,
                                                earned=int(paymentObj.amount * 10 / 100),
                                                action='Пополнение баланса')

        return Response(status=200)


class GetAllPayments(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    def get_queryset(self):
        return PaymentObj.objects.filter(user=self.request.query_params.get('user_id')).order_by('-created_at')


class GetAllPaymentsTypes(generics.ListAPIView):
    queryset = PaymentType.objects.filter()
    serializer_class = PaymentsTypesSerializer