from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('news/', views.news, name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('buy/', views.buy, name='buy'),
]