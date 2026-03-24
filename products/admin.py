from django.contrib import admin
from .models import ProductCategory, Product, ProductRating, Basket, Order, OrderItem


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'rating', 'category')
    list_filter = ('category',)


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'value')
    list_filter = ('value',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'card_last_four', 'created')
    list_filter = ('status',)
    search_fields = ('user__username', 'delivery_address', 'comment')
    inlines = [OrderItemInline]