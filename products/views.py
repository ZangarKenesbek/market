from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.timezone import now

from .forms import VacancyForm, CommentForm, ProductForm, CategoryForm
from .models import Comment, Cart, CartItem, Order, OrderItem
from .models import Product, Category
import pickle
import pandas as pd
from django.http import JsonResponse

def leave_request(request):
    if request.method == "POST":
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = VacancyForm()

    return render(request, 'ecommerce/vacancy_form.html', {'form': form})


def product_search(request):
    search_text = request.GET.get('search', '').strip()
    products = Product.objects.all()
    categories = Category.objects.all()
    prdctlst = []
    if search_text:
        for i in products:
            if i.name.lower().startswith(search_text.lower()):
                prdctlst.append(i)
    else:
        prdctlst.extend(products)

    return render(request, 'ecommerce/products_list.html', {
        'products': prdctlst,
        'categories': categories,
        'search_text': search_text,
        'search': True
    })



def products_list(request):
    category_filter = request.GET.get('category', '')
    products = Product.objects.all()

    if category_filter:
        products = products.filter(category__category=category_filter)

    categories = Category.objects.all()

    return render(request, 'ecommerce/products_list.html', {
        'products': products,
        'categories': categories,
        'category_filter': category_filter,
        'search': True
    })



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.comments.all()
    context = {
        "product": product,
        "reviews": reviews,
    }

    return render(request, "ecommerce/product_detail.html", context)


@login_required
def review_edit(request, pk, review_pk=None):
    product = get_object_or_404(Product, pk=pk)

    if review_pk:
        comment = get_object_or_404(Comment, pk=review_pk, product=product)
    else:
        comment = None

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.user_name = request.user.username
            new_comment.user_id = request.user.id
            new_comment.created_date = now()
            new_comment.save()
            return redirect('product_detail', pk=pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'ecommerce/review_form.html', {'form': form, 'product': product})

@permission_required('products.add_product', raise_exception=True)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


@permission_required('products.edit_product', raise_exception=True)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            product.delete()
            return redirect('home')

        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})



@permission_required('products.add_category', raise_exception=True)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print(product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # можно позже добавить сессию для анонимных
        return redirect('login')  # временно

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))
def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
        else:
            cart_items = []
    else:
        cart_items = []  # или перенаправить на login / сессию позже

    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        CartItem.objects.filter(cart=cart).delete()
    return redirect('cart')
@login_required
def increase_quantity(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, _ = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        except CartItem.DoesNotExist:
            pass
    return redirect('cart')
@login_required
def submit_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return redirect('cart')

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return redirect('cart')

    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()

    return render(request, 'ecommerce/thank_you.html')
def predict_sales(request, product_id):
    from products.models import OrderItem

    # загрузка модели
    with open('ml_model.pkl', 'rb') as f:
        model = pickle.load(f)

    today = pd.Timestamp.now().dayofyear

    # передаём два признака: [day, product_id]
    predicted_quantity = model.predict([[today, product_id]])[0]

    return JsonResponse({
        'product_id': product_id,
        'predicted_quantity': round(predicted_quantity),
    })


def predict_sales(request, product_id):
    import os
    from django.conf import settings

    model_path = os.path.join(settings.BASE_DIR, 'ml_models', f'model_{product_id}.pkl')

    if not os.path.exists(model_path):
        return JsonResponse({
            'product_id': product_id,
            'error': 'Model not found for this product'
        }, status=404)

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    today = pd.Timestamp.now().dayofyear

    try:
        predicted_quantity = model.predict([[today]])[0]
    except Exception as e:
        return JsonResponse({
            'product_id': product_id,
            'error': str(e)
        }, status=500)

    return JsonResponse({
        'product_id': product_id,
        'predicted_quantity': round(predicted_quantity)
    })


def get_order_data():
    data = []
    order_items = OrderItem.objects.select_related('order', 'product')
    for item in order_items:
        data.append({
            'product_id': item.product.id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'date': item.order.created_at.date()  # <-- используем дату из Order
        })
    return pd.DataFrame(data)
from django.http import JsonResponse
import os
import pickle
import pandas as pd
from django.conf import settings
from products.models import Product

def predict_all_sales(request):
    today = pd.Timestamp.now().dayofyear
    result = []

    for product in Product.objects.all():
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', f'model_{product.id}.pkl')

        if not os.path.exists(model_path):
            result.append({
                'product_id': product.id,
                'product_name': product.name,
                'error': 'Model not found'
            })
            continue

        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            predicted_quantity = model.predict([[today]])[0]
            result.append({
                'product_id': product.id,
                'product_name': product.name,
                'predicted_quantity': round(predicted_quantity)
            })
        except Exception as e:
            result.append({
                'product_id': product.id,
                'product_name': product.name,
                'error': str(e)
            })

    return JsonResponse(result, safe=False)
