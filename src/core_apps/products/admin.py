from django.contrib import admin

from core_apps.products.models import BrandName, Category, Product, ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "quantity", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)
    list_per_page = 10
    
@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("product", "image", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("product",)
    list_per_page = 10
    
@admin.register(Category)
class BrandNameAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)
    list_per_page = 10
    
@admin.register(BrandName)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)
    list_per_page = 10