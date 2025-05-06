from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.db import models
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.contrib.auth.models import User

class Vacancy(models.Model):
    full_name = models.CharField("ФИО", max_length=150)
    phone_number = models.CharField("Телефон", max_length=20)
    about = models.TextField("О себе")

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=150)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, null=True,related_name="products")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField("Скидка %", default=0)
    image = models.ImageField("Изображение", upload_to="products/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} — {self.total_price} тг"

    @property
    def total_price(self):
        return self.price - self.price * self.discount/100

    def add_to_cart(request, product_id):
        product = get_object_or_404(Product, id=product_id)

        # Получаем текущую корзину или создаём новую
        cart = request.session.get('cart', [])

        # Добавляем товар
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),  # сериализуем Decimal
        })

        request.session['cart'] = cart  # сохраняем в сессии
        return redirect('cart')  # или куда нужно


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user_name = models.CharField("Имя пользователя", max_length=150)
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} → {self.product.name}"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('cat',)
    search_fields = ('name',)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.user or self.session_key})"

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.total_price
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
