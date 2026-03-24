from decimal import Decimal

from .models import Basket, Product


def cart_total(request):
    """Сумма и количество позиций корзины (БД или сессия)."""
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user).select_related('product')
        total = sum(item.sum() for item in baskets)
        count = sum(item.quantity for item in baskets)
        return {"cart_total": total, "cart_count": count}

    cart = request.session.get('cart', {})
    if cart:
        products = {str(p.id): p for p in Product.objects.filter(id__in=cart.keys())}
        total = sum(products[pid].price * qty for pid, qty in cart.items() if pid in products)
        count = sum(cart.values())
        return {"cart_total": total, "cart_count": count}

    return {"cart_total": Decimal("0"), "cart_count": 0}
