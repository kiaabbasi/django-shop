from django.apps import AppConfig
import threading
import logging

class ToncoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.TonCoin'

    def ready(self):
        try :
            from .services.ton_transaction_tracer import start_ton_checker
            threading.Thread(target=start_ton_checker, daemon=True).start()
        except ValueError :
            logging.error("No Active Admin Wallet Found. Ton Checker Not Started.")