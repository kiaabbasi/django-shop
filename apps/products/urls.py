from django.urls import path
from .views import ProductsView,ProductView

urlpatterns = [
    path('', ProductsView.as_view(), name='product_list'),
    path('<int:pk>/', ProductView.as_view(), name='product_detail'),
]