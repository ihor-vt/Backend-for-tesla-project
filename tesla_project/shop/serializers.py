from rest_framework import serializers

from .models import Category, Product, Comment, MainPage, Contact


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", "category", "name", "slug", "image", "model_car", "price"
            ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class MainPageSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta:
        model = MainPage
        fields = ["id", "image", "video"]

    def get_video(self, obj):
        if obj.video:
            return obj.video.url
        return None


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "mobile_phone", "product"]
