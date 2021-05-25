from django.urls import path,include
from . import views

urlpatterns = [


    path('me/', views.GetUser.as_view()),
    path('fav_add/<int:unit_id>', views.FavAdd.as_view()),
    path('fav_del/<int:unit_id>', views.FavDel.as_view()),
    path('fav_get/', views.FavGet.as_view()),
    path('get_user/<int:pk>', views.GetUserByID.as_view()),
    path('get_user_feedback', views.GetUserFeedbacks.as_view()),
    path('update/', views.UserUpdate.as_view()),
    path('add_feedback/', views.UserAddFeedback.as_view()),
    path('sendSMS/', views.sendSMS.as_view()),
    path('getUserEmailbyPhone/', views.getUserEmailbyPhone.as_view()),
    path('new_payment/', views.UserNewPayment.as_view()),
    path('all_payment_types/', views.GetAllPaymentsTypes.as_view()),
    path('all_payments', views.GetAllPayments.as_view()),
    path('new_partner/', views.NewPartner.as_view()),
    path('get_refferals/', views.GetRefferals.as_view()),
    # path('get_refferals_money/', views.GetRefferalsMoney.as_view()),
    path('check_payment/', views.UserCheckPayment.as_view()),
    path('recover_password', views.UserRecoverPassword.as_view()),
    path('bonuses_to_money', views.BonusesToMoney.as_view()),


    path('mail/send_test', views.SendTestMail.as_view()),
    path('mail/l_quiz', views.LQuiz.as_view()),
    path('mail/l_form', views.LForm.as_view()),
    path('mail/land', views.LandingMail.as_view()),
    path('mail/astra', views.LandingAstra.as_view()),
    path('mail/test', views.LandingTest.as_view()),
]
