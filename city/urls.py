from django.urls import path,include
from . import views

urlpatterns = [


    path('create_city/', views.create_city),
    path('all/', views.GetAllCities.as_view()),
    path('search', views.SearchCity.as_view()),
    path('search_by_id', views.SearchCityID.as_view()),

]
