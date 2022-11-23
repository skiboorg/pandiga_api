from rest_framework import exceptions, serializers
from user.serializers import UserSerializer
from technique.serializers import TechniqueTypeSerializer,TechniqueUnitSerializer
from .models import *
from city.serializers import CitySerializer
from technique.serializers import TechniqueFilterSerializer,TechniqueFilterValueSerializer

class OrderSerializer(serializers.ModelSerializer):
    filter = TechniqueFilterSerializer(many=True, read_only=True)
    filter_value = TechniqueFilterValueSerializer(many=True, read_only=True)
    type = TechniqueTypeSerializer(many=False)
    worker = UserSerializer(many=False)
    owner = UserSerializer(many=False)
    worker_unit = TechniqueUnitSerializer(many=False)
    apply_units = TechniqueUnitSerializer(many=True)
    decline_units = TechniqueUnitSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'name_slug',
            'comment',
            'rent_type',
            'rentDate',
            'rentDays',
            'rentTime',
            'rentHours',
            'rentKm',
            'created_at',
            'filter',
            'filter_value',
            'type',
            'worker',
            'worker_unit',
            'apply_units',
            'views',
            'update_at',
            'is_finished',
            'customer_feedback',
            'worker_feedback',
            'decline_units',
            'owner'
        ]


class OrdersSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    # filter = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    # filter_value = serializers.SlugRelatedField(slug_field='label', many=True, read_only=True)
    filter = TechniqueFilterSerializer(many=True, read_only=True)
    filter_value = TechniqueFilterValueSerializer(many=True, read_only=True)
    type = TechniqueTypeSerializer(many=False)
    worker = UserSerializer(many=False)
    worker_unit = TechniqueUnitSerializer(many=False)
    # apply_units = TechniqueUnitSerializer(many=True)

    city = CitySerializer(required=False, read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'owner',
            'name',
            'name_slug',
            'comment',
            'rent_type',
            'rentDate',
            'rentDays',
            'rentTime',
            'rentHours',
            'rentKm',
            'created_at',
            'filter',
            'filter_value',
            'type',
            'worker',
            'worker_unit',
            'apply_units',
            'views',
            'update_at',
            'is_finished',
            'coords',
            'city',
            'decline_units']

