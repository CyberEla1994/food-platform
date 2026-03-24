from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'
    verbose_name = 'Товары'

    def ready(self):
        from django.contrib.auth.signals import user_logged_in
        from .views import _merge_session_basket

        def on_login(sender, request, user, **kwargs):
            _merge_session_basket(request, user)

        user_logged_in.connect(on_login)
