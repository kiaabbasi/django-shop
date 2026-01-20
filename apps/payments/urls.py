from django.urls import path
from .views import CreatePayment

urlpatterns = [
    path("create/<int:order_id>",CreatePayment.as_view(),name="create"),
]