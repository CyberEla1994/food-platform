from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.index, name='category'),

    path('basket/', views.basket_view, name='basket'),
    path('add/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('rate/<int:product_id>/', views.set_product_rating, name='set_product_rating'),

    path('basket/clear/', views.clear_basket, name='clear_basket'),
    path('basket/increase/<int:basket_id>/', views.increase_quantity, name='increase_quantity'),
    path('basket/decrease/<int:basket_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('basket/remove/<int:basket_id>/', views.remove_from_basket, name='remove_from_basket'),

    path('basket/s/clear/', views.session_clear, name='session_clear'),
    path('basket/s/increase/<int:product_id>/', views.session_increase, name='session_increase'),
    path('basket/s/decrease/<int:product_id>/', views.session_decrease, name='session_decrease'),
    path('basket/s/remove/<int:product_id>/', views.session_remove, name='session_remove'),

    path('create-order/', views.create_order, name='create_order'),
    path('orders/', views.orders_view, name='orders'),
]