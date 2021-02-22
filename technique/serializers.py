from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer

class TechniqueTypeSerializer(serializers.ModelSerializer):
    """Список типов"""
    orders_count=serializers.IntegerField(source='get_orders_count')
    class Meta:
        model = TechniqueType
        fields = [
            'id',
            'name',
            'name_lower',
            'name_slug',
            'orders_count'
        ]


class TechniqueCategorySerializer(serializers.ModelSerializer):
    """Список категорий"""
    types = TechniqueTypeSerializer(many=True, read_only=True)

    class Meta:
        model = TechniqueCategory
        fields = [
            'id',
            'name',
            'name_slug',
            'price',
            'image',
            'is_show_at_index',
            'types'
        ]


class TechniqueFilterValueSerializer(serializers.ModelSerializer):
    """Список значений фильтров"""
    class Meta:
        model = TechniqueFilterValue
        fields = ['id',
                  'filter',
                  'label',
                  'value',
                  'is_show_in_item_card'
                  ]


class TechniqueFilterSerializer(serializers.ModelSerializer):
    """Список фильтров"""
    values = TechniqueFilterValueSerializer(many=True, read_only=True)

    class Meta:
        model = TechniqueFilter
        fields = ['id',
                  'name_slug',
                  'type',
                  'placeholder',
                  'from_placeholder',
                  'to_placeholder',
                  'from_value',
                  'to_value',
                  'title',
                  'is_primary_filter',
                  'value',
                  'values']


class TechniqueUnitImageSerializer(serializers.ModelSerializer):
    """Список значений фильтров"""

    class Meta:
        model = TechniqueUnitImage
        fields = ['image','image_thumb',]
        depth = 1




class TechniqueUnitSerializer(serializers.ModelSerializer):
    """Список едениц техники"""
    type=TechniqueTypeSerializer(many=False)
    images = TechniqueUnitImageSerializer(many=True, read_only=True)
    city = serializers.SlugRelatedField(slug_field='city', read_only=True)
    class Meta:
        model = TechniqueUnit
        fields = [
                    'id',
                    'type',
                    'name',
                    'owner',
                    'name_slug',
                    'city',
                    'coords',
                  'min_rent_time',
            'is_moderated',
            'is_vip',
            'in_rent',
            'ad_price',
                  'rent_type',
                  'rent_price',
                  'rating',
                  'rate_times',
                  'is_free',
                  'images',
                  'year',
                  'is_active',
            'created_at'

                  ]


class TechniqueUnitFeedbackSerializer(serializers.ModelSerializer):
    """Список значений фильтров"""
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = TechniqueUnitFeedback
        fields = [
                  'created_at',
                  'text',
                    'author'
                  ]


class TechniqueUnitDetalSerializer(serializers.ModelSerializer):
    """Список едениц техники"""
    images = TechniqueUnitImageSerializer(many=True, read_only=True)
    unit_feedbacks = TechniqueUnitFeedbackSerializer(many=True, read_only=True)
    # filter = serializers.SlugRelatedField(slug_field='name',many=True, read_only=True)
    filter = TechniqueFilterSerializer(many=True, read_only=True)
    city = serializers.SlugRelatedField(slug_field='city',many=False, read_only=True)
    # filter_value = serializers.SlugRelatedField(slug_field='label',many=True, read_only=True)
    filter_value = TechniqueFilterValueSerializer(many=True, read_only=True)

    type = TechniqueTypeSerializer(many=False)
    owner = UserSerializer(many=False)
    class Meta:
        model = TechniqueUnit
        fields = [
            'id',
                  'type',
                  'owner',
                  'name',
            'city',
            'coords',
                  'name_slug',
                  'is_free',
                  'min_rent_time',
                  'rent_type',
                  'rent_price',
                  'rating',
                  'rate_times',
                  'description',
                  'images',
                  'unit_feedbacks',
                  'filter',
                  'filter_value',
            'year',
            'created_at'
                  ]