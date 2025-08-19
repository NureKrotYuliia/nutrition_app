from django.contrib import admin
from .models import Recipe, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("title", "description")
    inlines = [RecipeIngredientInline]
