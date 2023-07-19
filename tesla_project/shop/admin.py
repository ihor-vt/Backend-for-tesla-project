from django.contrib import admin, messages
from django.utils.html import mark_safe
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

from .models import Category, Product, Service, Comment, MainPage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "token", "created_by", "updated_by"]
    readonly_fields = ["token", "created_by", "updated_by"]
    actions = ["generate_new_token"]

    def save_model(self, request, obj, form, change):
        if not obj.token:
            token = get_random_string(length=32)
            obj.token = make_password(token)

        if not obj.id:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)

    def generate_new_token(self, request, queryset):
        for service in queryset:
            token = get_random_string(length=32)
            service.token = make_password(token)
            service.save()

    generate_new_token.short_description = "Генерація нового токену"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_by", "updated_by"]
    readonly_fields = ["created_by", "updated_by"]
    search_fields = ["name"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "display_image",
        "category",
        "model_car",
        "price",
        "available",
        "main_page",
        "created_by",
        "updated_by",
        "created",
        "updated",
        ]

    readonly_fields = [
        "created_by",
        "updated_by"
        ]

    list_display_links = [
        "name",
        "display_image",
        "category",
        "model_car",
        "price",
        "main_page",
        ]

    def display_image(self, obj):
        image = obj.image.url
        if image:
            return mark_safe(
                f'<img src="{image}" width="80" height="100"\
                    style="margin-right: 10px;" />'
            )
        return "-"

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}

    list_filter = [
        "category", "available", "model_car", "main_page"
        ]

    search_fields = [
        "name",
        "category__name",
        "model_car",
        "price",
        ]

    def get_queryset(self, request):
        """
        The get_queryset function is used to filter
        the objects displayed in the change list.
        It accepts a request object as its only
        parameter and returns a QuerySet of model instances.
        The default implementation simply returns
        self.model._default_manager.get_queryset().

        :param self: Represent the instance of the class
        :param request: Get the current request, which is
        used to determine whether or not the user is authenticated
        :return: A queryset of all model instances that can be edited by the
        :doc-author: Ihor Voitiuk
        """
        qs = super().get_queryset(request)
        return qs.order_by("-main_page")

    def changelist_view(self, request, extra_context=None):
        """
        The changelist_view function is a wrapper
        around the default changelist_view function.
        It adds a warning message to the admin interface
        if there are less than 3 products on the main page.

        :param self: Represent the instance of the class
        :param request: Access the current request
        :param extra_context: Add variables or objects to the template context
        :return: A response object
        :doc-author: Ihor Voitiuk
        """

        main_page_count = Product.objects.filter(main_page=True).count()
        if main_page_count < 3:
            messages.warning(
                request, "Важливо! Оберіть не менше 3-ох товарів для \
                    головної сторінки."
                )

        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["model", "author", "created_by", "updated_by"]
    readonly_fields = ["created_by", "updated_by"]
    list_filter = ["model", "author"]
    search_fields = ["model", "content", "author"]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = [
        "media_thumbnail",
        "available",
        "created_by",
        "updated_by",
        "created",
        "updated"
        ]

    readonly_fields = [
        "created_by",
        "updated_by"
        ]

    list_display_links = [
        "media_thumbnail",
        "available",
        "created",
        "updated",
        ]

    def media_thumbnail(self, obj):
        if obj.video:
            if obj.video.resource_type == 'video':
                return mark_safe(f'<video width="200" height="200" controls>\
                                <source src="{obj.video.url}" \
                                type="video/mp4"></video>')
        elif obj.image:
            return mark_safe(f'<img src="{obj.image.url}"\
                            width="200" height="200"\
                style="margin-right: 10px;" />')
        return "-"

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)

    media_thumbnail.allow_tags = True
    media_thumbnail.short_description = "Медіа"
