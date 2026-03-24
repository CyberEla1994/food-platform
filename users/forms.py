from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from food_platform.form_mixins import BootstrapFormMixin
from .models import User


class CustomLoginForm(BootstrapFormMixin, AuthenticationForm):
    """Форма входа с едиными Bootstrap-классами для полей."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = {"class": "form-control", "autocomplete": "username"}
        self.fields["username"].widget.attrs.update(attrs)
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "autocomplete": "current-password",
        })


class CustomPasswordChangeForm(BootstrapFormMixin, PasswordChangeForm):
    """Форма смены пароля с form-control и поддержкой глазика в шаблоне."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("old_password", "new_password1", "new_password2"):
            self.fields[name].widget.attrs.update({"class": "form-control"})


class UserRegisterForm(BootstrapFormMixin, UserCreationForm):

    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })


class ProfileForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "gender",
            "birth_date",
            "phone",
            "email",
        ]
        widgets = {
            "avatar": forms.FileInput(),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control js-date-input",
                    "placeholder": "дд.мм.гггг",
                    "autocomplete": "off",
                },
                format="%d.%m.%Y",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "")
            if "form-control" not in field.widget.attrs["class"]:
                field.widget.attrs["class"] += " form-control"
        self.fields["phone"].widget.attrs["class"] += " js-format-phone"
        self.fields["birth_date"].input_formats = ["%d.%m.%Y", "%d.%m.%y"]


class CustomPasswordResetForm(BootstrapFormMixin, PasswordResetForm):
    pass


class CustomSetPasswordForm(BootstrapFormMixin, SetPasswordForm):
    pass