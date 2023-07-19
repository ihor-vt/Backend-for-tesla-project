from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"products/main", views.ProductMainPageViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"comments", views.CommentViewSet)
router.register(r"medias", views.MainPageViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.index, name="index"),
]
