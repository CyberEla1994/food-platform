from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Product, ProductCategory, Basket, Order, OrderItem, ProductRating
from .forms import OrderCreateForm

def product_detail(request, product_id):
    product = get_object_or_404(Product.objects.select_related('category'), id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
def index(request, category_id=None):
    categories = ProductCategory.objects.all()

    products = Product.objects.all().order_by('id')

    if category_id:
        products = products.filter(category__id=category_id)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/index.html', {
        'categories': categories,
        'page_obj': page_obj,
        'current_category': category_id
    })


def _get_session_basket(request):
    """Возвращает список позиций сессионной корзины для анонима."""
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    items = []
    for p in products:
        qty = cart[str(p.id)]
        items.append({'product': p, 'quantity': qty, 'sum': p.price * qty})
    return items


def _merge_session_basket(request, user):
    """Переносит сессионную корзину в БД после авторизации."""
    cart = request.session.pop('cart', {})
    for product_id, qty in cart.items():
        basket_item, created = Basket.objects.get_or_create(
            user=user, product_id=int(product_id),
        )
        if not created:
            basket_item.quantity += qty
            basket_item.save()
        else:
            basket_item.quantity = qty
            basket_item.save()


def basket_view(request):
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user).select_related('product')
        total_sum = sum(item.sum() for item in baskets)
        return render(request, 'products/basket.html', {
            'baskets': baskets,
            'total_sum': total_sum,
        })

    items = _get_session_basket(request)
    total_sum = sum(i['sum'] for i in items)
    return render(request, 'products/basket.html', {
        'session_baskets': items,
        'total_sum': total_sum,
    })


def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        basket_item, created = Basket.objects.get_or_create(
            user=request.user, product=product,
        )
        if not created:
            basket_item.quantity += 1
            basket_item.save()
    else:
        cart = request.session.get('cart', {})
        key = str(product.id)
        cart[key] = cart.get(key, 0) + 1
        request.session['cart'] = cart

    messages.success(request, "Товар добавлен в корзину")
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def set_product_rating(request, product_id):
    """Поставить оценку товару (1–5). POST value=1..5."""
    product = get_object_or_404(Product, id=product_id)
    value = request.POST.get("value")
    if value is None or value not in ("1", "2", "3", "4", "5"):
        return redirect(request.META.get("HTTP_REFERER", "index"))
    ProductRating.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={"value": int(value)},
    )
    ProductRating.update_product_rating(product)
    messages.success(request, "Спасибо за оценку!")
    return redirect(request.META.get("HTTP_REFERER", "index"))


@login_required
def increase_quantity(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id, user=request.user)
    basket.quantity += 1
    basket.save()
    return redirect('basket')


@login_required
def decrease_quantity(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id, user=request.user)
    if basket.quantity > 1:
        basket.quantity -= 1
        basket.save()
    else:
        basket.delete()
    return redirect('basket')


@login_required
def remove_from_basket(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id, user=request.user)
    basket.delete()
    return redirect('basket')


@login_required
def clear_basket(request):
    Basket.objects.filter(user=request.user).delete()
    messages.success(request, "Корзина очищена")
    return redirect("basket")


def session_increase(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        cart[key] += 1
        request.session['cart'] = cart
    return redirect('basket')


def session_decrease(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        if cart[key] > 1:
            cart[key] -= 1
        else:
            del cart[key]
        request.session['cart'] = cart
    return redirect('basket')


def session_remove(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    cart.pop(key, None)
    request.session['cart'] = cart
    return redirect('basket')


def session_clear(request):
    request.session.pop('cart', None)
    messages.success(request, "Корзина очищена")
    return redirect('basket')


@login_required
@transaction.atomic
def create_order(request):

    baskets = Basket.objects.filter(user=request.user)

    if not baskets.exists():
        return redirect('basket')

    if request.method == 'POST':

        form = OrderCreateForm(request.POST)

        if form.is_valid():
            total_sum = sum(item.sum() for item in baskets)
            card_raw = form.cleaned_data["card_number"].replace(" ", "").replace("-", "")
            card_last_four = card_raw[-4:] if len(card_raw) >= 4 else ""

            order = Order.objects.create(
                user=request.user,
                total_price=total_sum,
                delivery_address=form.cleaned_data["delivery_address"],
                comment=form.cleaned_data.get("comment", "") or "",
                card_last_four=card_last_four,
            )

            for item in baskets:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

            baskets.delete()

            messages.success(request, "Заказ успешно создан")

            return redirect('orders')

    else:
        form = OrderCreateForm()

    total_sum = sum(item.sum() for item in baskets)

    return render(request, "products/create_order.html", {
        "form": form,
        "baskets": baskets,
        "total_sum": total_sum,
    })


@login_required
def orders_view(request):

    orders = Order.objects.filter(user=request.user).order_by('-created')

    return render(request, 'products/orders.html', {
        'orders': orders
    })