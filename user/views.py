import json
from order.models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from twilio.rest import Client
from .services import create_random_string
from .serializers import *
from .models import *
from rest_framework import generics
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
                user.save()
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=400)

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
            return Response(status=404)


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
