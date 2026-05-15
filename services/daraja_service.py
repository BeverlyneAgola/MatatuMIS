import requests
import base64
from requests.auth import HTTPBasicAuth
from datetime import datetime
from config import CALLBACK, KEY, SECRET, O_URL, S_URL, code, PASSKEY, PASSWORD

class DarajaService:
    consumer_key = KEY
    consumer_secret = SECRET
    oauth_url = O_URL
    stk_url = S_URL
    shortcode = code
    passkey = PASSKEY

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
            "Password": PASSWORD,
            "Timestamp": "20260307215549",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": CALLBACK,
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