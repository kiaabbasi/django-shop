from django.urls import path
from .views import AddComment

urlpatterns = [
    path("product/<int:pk>/comment/", AddComment.as_view(), name="add_comment"),
]
