from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('profile/', TemplateView.as_view(template_name="users/profile.html"), name='profile'),
]

