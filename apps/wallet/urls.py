from django.urls import path
from .views import ShowWallets,PayWithWallet,ChargWalletRequest

urlpatterns = [
    path("",ShowWallets.as_view(),name="show_all_wallets"),
    path("request/<int:payment_id>",PayWithWallet.as_view(),name="request"),
    path("charge/",ChargWalletRequest.as_view(),name="charge")
]
