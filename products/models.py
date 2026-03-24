from django.db import models
from django.conf import settings
from django.db.models import Avg


class ProductCategory(models.Model):
    name = models.CharField("Название", max_length=256)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "категория товара"
        verbose_name_plural = "категории товаров"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=256)
    image = models.ImageField("Изображение", upload_to='products/')
    description = models.TextField("Описание")
    short_description = models.CharField("Краткое описание", max_length=64)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество")
    rating = models.DecimalField(
        "Рейтинг",
        max_digits=2,
        decimal_places=1,
        default=0,
        help_text="От 0 до 5",
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name

    def get_star_display(self):
        """Возвращает список из 5 элементов: 1 — полная звезда, 0.5 — половина, 0 — пустая."""
        r = float(self.rating)
        r = max(0, min(5, r))
        result = []
        for i in range(1, 6):
            if r >= i:
                result.append(1)
            elif r >= i - 0.5:
                result.append(0.5)
            else:
                result.append(0)
        return result


class ProductRating(models.Model):
    """Оценка товара пользователем (1–5). Один пользователь — одна оценка на товар."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_ratings",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    value = models.PositiveSmallIntegerField(
        "Оценка",
        choices=[(i, str(i)) for i in range(1, 6)],
    )

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "оценка товара"
        verbose_name_plural = "оценки товаров"

    def __str__(self):
        return f"{self.user.username} — {self.product.name}: {self.value}"

    @staticmethod
    def update_product_rating(product):
        """Пересчитывает и сохраняет средний рейтинг в product.rating."""
        result = product.ratings.aggregate(avg=Avg("value"))
        product.rating = result["avg"] or 0
        product.save(update_fields=["rating"])


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='baskets',
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='baskets',
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    created_timestamp = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "корзины"

    def sum(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Order(models.Model):

    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('cooking', 'Готовится'),
        ('delivery', 'В пути'),
        ('delivered', 'Доставлен'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Пользователь",
    )

    created = models.DateTimeField("Дата создания", auto_now_add=True)

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default='created',
    )

    delivery_address = models.TextField(
        "Адрес доставки",
        null=True,
        blank=True,
    )
    comment = models.TextField(
        "Комментарий к заказу",
        blank=True,
        default="",
    )
    card_last_four = models.CharField(
        "Последние 4 цифры карты",
        max_length=4,
        blank=True,
        default="",
    )

    total_price = models.DecimalField(
        "Сумма заказа",
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ",
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество")

    class Meta:
        verbose_name = "позиция заказа"
        verbose_name_plural = "позиции заказа"

    def sum(self):
        return self.price * self.quantity