from django.urls import path
from .views import CreateOrder,ShowOrder,ShowOrders

urlpatterns = [
    path("create/", CreateOrder.as_view(), name="create"),
    path("<int:pk>",ShowOrder.as_view(),name="order_detail"),
    path("",ShowOrders.as_view(),name="show_all_user_order"),

]