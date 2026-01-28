from django import forms
from apps.payments.models import BalanceType,PaymentMethod

class WalletChargeForm(forms.Form):
    amount = forms.DecimalField(max_digits=30,decimal_places=6,min_value=1,label="Amount to Charge")
    balance_type = forms.ChoiceField(choices=BalanceType.choices,label="Currency")
    payment_method = forms.ChoiceField(choices=PaymentMethod.choices,label="Method")#TODO remove inplace payment and payment with walet if you are not ready dot exchange types