from django.urls import path,include
from . import views

urlpatterns = [


    path('get_chat', views.MessagesList.as_view()),
    path('all/', views.ChatsList.as_view()),
    path('add/<int:chat_id>', views.ChatAdd.as_view()),
    path('new_message/<int:owner_id>', views.ChatNewMessage.as_view()),
    # path('type/<str:name_slug>/', views.TechniqueTypeListView.as_view()),
    # path('filters/<str:name_slug>/', views.TechniqueFilterListView.as_view()),
    # path('units/<str:name_slug>/', views.TechniqueUnitListView.as_view()),
    # path('user/units/', views.TechniqueUserUnitsListView.as_view()),
    # path('unit/add/', views.TechniqueUnitAdd.as_view()),
    # path('unit/<str:name_slug>/', views.TechniqueUnitDetailView.as_view()),
    #
    # path('filter/', views.TechniqueFilter.as_view()),
]
