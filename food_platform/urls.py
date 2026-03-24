from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Оформление админки на русском
admin.site.site_header = "Администрирование Food Platform"
admin.site.site_title = "Food Platform"
admin.site.index_title = "Главная"
# Смена пароля в админке — в стандартном оформлении админки
admin.site.password_change_template = "admin/auth/password_change_form.html"
admin.site.password_change_done_template = "admin/auth/password_change_done.html"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)