from django.urls import path
from .views import TonCoinCreateTransactionRequest,TonCoinSeeStatus

urlpatterns = [
    path('ton/create/<int:payment_id>/', TonCoinCreateTransactionRequest.as_view(), name='ton_create'),
    path('ton/status/<int:payment_id>/', TonCoinSeeStatus.as_view(), name='ton_status'),

]
