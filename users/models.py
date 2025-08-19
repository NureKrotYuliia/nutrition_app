from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user", "Користувач"
        MODERATOR = "moderator", "Модератор"

    role = models.CharField(
        max_length=15,
        choices=Roles.choices,
        default=Roles.USER,
        help_text="Роль визначає права доступу"
    )

    def is_moderator(self) -> bool:
        return self.role == self.Roles.MODERATOR
