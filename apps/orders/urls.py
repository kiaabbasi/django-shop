from django.urls import path
from .views import CreateOrder,ShowOrder,ShowOrders,CanselOrder
#Order
urlpatterns = [
    path("create/", CreateOrder.as_view(), name="create"),
    path("<int:pk>/detail",ShowOrder.as_view(),name="order_detail"),
    path("",ShowOrders.as_view(),name="show_all_user_order"),
    path("<int:pk>/cansel",CanselOrder.as_view(),name="cansel")
]