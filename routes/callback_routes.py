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
    checkout_req_id = stk_callback.get("CheckoutRequestID")

    if result_code == 0:
        metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])

        update_data = {
            "ResultDesc": stk_callback.get("ResultDesc"),
            "Status": "Completed",
            "ReceivedAt": datetime.datetime.now()
        }

        for item in metadata:
            if item["Name"] == "Amount":
                update_data["Amount"] = item["Value"]
            elif item["Name"] == "MpesaReceiptNumber":
                update_data["TransactionID"] = item["Value"]
            elif item["Name"] == "PhoneNumber":
                update_data["PhoneNumber"] = item["Value"]

        result = payments_col.update_one(
            {"CheckoutRequestID": checkout_req_id},
            {"$set": update_data}
        )

        print("Matched:", result.matched_count)

    else:
        payments_col.update_one(
            {"CheckoutRequestID": checkout_req_id},
            {
                "$set": {
                    "Status": "Failed",
                    "ResultDesc": stk_callback.get("ResultDesc")
                }
            }
        )

    return jsonify({"ResultCode": 0, "ResultDesc": "Processed"}), 200