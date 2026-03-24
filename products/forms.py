from django import forms
from food_platform.form_mixins import BootstrapFormMixin


class OrderCreateForm(BootstrapFormMixin, forms.Form):
    """Форма оформления заказа: карта, адрес доставки, комментарий."""

    card_number = forms.CharField(
        label="Номер карты",
        max_length=19,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control js-format-card",
            "placeholder": "0000 0000 0000 0000",
            "autocomplete": "cc-number",
            "inputmode": "numeric",
        }),
        help_text="16 цифр",
    )
    delivery_address = forms.CharField(
        label="Адрес доставки",
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Город, улица, дом, квартира, подъезд, этаж",
        }),
    )
    comment = forms.CharField(
        label="Комментарий к заказу",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 2,
            "placeholder": "Пожелания по доставке, контактный телефон и т.п.",
        }),
    )

    def clean_card_number(self):
        value = self.cleaned_data.get("card_number", "").replace(" ", "").replace("-", "")
        if not value.isdigit():
            raise forms.ValidationError("Введите только цифры карты.")
        if len(value) != 16:
            raise forms.ValidationError("Номер карты должен содержать 16 цифр.")
        return value

