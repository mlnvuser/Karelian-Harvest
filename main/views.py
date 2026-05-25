from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category, News, ContactInformation


def index(request):
    # Получаем максимум 3 избранные и опубликованные новости
    featured_news = News.get_featured(limit=3)

    # Теперь безопасно используем отрицательную индексацию
    first_news = featured_news[0] if featured_news else None
    last_news = featured_news[-1] if featured_news else None

    # Получаем ТОП-4 товара по скидке
    top_discount_products = Product.get_top_discounts(limit=4)

    # Получим обычные новости (не избранные)
    regular_news = News.get_regular_news(limit=2)

    return render(request, 'main/index.html', {
        'featured_news': featured_news,
        'first_news': first_news,
        'last_news': last_news,
        'top_discount_products': top_discount_products,
        'regular_news': regular_news,
    })

def products(request):

    # Получаем текущие параметры из URL (если есть)
    category_slug = request.GET.get('category', '')
    show_discount = request.GET.get('discount')  # 'on' если чекбокс выбран
    show_available = request.GET.get('available')  # 'on' если чекбокс выбран

    products = Product.objects.all()

    # 1. Фильтр по категориям
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # 2. Фильтр по скидкам
    if show_discount == 'on':
        products = products.filter(discount__gt=0)

    # 3. Фильтр по наличию
    if show_available == 'on':
        products = products.filter(available=True)

    # Передаём список категорий для dropdown
    categories = Category.objects.all().order_by('name')


    return render(request, 'main/products.html', {
        'products': list(products.order_by('name')),
        'categories': categories,
        'current_category': category_slug,  # Для подсветки активной категории
        'show_discount': show_discount,      # Для проверки состояния чекбокса
        'show_available': show_available,   # Для проверки состояния чекбокса
    })

def product_detail(request, slug):
    """Детальная страница продукта"""
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'main/product_detail.html', {'product': product})

def news(request):

    all_news = list(News.objects.filter(published=True, ).order_by('-is_pinned', '-created'))

    # Создаем объект пагинатора
    paginator = Paginator(all_news, 5)  # 5 новостей на страницу

    # Получаем номер страницы из URL (по умолчанию 1)
    page_number = request.GET.get('page', 1)

    try:
        news_page = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page не число, показываем первую страницу
        news_page = paginator.page(1)
    except EmptyPage:
        # Если page больше чем максимальное количество страниц, показываем последнюю
        news_page = paginator.page(paginator.num_pages)

    return render(request, 'main/news.html', {
        'news_page': news_page,
        'paginator': paginator,
        'is_first_page': page_number == 1,
        'is_last_page': page_number == paginator.num_pages,
    })

def news_detail(request, slug):
    """Детальная страница новости"""
    # Получаем новость по slug, только опубликованные
    news = get_object_or_404(News, slug=slug, published=True)

    # Соседние новости (для перелистывания)
    all_news = list(News.objects.filter(published=True).order_by('-created'))
    current_index = all_news.index(news) if news in all_news else 0

    prev_news = all_news[current_index + 1] if current_index < len(all_news) - 1 else None
    next_news = all_news[current_index - 1] if current_index > 0 else None

    return render(request, 'main/news_detail.html', {
        'news': news,
        'prev_news': prev_news,
        'next_news': next_news,
    })

def contacts(request):
    """Страница контактов"""
    contact_info = ContactInformation.get_info()
    return render(request, 'main/contacts_info.html', {'contact': contact_info})

def buy(request):
    """Страница оформления покупки через мессенджеры"""
    contact = ContactInformation.get_info()
    return render(request, 'main/buy.html', {'contact': contact})

def error_404(request, exception=None):
    """Обработчик ошибки 404"""

    return render(
        request,
        'main/404.html',
        {
            'request': request,  # Передать запрос для доступа к статику
        },
        status=404
    )