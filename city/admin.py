from django.contrib import admin
from .models import *

class CityAdmin(admin.ModelAdmin):
    model=City
    list_display = ('order_num',
                    'city',
                    'region',
                    'coefficient',
                    )

    search_fields = ('city',)
admin.site.register(City,CityAdmin)
