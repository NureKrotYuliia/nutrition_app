from django.views.generic import ListView, DetailView
from .models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/list.html"
    context_object_name = "recipes"
    paginate_by = 10


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"
    context_object_name = "recipe"
