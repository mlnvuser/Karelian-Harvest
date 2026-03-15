from django.shortcuts import render, get_object_or_404
from .models import Product, Category, News


def index(request):
    return render(request, template_name='main/index.html')
