from flask import Blueprint, request, jsonify
import datetime
from db.mongodb import get_db

callback_bp = Blueprint("callback_bp", __name__)

db = get_db()
payments_col = db["payments"] if db is not None else None


@callback_bp.route("/callback", methods=["POST"])
def mpesa_callback():
    if not payments_col:
        return jsonify({"error": "Database not available"}), 500

    data = request.json
    stk_callback = data.get("Body", {}).get("stkCallback", {})

    result_code = stk_callback.get("ResultCode")
    merchant_req_id = stk_callback.get("MerchantRequestID")
    checkout_req_id = stk_callback.get("CheckoutRequestID")

    if result_code == 0:
        callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])

        transaction_update = {
            "ResultDesc": stk_callback.get("ResultDesc"),
            "ReceivedAt": datetime.datetime.now()
        }

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

        # Update the existing payment
        update_result = payments_col.update_one(
            {"CheckoutRequestID": checkout_req_id},  # match pending record
            {"$set": transaction_update}
        )

        print(f"Matched {update_result.matched_count}, Modified {update_result.modified_count}")

        return jsonify({"ResultCode": 0, "ResultDesc": "Success"}), 200

    return jsonify({
        "ResultCode": result_code,
        "ResultDesc": stk_callback.get("ResultDesc")
    }), 200