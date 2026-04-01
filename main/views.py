from django.shortcuts import render, get_object_or_404
from .models import Product, Category, News


def index(request):
    return render(request, template_name='main/index.html')

def products(request):
    return render(request, template_name='main/products.html')

def news(request):
    return render(request, template_name='main/products.html')
