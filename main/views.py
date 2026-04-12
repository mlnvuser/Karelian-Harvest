from django.shortcuts import render, get_object_or_404
from .models import Product, Category, News


def index(request):
    # Получаем максимум 3 избранные и опубликованные новости
    featured_news = News.get_featured(limit=3)

    # Теперь безопасно используем отрицательную индексацию
    first_news = featured_news[0] if featured_news else None
    last_news = featured_news[-1] if featured_news else None

    return render(request, 'main/index.html', {
        'featured_news': featured_news,
        'first_news': first_news,
        'last_news': last_news,
    })

def products(request):
    return render(request, template_name='main/products.html')

def news(request):
    return render(request, template_name='main/products.html')

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, published=True)
    return render(request, 'main/news_detail.html', {'news': news})
