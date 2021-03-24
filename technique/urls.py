from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.test,name='test'),
    path('categories/', views.TechniqueCategoryListView.as_view()),
    path('type/<str:name_slug>/', views.TechniqueTypeListView.as_view()),
    path('types/', views.TechniqueTypesListView.as_view()),
    path('filters/<str:name_slug>/', views.TechniqueFilterListView.as_view()),
    path('units', views.TechniqueUnitListView.as_view()),
    path('user/units', views.TechniqueUserUnitsListView.as_view()),
    path('unit/add/', views.TechniqueUnitAdd.as_view()),
    path('unit/edit/', views.TechniqueUnitEdit.as_view()),
    path('unit/delete/', views.TechniqueUnitDelete.as_view()),

    path('unit/<str:name_slug>', views.TechniqueUnitDetailView.as_view()),
    path('unit_edit/<str:uuid>', views.TechniqueUnitEditView.as_view()),
    path('add_feedback/', views.TechniqueUnitAddFeedback.as_view()),
    path('filter/', views.TechniqueFilter.as_view()),
    path('search/<str:query>', views.TechniqueSearch.as_view()),
    path('promote', views.TechniquePromote.as_view()),
    path('pay', views.TechniquePay.as_view()),
]
