from django.contrib import admin
from .models import Category, Product, News, ContactInformation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'category','name','price', 'discount',
        'available', 'created', 'updated',
    ]
    list_filter = ['category','available', 'created', 'updated']
    list_editable = ['price', 'available', 'discount']
    prepopulated_fields = {'slug':('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'name','get_media_type_display', 'is_featured', 'is_pinned',
        'published', 'created', 'updated'
    ]
    list_filter = ['created', 'updated', 'published', 'is_pinned', 'is_featured']
    prepopulated_fields = {'slug':('name',)}
    fieldsets = [
        ('Основная информация', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Медиафайл', {
            'fields': ('image', 'video'),
            'description': 'Загружайте <b>либо изображение, либо видео</b>. Одновременно оба загружать нельзя.'
        }),
        ('Статус', {
            'fields': ('is_featured', 'is_pinned', 'published')
        }),
    ]

    def get_media_type_display(self, obj):
        if obj.video:
            return '🎥 Видео'
        if obj.image:
            return '🖼️ Фото'
        return '—'

    get_media_type_display.short_description = 'Медиа'

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    # --- 1. Отображение столбцов в списке записей ---
    list_display = [
        'phone',  # Телефон
        'email',  # Почта
        'telegram',  # Телеграм
        'instagram',  # Инстаграм
        'vk',  # Вконтакте
        'has_yandex_widget',  # 🆕 Специальный статус наличия виджета
    ]

    # --- 2. Группировка полей в форме редактирования ---
    fieldsets = [
        ('Основные контакты', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Социальные сети', {
            'fields': ('telegram', 'instagram', 'vk', 'messenger_max')
        }),
        ('Текстовая информация', {
            'fields': ('info', 'yandex_widget')  # 🆕 Добавили сюда виджет
            # Внимание: yandex_widget лучше размещать ближе к концу формы
            # Так как он может быть длинным кодом
        }),
    ]

    # --- 3. Метод-свойство для отображения статуса виджета ---
    @admin.display(description='Есть виджет Яндекс')  # Заголовок колонки
    def has_yandex_widget(self, obj):  # Метод принимает объект модели
        return bool(obj.yandex_widget)  # Возвращает True или False

    has_yandex_widget.boolean = True  # Показывает галочку ✅/❌ вместо текста

    # --- 4. Управление доступом (Защита от дубликатов) ---
    def has_add_permission(self, request):
        """Разрешаем создать новую запись только если её ещё нет"""
        if self.model.objects.exists():  # Если база уже содержит хоть одну запись...
            return False  # ...запрещаем добавлять новую
        return True  # Иначе разрешаем

    def has_delete_permission(self, request, obj=None):
        """Запрещаем удалять единственную запись контактов"""
        return False  # Всегда возвращаем False

