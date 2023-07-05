from django.urls import reverse
from django.shortcuts import render
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from .authentication import ServiceOnlyAuthentication, ServiceOnlyAuthorizationSite


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [ServiceOnlyAuthentication]
    permission_classes = [ServiceOnlyAuthorizationSite]

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
            categories = product.category.products.all()
            category_serializer = CategorySerializer(
                categories, many=True, context={"request": request}
            )
            item["categories"] = category_serializer.data

            images = product.images.all()
            image_serializer = ProductImageSerializer(
                images, many=True, context={"request": request}
            )
            item["images"] = image_serializer.data

        return Response(data)

    @method_decorator(cache_page(60 * 2))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        data = serializer.data

        categories = instance.category.products.all()
        category_serializer = CategorySerializer(
            categories, many=True, context={"request": request}
        )
        data["categories"] = category_serializer.data

        images = instance.images.all()
        image_serializer = ProductImageSerializer(
            images, many=True, context={"request": request}
        )
        data["images"] = image_serializer.data

        return Response(data)


def index(request):
    api_url = reverse("api-root")
    admin_url = reverse("admin:index")

    context = {
        "api_url": api_url,
        "admin_url": admin_url,
    }

    return render(request, "shop/index.html", context)
