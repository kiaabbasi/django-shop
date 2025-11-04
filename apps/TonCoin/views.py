from django.shortcuts import render,get_object_or_404
from apps.payments.models import Payment
from django.http import JsonResponse
from apps.TonCoin.models import TonPaymentRequest , Wallet_admin ,TonTransaction
from django.views import View

def get_admin_wallet()-> Wallet_admin:
    wallet = Wallet_admin.objects.filter(is_active=True).first()
    if not wallet:
        raise ValueError("No active admin wallet found")
    return wallet

class TonCoinCreateTransactionRequest(View):
   

    def post(self, request, payment_id):# THis view creates a TonCoin payment request for a given payment ID
        
        payment_cart = get_object_or_404(Payment, id=payment_id, method='TON')


        if request.user != payment_cart.order.user:
            return JsonResponse({"message" :"Unauthorized"}, status=403)

        if payment_cart.status != 'pending':
            return JsonResponse({"message":"Payment status must be pending"}, status=400)

        code=str(payment_cart.id)
        TonPaymentRequest.objects.create(
            payment=payment_cart,
            amount=payment_cart.amount,
            address=get_admin_wallet(),
            message=code
        )

        return JsonResponse({"message": "TonCoin Payment Request Created","code":code}, status=201)


class TonCoinSeeStatus(View):
    def post(self, request, payment_id):# this is show the TonCoin payment status
        payment_cart = get_object_or_404(Payment, id=payment_id)
        if request.user != payment_cart.order.user:
            return JsonResponse({"message" :"Unauthorized"}, status=403)

        try:
            tpr= TonPaymentRequest.objects.get(payment=payment_cart)
            tt = TonTransaction.objects.get(message=tpr.message)
            return JsonResponse({
                "message":"TonCoin Payment Request Found",
                "payment_status": payment_cart.status,
                "ton_transaction_status": tt.status,
                "ton_transaction_hash": tt.tx_hash
            }, status=200)
        except TonPaymentRequest.DoesNotExist:
            return JsonResponse({"message":"TonCoin Payment Request Not Found"}, status=404)
        except TonTransaction.DoesNotExist:
            return JsonResponse({"message":"TonCoin Transaction Not Found"}, status=404)