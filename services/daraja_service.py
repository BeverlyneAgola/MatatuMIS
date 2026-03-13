import requests
import base64
from requests.auth import HTTPBasicAuth
from datetime import datetime

class DarajaService:
    consumer_key = 'RiAQBIsjvkTl6uXI5owaCAmXzNMMjzyyNYCHWVCAROIRAnXJ'
    consumer_secret = 'Uxzw1OpAqXHhNinbUuUDW7Tl8K8GA9mKWMIn9LTxnEAAje753DW09qjEefznCLqH'
    oauth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    stk_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    shortcode = '174379'
    passkey = 'bfb279f9aa9bdbcf158e97dd8e6bca9b5dcb6c7f5d2b0fdbf9c4a6e7d8f9e6f'

    def get_access_token(self):
        """Generates OAuth token"""
        try:
            response = requests.get(
                self.oauth_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            print("TOKEN RESPONSE:", data)
            return data.get("access_token")
        except Exception as e:
            print("Failed to get access token:", e)
            return None

    

    def initiate_stk_push(self, amount, phone_number, account_reference, transaction_desc):
        """Initiates STK push to the given phone number"""
        token = self.get_access_token()
        if not token:
            return {"error": "Failed to generate access token"}

        # Format phone number
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]
        elif phone_number.startswith("+254"):
            phone_number = phone_number[1:]

       
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjYwMzA3MjE1NTQ5",
            "Timestamp": "20260307215549",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://036e-105-161-107-141.ngrok-free.app/callback",
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.stk_url, json=payload, headers=headers, timeout=60)
            print("STK RESPONSE:", response.text)
            return response.json()
        except Exception as e:
            print("STK push request failed:", e)
            return {
                "error": "Invalid response from M-Pesa API",
                "details": str(e)
            }