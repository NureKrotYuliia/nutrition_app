from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField("Назва", max_length=120, unique=True)
    calories_kcal = models.DecimalField("Калорійність (ккал/100г)", max_digits=8, decimal_places=2,
                                        validators=[MinValueValidator(0)])
    protein_g = models.DecimalField("Білки (г/100г)", max_digits=8, decimal_places=2,
                                    validators=[MinValueValidator(0)])
    fat_g = models.DecimalField("Жири (г/100г)", max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0)])
    carbs_g = models.DecimalField("Вуглеводи (г/100г)", max_digits=8, decimal_places=2,
                                  validators=[MinValueValidator(0)])

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Автор (хто додав)"
    )
    is_approved = models.BooleanField("Підтверджено модератором", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    def __str__(self):
        return self.name
