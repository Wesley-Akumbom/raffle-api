import requests
from django.conf import settings
import json


class FlutterwaveClient:
    def __init__(self):
        self.base_url = "https://api.flutterwave.com/v3"  # Use the Flutterwave API base URL
        self.secret_key = settings.FLUTTERWAVE_SECRET_KEY  # Add this to your settings

    def initiate_mobile_money_payment(self, amount, phone_number, tx_ref, fullname):
        """ Initiates a mobile money payment request """
        url = f"{self.base_url}/charges?type=mobile_money_franco"  # Adjusted for Cameroon
        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }

        # Use a placeholder email
        placeholder_email = "keyzwesley@gmail.com"

        payload = {
            "tx_ref": tx_ref,
            "amount": str(amount),
            "currency": "XAF",  # CFA Franc
            "payment_type": "mobilemoneyfranco",
            "redirect_url": "https://your-redirect-url.com",
            "phone_number": phone_number,  # Moved outside the mobile_money object
            "fullname": fullname,  # Use fullname from user object
            "email": "keyzwesley@gmail.com",  # Collect or use a placeholder email
            "mobile_money": {
                "provider": "mtn"  # You can keep the provider here or include it elsewhere based on API requirements
            }
        }

        print("Sending payment request with payload:", json.dumps(payload, indent=4))  # Pretty print for clarity

        response = requests.post(url, json=payload, headers=headers)

        # Log the full response for debugging
        print("Response status code:", response.status_code)
        print("Response content:", response.json())

        return response.json()

    def check_transaction_status(self, tx_ref):
        """ Check the transaction status """
        url = f"{self.base_url}/transactions/{tx_ref}/verify"
        headers = {
            'Authorization': f'Bearer {self.secret_key}'
        }
        response = requests.get(url, headers=headers)
        return response.json()