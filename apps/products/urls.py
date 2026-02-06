from django.urls import path
from .views import ProductsView,ProductView,product_search

urlpatterns = [
    path('', ProductsView.as_view(), name='product_list'),
    path('<int:pk>/', ProductView.as_view(), name='product_detail'),
    path("search/", product_search, name="search"),
]