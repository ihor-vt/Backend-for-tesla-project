from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

from .models import Category, Product, ProductImage, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "token")
    readonly_fields = ("token",)
    actions = ["generate_new_token"]

    def save_model(self, request, obj, form, change):
        if not obj.token:
            token = get_random_string(length=32)
            obj.token = make_password(token)
        super().save_model(request, obj, form, change)

    def generate_new_token(self, request, queryset):
        for service in queryset:
            token = get_random_string(length=32)
            service.token = make_password(token)
            service.save()

    generate_new_token.short_description = "Генерація нового токену"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_first_image",
        "product_code",
        "category",
        "price",
        "discounted_price",
        "available",
        "created",
        "updated",
    )
    list_display_links = ("name", "display_first_image", "product_code", "category")

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}

    def display_first_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return mark_safe(
                f'<img src="{first_image.image.url}" width="80" height="100" style="margin-right: 10px;" />'
            )
        return "-"

    display_first_image.short_description = "Перше зображення"

    list_filter = ("category", "available", "product_code")
    search_fields = (
        "name",
        "category__name",
        "product_code",
        "description",
        "price",
        "discounted_price",
    )
    inlines = [ProductImageInline]
