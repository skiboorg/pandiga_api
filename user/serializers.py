from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers
from djoser.conf import settings
from city.serializers import CitySerializer
from .models import UserFeedback

User = get_user_model()




class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='get_full_name',read_only=True,required=False)
    # avatar = serializers.CharField(source='get_avatar',read_only=True,required=False)
    avatar = serializers.SerializerMethodField()
    city = CitySerializer(required=False,read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'last_login',
            'avatar',
            'city',
            'first_name',
            'last_name',
            'phone',
            'email',
            'birthday',
            'fullname',
            'rating',
            'is_customer',
            'rate_times',
            'balance',
            'partner_balance',
            'subscribe_type',
            'orders_count',
            'rent_count',
            'date_joined'

                  ]

    def get_avatar(self, obj):
        print(obj)
        if obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url)
        else:
            return 'https://icon-icons.com/icons2/1097/PNG/96/1485477097-avatar_78580.png'

class UserFeedbackSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False,read_only=True)
    class Meta:
        model = UserFeedback
        fields = [
            'id',
            'text',
            'created_at',
            'author',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'phone',
            'first_name',
            'last_name',
            'city',
            'organization_name',
            'inn',
            'is_customer',
            'is_person',
            settings.LOGIN_FIELD,
            User._meta.pk.name,
            "password",

        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        print(validated_data)
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        print('validated_data',validated_data)
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user

