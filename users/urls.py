from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm, CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/avatar-delete/', views.avatar_delete, name='avatar_delete'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            form_class=CustomLoginForm,
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # 👇 ВАЖНО: меняем URL и name
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            form_class=CustomPasswordResetForm,
            success_url=reverse_lazy('users:reset_password_done')
        ),
        name='reset_password'
    ),

    path(
        'reset-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='reset_password_done'
    ),

    path(
        'reset-password-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            form_class=CustomSetPasswordForm,
            success_url=reverse_lazy('users:reset_password_complete')
        ),
        name='reset_password_confirm'
    ),

    path(
        'reset-password-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='reset_password_complete'
    ),

    path(
        'password-change/',
        views.PasswordChangeViewCustom.as_view(),
        name='password_change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html',
        ),
        name='password_change_done'
    ),
]