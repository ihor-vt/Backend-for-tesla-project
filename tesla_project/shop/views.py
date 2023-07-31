import logging

from datetime import datetime

from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Category, Product, Comment, MainPage, Contact
from .serializers import CategorySerializer,\
    ProductSerializer, CommentSerializer, \
    MainPageSerializer, ContactSerializer
from .authentication import ServiceOnlyAuthentication,\
    ServiceOnlyAuthorizationSite


logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['get']

    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['get']

    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        data = serializer.data

        for item in data:
            product_id = item["id"]
            product = Product.objects.get(pk=product_id)
            category = product.category
            category_serializer = CategorySerializer(
                category, context={"request": request}
            )
            item["category"] = category_serializer.data

        return Response(data)

    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            context={"request": request})
        data = serializer.data

        category = instance.category
        category_serializer = CategorySerializer(
            category, context={"request": request}
        )
        data["category"] = category_serializer.data

        return Response(data)


class ProductMainPageViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(available=True, main_page=True)
    serializer_class = ProductSerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['get']

    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        data = serializer.data

        for item in data:
            product_id = item["id"]
            product = Product.objects.get(pk=product_id)
            category = product.category
            category_serializer = CategorySerializer(
                category, context={"request": request}
            )
            item["category"] = category_serializer.data

        return Response(data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['get']

    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MainPageViewSet(viewsets.ModelViewSet):
    queryset = MainPage.objects.filter(available=True)
    serializer_class = MainPageSerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['get']

    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            context={"request": request})
        data = serializer.data

        return Response(data)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.none()
    serializer_class = ContactSerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        product_id = data.get('product', None)
        product_message = "-"

        if product_id is not None:
            try:
                product = Product.objects.get(pk=product_id)
                product_message = f"{product.name}, Модель авто: {product.model_car if product.model_car else '-'}, Ціна: {product.price}"
            except Product.DoesNotExist:
                return Response(
                    {'error': 'Invalid product_id'},
                    status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Send email
        time_now = datetime.now()
        formatted_datetime = time_now.strftime("%d.%m.%Y - %H:%M")
        subject = "Форму з сайту заповнив клієнт"
        first_name = serializer.data.get('first_name', "")
        last_name = serializer.data.get('last_name', "")
        mobile_phone = serializer.data.get('mobile_phone', "")
        message = f"Дата і час: {formatted_datetime},\nІм'я: {first_name}\nПрізвище: {last_name}\nТелефон: {mobile_phone}\nТовар: {product_message}"

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError as e:
            logger.error(f"Invalid header found: {e}")
        except Exception as e:
            logger.error(f">>> Failed to send email: {e}")

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)


def index(request):
    api_url = reverse("api-root")
    admin_url = reverse("admin:index")

    context = {
        "api_url": api_url,
        "admin_url": admin_url,
    }

    return render(request, "shop/index.html", context)
