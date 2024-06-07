from django.urls import path
from . import views

app_name = 'priceChecker'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('viewAll/', views.viewAll, name='viewAll'),
    path('about/', views.about, name='about')
]