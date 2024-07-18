import requests
import json
from decouple import config


def make_paypal_payment(amount, currency, return_url, cancel_url):
    # Cấu hình PayPal API credentials
    client_id = config("PAYPAL_CLIENT_ID")
    secret = config("PAYPAL_SECRET")
    url = config("PAYPAL_BASE_URL")
    # Cấu hình API endpoints
    base_url = url
    token_url = base_url + '/v1/oauth2/token'
    payment_url = base_url + '/v1/payments/payment'

    # Cấu hình token
    token_payload = {'grant_type': 'client_credentials'}
    token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

    if token_response.status_code != 200:
        return False, "Failed to authenticate with PayPal API", None

    access_token = token_response.json()['access_token']

    # Tạo payment payload
    payment_payload = {
        'intent': 'sale',
        'payer': {'payment_method': 'paypal'},
        'transactions': [{
            'amount': {'total': str(amount), 'currency': currency},
            'description': 'Vulnvision scan & protect '
        }],
        'redirect_urls': {
            'return_url': return_url,
            'cancel_url': cancel_url
        }
    }

    # Tạo payment request headers
    payment_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Gọi payment transaction
    payment_response = requests.post(payment_url, data=json.dumps(payment_payload), headers=payment_headers)
    # print(payment_response.text)
    if payment_response.status_code != 201:
        return False, 'Failed to create PayPal payment.', None

    payment_id = payment_response.json()['id']
    approval_url = next(link['href'] for link in payment_response.json()['links'] if link['rel'] == 'approval_url')

    return True, payment_id, approval_url


def verify_paypal_payment(payment_id):
    client_id = config("PAYPAL_CLIENT_ID")
    secret = config("PAYPAL_SECRET")
    url = config("PAYPAL_BASE_URL")

    base_url = url
    token_url = base_url + '/v1/oauth2/token'
    payment_url = base_url + '/v1/payments/payment'

    token_payload = {'grant_type': 'client_credentials'}
    token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

    if token_response.status_code != 200:
        raise Exception('Failed to authenticate with PayPal API.')

    access_token = token_response.json()['access_token']

    payment_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payment_details_url = f'{payment_url}/{payment_id}'
    payment_details_response = requests.get(payment_details_url, headers=payment_headers)

    if payment_details_response.status_code != 200:
        raise Exception('Failed to retrieve PayPal payment details.')

    payment_status = payment_details_response.json()['payer']['status']
    if payment_status == 'VERIFIED':
        # Payment is successful, process the order
        # Retrieve additional payment details if needed
        payer_email = payment_details_response.json()['payer']['payer_info']['email']
        # ... process the order ...
        return True
    else:
        # Payment failed or was canceled
        return False


# Thực hiện hoàn tiền cho user khi hủy hóa đơn
def refund_paypal_payment(order_id, amount, currency, return_url, cancel_url):
    # Cấu hình PayPal API credentials
    client_id = config("PAYPAL_CLIENT_ID")
    secret = config("PAYPAL_SECRET")
    url = config("PAYPAL_BASE_URL")
    # Cấu hình API endpoints
    base_url = url
    token_url = base_url + '/v1/oauth2/token'
    refund_url = f'{base_url}/v1/payments/order/{order_id}/refund'  

    # Cấu hình token
    token_payload = {'grant_type': 'client_credentials'}
    token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

    if token_response.status_code != 200:
        return False, "Failed to authenticate with PayPal API", None

    access_token = token_response.json()['access_token']

    # Thực hiện hoàn tiền
    refund_payload = {
        'transactions': [{
            'amount': {'total': str(amount), 'currency': currency},
            'description': 'Vulnvision scan & protect '
        }],
        'redirect_urls': {
            'return_url': return_url,
            'cancel_url': cancel_url
        }
    }
    # Tạo refund request headers
    refund_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    # Gọi refund transaction
    refund_response = requests.post(refund_url, data=json.dumps(refund_payload), headers=refund_headers)
    # print(payment_response.text)
    if refund_response.status_code != 201:
        return False, 'Failed to create PayPal payment.', None
    # Kiểm tra id của refund
    refund_id = refund_responsive.json()['id']
    approval_url = next(link['href'] for link in refund_response.json()['links'] if link['rel'] == 'approval_url')

    return True, refund_id, approval_url, 'Refund Successful'
