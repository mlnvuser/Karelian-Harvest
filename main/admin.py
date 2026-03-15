from django.contrib import admin
from .models import Category, Product, News

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
        'name','slug',
        'created', 'updated'
    ]
    list_filter = ['created', 'updated']
    prepopulated_fields = {'slug':('name',)}

