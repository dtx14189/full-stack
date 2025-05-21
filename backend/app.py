from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db
from datetime import datetime
from decimal import Decimal, InvalidOperation
from bank import Bank
import exceptions

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/bank_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

bank = Bank()

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    return jsonify({"error": str(error)}), 500

@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    print(data)
    account_type = data.get("type")
    if account_type not in ("checking", "savings"):
        return jsonify({"error": "Invalid account type"}), 400
    
    bank.add_account(account_type)
    return jsonify({"message": f"{account_type} account created"}), 201

@app.route("/accounts", methods=["GET"])
def describe_accounts():
    accounts = bank.describe_accounts()
    return jsonify({"accounts": accounts}), 200

@app.route("/accounts/<account_id>", methods=["GET"])
def describe_account(account_id):
    account = bank.find_account(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"account": account.describe()}), 200

@app.route("/accounts/<account_id>/transactions", methods=["POST"])
def add_transaction(account_id):
    data = request.get_json()
    amount = data.get("amount")
    date_str = data.get("date")

    if amount is None or date_str is None:
        return jsonify({"error": "Missing amount or date"}), 400
    
    try:
        amount = Decimal(str(amount))
    except InvalidOperation:
        return jsonify({"error": "Invalid dollar amount"}), 400
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date() 
    except ValueError:
        return jsonify({"error": "Invalid date. Please try again with a valid date in the format YYYY-MM-DD."}), 400
    
    account = bank.find_account(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    try:
        account.deposit_withdraw(amount, date)
        return jsonify({"message": f"Transaction added to account {account_id}",
                        "balance": str(account.get_bal())}), 201
    except exceptions.OverdrawError:
        return jsonify({"error": "Insufficient balance"}), 400
    except exceptions.TransactionLimitError as e:
        msg = "Daily limit reached" if e.hit_daily_limit else "Monthly limit reached"
        return jsonify({"error": msg}), 400
    except exceptions.TransactionSequenceError as e:
        return jsonify({"error": f"Date must be on or after {e.latest_date}"}), 400

@app.route("/accounts/<account_id>/transactions", methods=["GET"])
def describe_transactions(account_id):
    account = bank.find_account(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    transactions = account.describe_transactions()
    return jsonify({"transactions": transactions}), 200

@app.route("/accounts/<account_id>/apply-interest-fees", methods=["POST"])
def apply_interest_fees(account_id):
    account = bank.find_account(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404

    try:
        account.apply_interest_fees()
        return jsonify({"message": f"Interest and fees applied to account {account_id}",
                        "balance": str(account.get_bal())}), 200
    except exceptions.TransactionSequenceError as e:
        return jsonify({"error": f"Interest and fees already applied for {e.latest_date.strftime('%B')}."}), 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
