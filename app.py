
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "gpay-demo-secret-key"

users = {
    "admin": "1234"
}

balance = 25000.00
transactions = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        session["user"] = username
        return redirect(url_for("dashboard"))

    flash("Invalid username or password")
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    return render_template(
        "dashboard.html",
        balance=balance,
        username=session["user"]
    )


@app.route("/send", methods=["POST"])
def send_money():
    global balance

    if "user" not in session:
        return redirect(url_for("home"))

    receiver = request.form["receiver"]
    amount = float(request.form["amount"])

    if amount <= 0:
        flash("Enter a valid amount")
    elif amount > balance:
        flash("Insufficient balance")
    else:
        balance -= amount

        transactions.append({
            "type": "Money Sent",
            "receiver": receiver,
            "amount": amount
        })

        flash("Demo transaction successful!")

    return redirect(url_for("dashboard"))


@app.route("/recharge", methods=["POST"])
def recharge():
    global balance

    if "user" not in session:
        return redirect(url_for("home"))

    mobile = request.form["mobile"]
    amount = float(request.form["amount"])

    if amount <= 0:
        flash("Enter a valid recharge amount")
    elif amount > balance:
        flash("Insufficient balance")
    else:
        balance -= amount

        transactions.append({
            "type": "Mobile Recharge",
            "receiver": mobile,
            "amount": amount
        })

        flash("Demo recharge successful!")

    return redirect(url_for("dashboard"))


@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("home"))

    return render_template(
        "history.html",
        transactions=transactions
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
