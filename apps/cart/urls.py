from django.urls import path
from .views import AddToCartView,ShowCart,DecreaseFromCart

urlpatterns = [
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path('', ShowCart.as_view(), name='show_cart'),
    path("Decrease/<int:product_id>",DecreaseFromCart.as_view(),name="decrease_item"),
]