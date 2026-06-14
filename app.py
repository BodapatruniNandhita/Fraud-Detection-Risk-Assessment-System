from flask import Flask, make_response, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    risk_score = None
    risk_level = None
    risk_class = None
    risk_icon = None
    recommendation = None
    transaction_type = None
    account_age = None
    risk_factors = []

    if request.method == "POST":
        amount = float(request.form["amount"])
        transaction_type = request.form["transaction_type"]
        account_age = request.form["account_age"]
        new_device = request.form["new_device"]
        international = request.form["international"]
        multiple = request.form["multiple"]

        risk_score = 0

        if amount > 100000:
            risk_score += 20

        if new_device == "Yes":
            risk_score += 30

        if international == "Yes":
            risk_score += 30

        if multiple == "Yes":
            risk_score += 20

        if account_age == "< 1 Month":
            risk_score += 20

        risk_score = min(risk_score, 100)

        if risk_score < 30:
            risk_level = "Low Risk"
            risk_class = "low"
            risk_icon = "🟢"
        elif risk_score < 60:
            risk_level = "Medium Risk"
            risk_class = "medium"
            risk_icon = "🟠"
        else:
            risk_level = "High Risk"
            risk_class = "high"
            risk_icon = "🔴"

        risk_factors.append(
            {
                "label": "Transaction Amount",
                "detail": f"₹{amount:,.2f}",
                "status": "Low Risk" if amount <= 100000 else "Elevated Risk",
                "class": "warn" if amount > 100000 else "safe",
            }
        )
        risk_factors.append(
            {
                "label": "Account Age",
                "detail": account_age,
                "status": "Low Risk" if account_age != "< 1 Month" else "High Risk",
                "class": "warn" if account_age == "< 1 Month" else "safe",
            }
        )
        risk_factors.append(
            {
                "label": "Device Trust",
                "detail": "New device" if new_device == "Yes" else "Known device",
                "status": "Risky" if new_device == "Yes" else "Low Risk",
                "class": "warn" if new_device == "Yes" else "safe",
            }
        )
        risk_factors.append(
            {
                "label": "Transaction Scope",
                "detail": "International" if international == "Yes" else "Domestic",
                "status": "Risky" if international == "Yes" else "Low Risk",
                "class": "warn" if international == "Yes" else "safe",
            }
        )
        risk_factors.append(
            {
                "label": "Activity Pattern",
                "detail": "Multiple transactions in last hour" if multiple == "Yes" else "Normal frequency",
                "status": "Risky" if multiple == "Yes" else "Low Risk",
                "class": "warn" if multiple == "Yes" else "safe",
            }
        )

        if risk_level == "High Risk":
            recommendation = "Block transaction and request verification"
        elif risk_level == "Medium Risk":
            recommendation = "Send OTP verification"
        else:
            recommendation = "Approve transaction"

    response = make_response(render_template(
        "index.html",
        risk_score=risk_score,
        risk_level=risk_level,
        risk_class=risk_class,
        risk_icon=risk_icon,
        recommendation=recommendation,
        transaction_type=transaction_type,
        account_age=account_age,
        risk_factors=risk_factors,
    ))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
