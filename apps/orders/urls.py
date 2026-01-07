from django.urls import path
from .views import CreateOrder,ShowOrder

urlpatterns = [
    path("create/", CreateOrder.as_view(), name="create"),
    path("<int:pk>",ShowOrder.as_view(),name="order_detail")
]