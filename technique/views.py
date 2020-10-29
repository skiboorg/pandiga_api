import json
from order.models import Order
from itertools import chain
from rest_framework import generics
from django.shortcuts import HttpResponse
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files import File as DjangoFile
from .models import *
from .serializers import *

class UnitsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links':{
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
            },
            'page_count':self.page.paginator.num_pages,
            'results':data
        })

class TechniqueUnitAddFeedback(APIView):
    def post(self, request):
        data = request.data
        print(data['data']['rate_value'])
        TechniqueUnitFeedback.objects.create(techniqueitem_id=data['to'],
                                    author=request.user,
                                    text=data['data']['rate_text'],
                                    value=data['data']['rate_value']
                                    )
        order = Order.objects.get(id=data['order'])
        order.customer_feedback = True
        order.save()
        return Response(status=201)

class TechniqueUnitAdd(APIView):
    def post(self,request):
        print(request.data)
        print(request.FILES)
        unit_data = json.loads(request.data['unit'])
        filters_data = json.loads(request.data['filters'])
        images_data = request.data['images']

        print(images_data)

        type = TechniqueType.objects.get(name_slug=unit_data['selectedType'])

        unit = TechniqueUnit.objects.create(type=type,
                                     owner=request.user,
                                     name=unit_data['name'],
                                     year=unit_data['year'],
                                     min_rent_time=unit_data['min_rent_time'],
                                     rent_type=unit_data['rent_type'],
                                     rent_price=unit_data['rent_price'],
                                     description=unit_data['description'],
                                            city_id=unit_data['city_id'],
                                            coords=unit_data['coords'],
        )

        for filter in filters_data:
            if filter['value'] != '':
                for v in filter['values']:
                    if v['value'] == filter['value']:
                        unit.filter_value.add(v['id'])
                unit.filter.add(filter['id'])

        for f in request.FILES.getlist('images'):
            TechniqueUnitImage.objects.create(techniqueitem=unit,image=f)
        for f in request.FILES.getlist('docs_images'):
            TechniqueUnitImageDoc.objects.create(techniqueitem=unit,image=f)
        return Response(status=201)



class TechniqueUnitListView(APIView):
    pagination_class = UnitsPagination

    def get(self,request):
        units = TechniqueUnit.objects.filter(type__name_slug=request.GET.get('type'),
                                             is_active=True).order_by('-is_vip')
        page = self.paginate_queryset(units)
        if page is not None:
            serializer = TechniqueUnitSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class TechniqueUserUnitsListView(generics.ListAPIView):
    """Вывод едениц техники юзера"""
    serializer_class = TechniqueUnitSerializer
    def get_queryset(self):
        return TechniqueUnit.objects.filter(owner=self.request.query_params.get('user_id'))

    # def get(self,request):
    #     techique_units = TechniqueUnit.objects.filter(owner=request.user)
    #     serializer = TechniqueUnitSerializer(techique_units,many=True)
    #     return Response(serializer.data)

# class TechniqueUnitDetailView(APIView):
#     """Вывод деталей еденицы техники по slug name"""
#     def get(self,request, name_slug):
#
#         try:
#             techique_unit = TechniqueUnit.objects.get(name_slug=name_slug)
#             serializer = TechniqueUnitDetalSerializer(techique_unit,many=False)
#             return Response(serializer.data)
#         except:
#             return Response(status=404)

class TechniqueUnitDetailView(generics.RetrieveAPIView):
    """Вывод деталей еденицы техники по slug name"""
    serializer_class = TechniqueUnitDetalSerializer
    lookup_field = 'name_slug'
    queryset = TechniqueUnit.objects.filter()



class TechniqueCategoryListView(generics.ListAPIView):
    """Вывод категории техники"""
    serializer_class = TechniqueCategorySerializer

    def get_queryset(self):
        return TechniqueCategory.objects.filter(is_active=True)



class TechniqueTypeListView(generics.RetrieveAPIView):
    """Вывод типа техники по slug name"""
    queryset = TechniqueType.objects.filter()
    lookup_field = 'name_slug'
    serializer_class = TechniqueTypeSerializer


class TechniqueTypesListView(generics.ListAPIView):
    """Вывод всех типов техники """
    queryset = TechniqueType.objects.filter()
    serializer_class = TechniqueTypeSerializer



class TechniqueFilterListView(APIView):
    def get(self, request, name_slug):
        techique_type= TechniqueType.objects.get(name_slug=name_slug)
        filters = techique_type.filters
        serializer = TechniqueFilterSerializer(filters, many=True)
        return Response(serializer.data,headers=None)


class TechniqueSearch(APIView):
    def get(self, request,query):
        f_a = TechniqueFilterValue.objects.all()
        for f in f_a:
            f.save()
        print(query)
        # filter_values = TechniqueFilterValue.objects.filter(label_lower__startswith=query.lower())
        # print(filter_values)
        # filters=[]
        # for filter_value in filter_values:
        #     filters.append(filter_value.filter)
        # print(filters)
        # types=TechniqueType.objects.filter(filters__in=filters)
        # print(types)
        # result=[]
        # for type in types:
        #     result.append({
        #         'id':type.id,
        #         'query':query.upper(),
        #         'type':type.name
        #     })

        filter_values = TechniqueFilterValue.objects.filter(label_lower__startswith=query.lower())
        print(filter_values)
        filters = []
        result = []
        for filter_value in filter_values:

            types = TechniqueType.objects.filter(filters=filter_value.filter)
            print(types)

            for type in types:
                result.append({
                    'type_id': type.id,
                    'type_name_slug': type.name_slug,
                    'type_name': type.name,
                    'filter_id': filter_value.filter.id,
                    'filter_value_id':filter_value.id,
                    'filter_value_label':filter_value.label.upper(),
                    'filter_value':filter_value.value,
                    'filter_name_slug':filter_value.filter.name_slug,

                })

        return Response(result,status=200)


class TechniqueFilter(APIView):
    pagination_class = UnitsPagination
    def post(self,request):
        request_unicode = request.body.decode('utf-8')
        request_body = json.loads(request_unicode)
        print(request_body)
        technique_type = request_body['technique_type']
        # первоначально отфильтрованные данные
        filtered_qs = []
        result_qs = []
        result = []
        # ключи-значения переданных фильтров
        all_filters_values = []
        order_type = 'created_at'
        if request_body['order_by']:
            order_type = request_body['order_by']
        for filter in request_body['primary_filter']:
            if filter['value'] != '':
                all_filters_values.append({
                    filter['name_slug']: filter['value']
                })
            key = filter['name_slug']
            value = filter['value']
            qs = TechniqueUnit.objects.filter(type__name_slug=technique_type,
                                              filter__name_slug__exact=key,
                                              filter_value__value__exact=value).distinct()
            filtered_qs.append(qs)

        print('filtered_qs',filtered_qs)

        for qs in filtered_qs:
            temp_qs = None
            for item in qs:
                print('item.get_filter_value()', item.get_filter_value())
                print('all_filters_values', all_filters_values)
                for subfilter in all_filters_values:
                    if subfilter not in item.get_filter_value():
                        print('remove',item)
                        qs = qs.exclude(id=item.id)
                        print('filter Qs', qs)

                # if item.get_filter_value() != all_filters_values:
                #     print('remove', item)
                #     qs = qs.exclude(id=item.id)
                #     print('filter Qs', qs)

            if request_body['city_id']:
                temp_qs = qs.filter(type__name_slug=technique_type,
                                    rent_price__gte=request_body['rent_price_from'],
                                    rent_price__lte=request_body['rent_price_to'],
                                    min_rent_time__gte=request_body['rent_time_from'],
                                    min_rent_time__lte=request_body['rent_time_to'],
                                    rent_type=request_body['rent_type'],
                                    city_id=request_body['city_id'],
                                    is_active=True).order_by('-is_vip').order_by(order_type)
            else:
                temp_qs = qs.filter(type__name_slug=technique_type,
                                    rent_price__gte=request_body['rent_price_from'],
                                    rent_price__lte=request_body['rent_price_to'],
                                    min_rent_time__gte=request_body['rent_time_from'],
                                    min_rent_time__lte=request_body['rent_time_to'],
                                    rent_type=request_body['rent_type'],
                                    is_active=True).order_by('-is_vip').order_by(order_type)
            result_qs.append(temp_qs)
        # проверка на дубли
        for single_qs in result_qs:
            for qs in single_qs:
                if not qs in result:
                    result.append(qs)
        # serializer = TechniqueUnitSerializer(result, many=True)

        if len(all_filters_values) == 0:
            if request_body['city_id']:
                result_vip = TechniqueUnit.objects.filter(type__name_slug=technique_type,
                                                      rent_price__gte=request_body['rent_price_from'],
                                                      rent_price__lte=request_body['rent_price_to'],
                                                      min_rent_time__gte=request_body['rent_time_from'],
                                                      min_rent_time__lte=request_body['rent_time_to'],
                                                      rent_type=request_body['rent_type'],
                                                          city_id=request_body['city_id'],
                                                          is_active=True,
                                                      is_vip=True).order_by('-promote_at')
                result_other = TechniqueUnit.objects.filter(type__name_slug=technique_type,
                                                          rent_price__gte=request_body['rent_price_from'],
                                                          rent_price__lte=request_body['rent_price_to'],
                                                          min_rent_time__gte=request_body['rent_time_from'],
                                                          min_rent_time__lte=request_body['rent_time_to'],
                                                          rent_type=request_body['rent_type'],
                                                            city_id=request_body['city_id'],
                                                            is_vip=False,
                                                          is_active=True).order_by('-promote_at')
            else:
                result_vip = TechniqueUnit.objects.filter(type__name_slug=technique_type,
                                                          rent_price__gte=request_body['rent_price_from'],
                                                          rent_price__lte=request_body['rent_price_to'],
                                                          min_rent_time__gte=request_body['rent_time_from'],
                                                          min_rent_time__lte=request_body['rent_time_to'],
                                                          rent_type=request_body['rent_type'],
                                                          is_active=True,
                                                          is_vip=True).order_by('-promote_at')
                result_other = TechniqueUnit.objects.filter(type__name_slug=technique_type,
                                                            rent_price__gte=request_body['rent_price_from'],
                                                            rent_price__lte=request_body['rent_price_to'],
                                                            min_rent_time__gte=request_body['rent_time_from'],
                                                            min_rent_time__lte=request_body['rent_time_to'],
                                                            rent_type=request_body['rent_type'],
                                                            is_vip=False,
                                                            is_active=True).order_by('-promote_at')



            result = list(chain(result_vip, result_other))

            # serializer = TechniqueUnitSerializer(result, many=True)

        page = self.paginate_queryset(result)
        if page is not None:
            serializer = TechniqueUnitSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        # return Response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)




def test(request):
    primary_filter = {
        'rent_type': '0',
        'rent_price_from':'100',
        'rent_price_to':'1000000',

    }
    filter = {
        'dlina-vil':'1',
        # 'vyisota-podema':'2',
        'tsvet':'black',
    }
    filtered_qs=[]
    result_qs = []
    qs = None
    result = ''

    for key in filter:
        value=filter[key]
        print(key,value)
        qs = TechniqueUnit.objects.filter(type=1,
                                          filter__name_slug__exact=key,
                                          filter_value__value__exact=value).distinct()
        print('qs1', qs)
        filtered_qs.append(qs)

    # Ищем по первичным фильтрам
    if len(primary_filter) > 0 and filtered_qs:
        for qs in filtered_qs:
            temp_qs=None
            temp_qs = qs.filter(type=1, rent_price__gte=primary_filter['rent_price_from'],
                                rent_price__lte=primary_filter['rent_price_to'],
                                rent_type=primary_filter['rent_type'],
                                is_active=True,
                                is_moderated=True)
            result_qs.append(temp_qs)
        print('result_list', result_qs)
    result = list(chain(*result_qs))

    return HttpResponse(result,status=200)
