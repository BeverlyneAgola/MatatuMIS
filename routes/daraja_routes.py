from flask import Blueprint, request, jsonify, render_template
from services.daraja_service import DarajaService
from db.mongodb import get_db
from pymongo import MongoClient
import datetime , certifi
from services.decorator import post_required

daraja_bp = Blueprint("daraja", __name__)
dashboard_bp = Blueprint("dashboard_bp", __name__)

client = MongoClient(
    "mongodb+srv://agola:myfirstdatabase@trial.qwqpkuo.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)
db = client["sacco_management"]
payments_col = db["payments"]


@daraja_bp.route("/payments", methods=["GET"])
def stk_page():
    return render_template("payments/stk_payment.html")

@daraja_bp.route("/payments")
@post_required(["admin", "finance", "conductor"])
def payments_page():
    return render_template("payments/stk_payment.html")

@daraja_bp.route("/api/stkpush", methods=["POST"])
def stk_push():
    data = request.json
    amount = data.get("amount")
    phone_number = data.get("phone_number")
    route = data.get("route")
    vehicle = data.get("vehicle")

    if not amount or not phone_number or not route or not vehicle:
        return jsonify({"error": "Amount, phone, route, and vehicle required"}), 400

    if phone_number.startswith("0"):
        phone_number = "254" + phone_number[1:]

    daraja_service = DarajaService()

    try:
        response = daraja_service.initiate_stk_push(
            amount,
            phone_number,
            account_reference="MatatuHub",
            transaction_desc="Payment"
        )

        # Save pending payment
        payments_col.insert_one({
            "CheckoutRequestID": response.get("CheckoutRequestID"),
            "MerchantRequestID": response.get("MerchantRequestID"),
            "PhoneNumber": phone_number,
            "Amount": float(amount),
            "ResultDesc": "Pending",
            "ReceivedAt": datetime.datetime.now(),
            "Route": route,
            "Vehicle": vehicle
        })

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@daraja_bp.route("/callback", methods=["POST"])
def callback():
    data = request.json
    stk_callback = data.get("Body", {}).get("stkCallback", {})
    result_code = stk_callback.get("ResultCode")
    merchant_req_id = stk_callback.get("MerchantRequestID")
    checkout_req_id = stk_callback.get("CheckoutRequestID")

    if result_code == 0:
        callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
        transaction_update = {"ResultDesc": stk_callback.get("ResultDesc"),
                              "ReceivedAt": datetime.datetime.now()}

        for item in callback_metadata:
            name = item.get("Name")
            value = item.get("Value")
            if name == "Amount":
                transaction_update["Amount"] = value
            elif name == "MpesaReceiptNumber":
                transaction_update["TransactionID"] = value
            elif name == "PhoneNumber":
                transaction_update["PhoneNumber"] = value
            elif name == "TransactionDate":
                transaction_update["TransactionDate"] = value

        # Update the existing payment by CheckoutRequestID
        payments_col.update_one(
            {"CheckoutRequestID": checkout_req_id},
            {"$set": transaction_update}
        )

        return jsonify({"ResultCode": 0, "ResultDesc": "Success"}), 200

    return jsonify({"ResultCode": result_code, "ResultDesc": stk_callback.get("ResultDesc")}), 200

@dashboard_bp.route("/api/recent-payments", methods=["GET"])
def recent_payments():
    db = get_db()
    payments = list(db["payments"].find().sort("ReceivedAt", -1).limit(10))

    result = []
    for p in payments:
        result.append({
            "receipt": p.get("TransactionID", "Pending"),
            "amount": p.get("Amount", 0),
            "phone": p.get("PhoneNumber", "-"),
            "route": p.get("Route", "-"),
            "vehicle": p.get("Vehicle", "-"),
            "date": p.get("TransactionDate") or p.get("ReceivedAt"),
            "status": p.get("ResultDesc", "Pending"),
            "checkout_id": p.get("CheckoutRequestID") or p.get("MerchantRequestID")
        })

    return jsonify(result)