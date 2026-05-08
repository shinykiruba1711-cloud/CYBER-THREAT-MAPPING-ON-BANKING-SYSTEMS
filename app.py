from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mail import Mail, Message
import random

attacks = [
    {"username":"admin","location":"Chennai","ip":"192.168.1.1","status":"HIGH","time":"now"},
    {"username":"bot","location":"Mumbai","ip":"10.0.0.2","status":"MEDIUM","time":"now"}
]

app = Flask(__name__)
app.secret_key = "secure_key"

# ---------------- MAIL CONFIG ----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rbharkavi17112004@gmail.com'
app.config['MAIL_PASSWORD'] = 'jdyyehqeafhcrpaz'

mail = Mail(app)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register")
def register():
    return render_template("register.html")


# ---------------- PERSONAL ----------------
@app.route("/personal")
def personal():
    if "user" not in session:
        return redirect("/login")
    return render_template("personal.html")


# ---------------- SECURITY ----------------
@app.route("/security")
def security():
    if "user" not in session:
        return redirect("/login")
    return render_template("security.html")


# ---------------- ADMIN LOGIN ----------------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin":
            session["admin"] = "admin"
            return redirect("/admin_portal")

        return "Invalid Admin Login"

    return render_template("admin_login.html")


# ---------------- ADMIN PORTAL (FIXED) ----------------
@app.route("/admin_portal")
def admin_portal():

    if "admin" not in session:
        return redirect("/admin_login")

    return render_template("admin_dashboard.html")


# ---------------- SEND OTP ----------------
@app.route("/send_otp", methods=["POST"])
def send_otp():

    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    otp = random.randint(100000, 999999)

    session["reg_username"] = username
    session["reg_password"] = password
    session["reg_email"] = email
    session["otp"] = str(otp)

    msg = Message(
        subject="CyberShield Bank OTP Verification",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )

    msg.body = f"Your OTP is {otp}"
    mail.send(msg)

    return redirect("/verify_otp")


# ---------------- VERIFY OTP ----------------
@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":

        if request.form.get("otp") == session.get("otp"):
            session["user"] = session.get("reg_username")
            return redirect("/login")

        return "Wrong OTP"

    return render_template("verify_otp.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == session.get("reg_username") and password == session.get("reg_password"):

            session["user"] = username
            return redirect("/dashboard")

        return "Login Failed"

    return render_template("index.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session and "admin" not in session:
        return redirect("/login")

    return render_template("admin_dashboard.html")


# ---------------- MAP ----------------
@app.route("/map")
def map_page():

    if "user" not in session:
        return redirect("/login")

    return render_template("map.html")

@app.route("/attack_data")
def attack_data():
    return jsonify(attacks)


@app.route("/report_user", methods=["POST"])
def report_user():

    data = request.get_json()

    username = data["username"]
    action = data["action"]

    if action == "BLOCK":

        for user in attacks:
            if user["username"] == username:
                user["status"] = "BLOCKED"

        return jsonify({
            "message": f"{username} account was blocked successfully"
        })

    return jsonify({
        "message": f"{username} was not blocked"
    })

# ---------------- LIVE ATTACKS (FIXED) ----------------
@app.route("/live_attacks")
def live_attacks():

    #--if "admin" not in session:--
        #--return redirect("/admin_login")--

    return render_template("live_attacks.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)