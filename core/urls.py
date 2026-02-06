from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('apps.users.urls',"accounts"), namespace="accounts")),
    path('product/', include(('apps.products.urls',"products"),namespace="products")),
    path("cart/", include(("apps.cart.urls", "cart"), namespace="cart")),
    path("order/", include(("apps.orders.urls", "orders"), namespace="orders")),
    path("payment/", include(("apps.payments.urls", "payments"), namespace="payments")),
    path("zarinpall/", include(("apps.zarinpal.urls", "zarinpall"), namespace="zarinpall")),
    path("wallet/", include(("apps.wallet.urls", "wallet"), namespace="wallets")),
    path("comments/", include(("apps.comments.urls", "comments"), namespace="comments")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)