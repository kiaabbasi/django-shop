from django.shortcuts import redirect, HttpResponse
from django.conf import settings
import requests
import json
from apps.payments.models import Payment
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Bank_Transaction


MERCHANT = "YOUR_MERCHANT_ID_HERE"
ZP_API_REQUEST = f"https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"
if settings.SANDBOX:
    
    ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    ZP_API_STARTPAY ="https://sandbox.zarinpal.com/pg/StartPay/"



domain = '127.0.0.1:8000/'


def send_request(request, payment_id, total_price):
    payment_want_to_pay= get_object_or_404(Payment.objects.get(id = payment_id))

    if  payment_want_to_pay.successful:
        return HttpResponse('این پرداخت قبلا انجام شده است.')
    data = {
        "merchant_id": settings.MERCHANT ,
        "amount": total_price,  # دریافت مبلغ پرداخت به عنوان پارامتر
        "description": "خرید",
        "mobile": "",
        "callback_url":  f"{domain}zarinpal/verify/{payment_id}",
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    try:
        
        response = requests.post(ZP_API_REQUEST,data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            if response_json['data']['code'] == 100:
                return redirect(ZP_API_STARTPAY + str(response_json['data']['authority']))
            else:
                return HttpResponse(f'Error: {response_json['data']["code"]}')
        else:
            return HttpResponse('Failed to get a valid response from the payment gateway.')

    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


#http://127.0.0.1:8000/zarinpal/verify/2?Authority=A00000000000000000000000000202690354&Status=OK
@csrf_exempt
def verify(request, order_id):
    
    authority = request.GET.get('Authority')
    status = request.GET.get("Status")
    if  status =="NOK":
        return HttpResponse('پرداخت ناموفق')
    
    peyment_want_to_pay = get_object_or_404(Payment.objects.get(id = order_id))
    total_price = peyment_want_to_pay.amount

   
    data = {
        "merchant_id": MERCHANT,
        "amount": total_price,
        "authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['data']['code'] == 100:
            Bank_Transaction.objects.create(
            peyment_on=peyment_want_to_pay, 
            peymentid=str(authority),
        )
            peyment_want_to_pay.successful = True
            peyment_want_to_pay.save()
            
        if response['data']['code'] == 100 or response['data']['code'] == 101:
            return HttpResponse("پرداخت موفق")
        else:
            return HttpResponse('پرداخت ناموفق')
    return HttpResponse('پرداخت ناموفق')
