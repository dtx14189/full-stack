from flask import Flask, request, jsonify
from bank import Bank  

app = Flask(__name__)

bank = Bank()

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    return jsonify({"error": str(error)}), 500

@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    account_type = data.get("type")
    if account_type not in ("checking", "savings"):
        return jsonify({"error": "Invalid account type"}), 400
    
    bank.add_account(account_type)
    return jsonify({"message": f"{account_type} account created"}), 201


if __name__ == "__main__":
    app.run(debug=True)
