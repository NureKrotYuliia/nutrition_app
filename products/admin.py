from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "calories_kcal", "protein_g", "fat_g", "carbs_g", "is_approved", "created_by")
    list_filter = ("is_approved",)
    search_fields = ("name",)
