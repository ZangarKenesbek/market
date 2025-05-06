# serializers.py

from rest_framework import serializers
from .models import Vacancy, Category, Product, Comment


class VacancySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=20)
    about = serializers.CharField()

    def create(self, validated_data):
        return Vacancy.objects.create(**validated_data)


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    cat = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.IntegerField(default=0)
    image = serializers.ImageField(required=False, allow_null=True)

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.total_price

    def validate_discount(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Скидка должна быть от 0 до 100.")
        return value

    def validate_cat(self, value):
        if not Category.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Категория не найдена")
        return value

    def create(self, validated_data):
        category_id = validated_data.pop('cat')
        category = Category.objects.get(pk=category_id)
        return Product.objects.create(cat=category, **validated_data)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "cat": instance.cat_id,
            "price": str(instance.price),
            "discount": instance.discount,
            "image": instance.image.url if instance.image else None
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'product', 'user_name', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']
