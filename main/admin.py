from django.contrib import admin
from .models import Category, Product, News, ContactInformation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'category','name', 'slug','price',
        'available', 'created', 'updated', 'discount'
    ]
    list_filter = ['category','available', 'created', 'updated']
    list_editable = ['price', 'available', 'discount']
    prepopulated_fields = {'slug':('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'name','get_media_type_display', 'is_featured',
        'published', 'created', 'updated'
    ]
    list_filter = ['created', 'updated', 'published']
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
            'fields': ('is_featured', 'published')
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
    list_display = ['phone', 'email', 'telegram', 'instagram', 'vk']
    fieldsets = [
        ('Контактные данные', {
            'fields': ('phone', 'email', 'telegram', 'instagram', 'vk', 'address')
        }),
    ]

    def has_add_permission(self, request):
        """Запрещаем создавать больше одной записи"""
        if self.model.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        """Запрещаем удалять единственную запись"""
        return False

