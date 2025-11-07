import requests
import time
from decimal import Decimal
from django.conf import settings
from ..models import TonTransaction, TonPaymentRequest,Wallet_admin
from ..views import get_admin_wallet
import logging

TON_API_URL = "https://tonapi.io/v2/blockchain/getTransactions"


def check_ton_transactions(wallet_address):
    """
    این تابع هر بار لیست تراکنش‌های جدید ولت رو می‌گیره و در دیتابیس ذخیره می‌کنه
    """
    try:
        
        response = requests.get(f"{TON_API_URL}?account={wallet_address}&limit=50")
        data = response.json().get("transactions", [])

        for tx in data:
            tx_hash = tx["hash"]
            in_msg = tx.get("in_msg", {})
            message = in_msg.get("message", "")
            amount = Decimal(in_msg.get("value", 0)) / Decimal(1e9)
            sender = in_msg.get("source")
            receiver = in_msg.get("destination")

            if TonTransaction.objects.filter(tx_hash=tx_hash).exists():
                continue  # از تکرار جلوگیری می‌کنه

            ton_tx = TonTransaction.objects.create(
                tx_hash=tx_hash,
                message=message,
                amount=amount,
                sender_address=sender,
                receiver_address=receiver,
            )

            req = TonPaymentRequest.objects.filter(message=message, is_completed=False).first()
            if req and ton_tx.amount >= req.amount:
                ton_tx.matched_request = req
                ton_tx.save()
                req.is_completed = True
                req.save()

        

    except Exception as e:
        logging.error(f"Error checking TON transactions: {e}")
        #print("❌ Error checking TON transactions:", e)


def start_ton_checker():
    """
    حلقه‌ی همیشگی که هر ۳۰ ثانیه یک بار check_ton_transactions را اجرا می‌کند.
    """
    while True:
        for w in Wallet_admin.objects.filter(is_active=True):
            check_ton_transactions(w.address)
        time.sleep(30)
