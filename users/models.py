from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


class User(AbstractUser):

    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)

    phone = models.CharField("Телефон", max_length=20, blank=True)

    birth_date = models.DateField(
        "Дата рождения",
        null=True,
        blank=True
    )

    gender = models.CharField(
        "Пол",
        max_length=10,
        choices=[
            ("male", "Мужской"),
            ("female", "Женский")
        ],
        blank=True
    )

    avatar = models.ImageField(
        "Аватар",
        upload_to="avatars/",
        blank=True,
    )

    GENDER_AVATAR_MAP = {
        "male": "img/avatars/default_male.png",
        "female": "img/avatars/default_female.png",
    }
    DEFAULT_AVATAR = "img/avatars/default_neutral.png"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static(self.GENDER_AVATAR_MAP.get(self.gender, self.DEFAULT_AVATAR))

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"