from django.urls import path,include
from . import views

urlpatterns = [


    path('me/', views.GetUser.as_view()),
    path('get_user/<int:pk>', views.GetUserByID.as_view()),
    path('get_user_feedback', views.GetUserFeedbacks.as_view()),
    path('update/', views.UserUpdate.as_view()),
    path('add_feedback/', views.UserAddFeedback.as_view()),
    path('sendSMS/', views.sendSMS.as_view()),
    path('getUserEmailbyPhone/', views.getUserEmailbyPhone.as_view()),
]
