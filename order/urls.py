from django.urls import path
from . import views

urlpatterns = [


    path('add/', views.OrderAdd.as_view()),
    path('delete/', views.OrderDelete.as_view()),
    path('close/', views.OrderClose.as_view()),
    path('apply/', views.OrderApply.as_view()),
    path('apply/accept/', views.OrderApplyAccept.as_view()),
    path('apply/decline/', views.OrderApplyDecline.as_view()),
    path('get_orders', views.OrdersGet.as_view()),
    path('get_user_orders/', views.UserOrdersGet.as_view()),
    path('get_user_orders_applyed/', views.UserOrdersApplyedGet.as_view()),
    path('get_user_orders_accepted/', views.UserOrdersAcceptedGet.as_view()),

    # path('get_order/<str:name_slug>', views.OrderGet.as_view()),
    path('get_order', views.OrderGet.as_view()),
    path('get_lk_order/<str:name_slug>', views.OrderLkGet.as_view()),
    path('subscribe', views.OrdersSubscribe.as_view()),



]
