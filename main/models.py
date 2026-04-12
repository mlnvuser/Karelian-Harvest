from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Категория')
    slug = models.SlugField(max_length=20, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Слаг')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    discount = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Скидка')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields = ['slug']),
            models.Index(fields = ['name']),
            models.Index(fields = ['-created']),
        ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:product_detail',
                       args=[self.slug])

    def sell_price(self):
        if self.discount:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price


class News(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Слаг')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, verbose_name='Изображение')
    video = models.FileField(
        upload_to='news/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Видео',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm'])],
        help_text='Поддерживаемые форматы: MP4, WebM'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    is_featured = models.BooleanField(default=False,verbose_name='Избранная новость')
    published = models.BooleanField(default=False,verbose_name='Опубликовано')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields = ['slug']),
            models.Index(fields = ['name']),
            models.Index(fields = ['-created']),
        ]
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.name

    def clean(self):
        """Запрещаем загружать одновременно и фото, и видео"""
        if self.image and self.video:
            raise ValidationError('Выберите либо изображение, либо видео — оба одновременно нельзя.')

    def get_media_type(self):
        """Возвращает тип медиа: 'image', 'video' или None"""
        if self.video:
            return 'video'
        if self.image:
            return 'image'
        return None

    def get_main_media(self):
        """Возвращает либо видео, либо изображение"""
        if self.video:
            return self.video
        return self.image

    @classmethod
    def get_featured(cls, limit=3):
        """Возвращает избранные новости, отсортированные по дате создания (новые сверху)"""
        return cls.objects.filter(published=True,is_featured=True).order_by('-created')[:limit]

class ContactInformation(models.Model):
    phone = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')
    email = models.EmailField(blank=True, verbose_name='Электронная почта'
    )
    telegram = models.URLField(max_length=200, blank=True, verbose_name='Telegram')
    instagram = models.URLField(max_length=200, blank=True, verbose_name='Instagram')
    vk = models.URLField(max_length=200, blank=True, verbose_name='ВКонтакте')
    address = models.TextField(blank=True, verbose_name='Адрес торговли')

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return 'Контактная информация сайта'

    @classmethod
    def get_info(cls):
        """Удобный метод для получения контактных данных"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj