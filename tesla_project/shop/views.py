from django.urls import reverse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Product, Comment, MainPage
from .serializers import CategorySerializer,\
    ProductSerializer, CommentSerializer, MainPageSerializer
from .authentication import ServiceOnlyAuthentication,\
    ServiceOnlyAuthorizationSite


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['get']

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['get']

    @method_decorator(cache_page(60 * 2))
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

    @method_decorator(cache_page(60 * 2))
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

    @method_decorator(cache_page(60 * 2))
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

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MainPageViewSet(viewsets.ModelViewSet):
    queryset = MainPage.objects.filter(available=True)
    serializer_class = MainPageSerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]
    http_method_names = ['get']

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            context={"request": request})
        data = serializer.data

        return Response(data)


def index(request):
    api_url = reverse("api-root")
    admin_url = reverse("admin:index")

    context = {
        "api_url": api_url,
        "admin_url": admin_url,
    }

    return render(request, "shop/index.html", context)
