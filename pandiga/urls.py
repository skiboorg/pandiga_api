from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/technique/', include('technique.urls')),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/chat/', include('chat.urls')),
    path('api/v1/city/', include('city.urls')),
    path('api/v1/order/', include('order.urls')),
    path('api/v1/notification/', include('notification.urls')),


    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
