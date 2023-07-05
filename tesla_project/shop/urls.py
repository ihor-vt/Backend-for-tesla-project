from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"products", views.ProductViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.index, name="index"),
]
