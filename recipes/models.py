from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product
from decimal import Decimal


class Recipe(models.Model):
    title = models.CharField("Назва рецепта", max_length=150)
    description = models.TextField("Опис", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    is_approved = models.BooleanField("Підтверджено модератором", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепти"

    def __str__(self):
        return self.title

    # —— агреговані значення для всього рецепта
    @property
    def total_weight_g(self) -> Decimal:
        return sum((ing.quantity_g for ing in self.ingredients.all()), Decimal("0"))

    @property
    def calories_kcal(self) -> Decimal:
        total = Decimal("0")
        for ing in self.ingredients.select_related("product"):
            total += (ing.product.calories_kcal * ing.quantity_g) / Decimal("100")
        return total.quantize(Decimal("0.01"))

    @property
    def protein_g(self) -> Decimal:
        total = Decimal("0")
        for ing in self.ingredients.select_related("product"):
            total += (ing.product.protein_g * ing.quantity_g) / Decimal("100")
        return total.quantize(Decimal("0.01"))

    @property
    def fat_g(self) -> Decimal:
        total = Decimal("0")
        for ing in self.ingredients.select_related("product"):
            total += (ing.product.fat_g * ing.quantity_g) / Decimal("100")
        return total.quantize(Decimal("0.01"))

    @property
    def carbs_g(self) -> Decimal:
        total = Decimal("0")
        for ing in self.ingredients.select_related("product"):
            total += (ing.product.carbs_g * ing.quantity_g) / Decimal("100")
        return total.quantize(Decimal("0.01"))

    # На 100 г готового рецепта
    def per100g(self) -> dict:
        w = self.total_weight_g or Decimal("1")
        k = (self.calories_kcal / w) * Decimal("100")
        p = (self.protein_g / w) * Decimal("100")
        f = (self.fat_g / w) * Decimal("100")
        c = (self.carbs_g / w) * Decimal("100")
        q = Decimal("0.01")
        return {
            "kcal_100g": k.quantize(q),
            "protein_100g": p.quantize(q),
            "fat_100g": f.quantize(q),
            "carbs_100g": c.quantize(q)
        }


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Рецепт"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт"
    )
    quantity_g = models.DecimalField(
        "К-сть (г)",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    note = models.CharField("Примітка", max_length=120, blank=True)

    class Meta:
        unique_together = ("recipe", "product")
        verbose_name = "Інгредієнт рецепта"
        verbose_name_plural = "Інгредієнти рецепта"

    def __str__(self):
        return f"{self.product.name} — {self.quantity_g} г"
