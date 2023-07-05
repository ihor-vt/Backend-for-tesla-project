import cloudinary

from django.db import models
from django.utils.html import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    parent_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Головна категорія",
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категорія",
    )
    name = models.CharField(max_length=200, verbose_name="Назва")
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    product_code = models.CharField(max_length=12, null=True, verbose_name="Код товару")
    model_car = models.CharField(max_length=200, verbose_name="Модель авто")
    description = models.TextField(blank=True, verbose_name="Опис")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ціна основна"
    )
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Ціна зі знижкою",
    )
    available = models.BooleanField(default=True, verbose_name="Наявність")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Час обновлення")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE, verbose_name="Товар"
    )
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name="Зображення")

    def __str__(self) -> str:
        return str(self.image)

    def delete(self, *args, **kwargs):
        if self.image:
            cloudinary.uploader.destroy(self.image.public_id)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Зображення товару"
        verbose_name_plural = "Зображення товарів"


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    token = models.CharField(max_length=255, unique=True, verbose_name="Токен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сервіс"
        verbose_name_plural = "Сервіси"
