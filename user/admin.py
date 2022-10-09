from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(PaymentObj)
admin.site.register(PaymentType)
admin.site.register(Refferal)
admin.site.register(UserFeedback)
admin.site.register(Settings)
