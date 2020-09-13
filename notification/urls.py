from django.urls import path
from . import views

urlpatterns = [


    path('get/', views.NotificationGet.as_view()),
    path('set_read/', views.NotificationSetRead.as_view()),




]
