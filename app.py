from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "smartparkingsecret"

slots = ["Available"] * 6

# User view
@app.route("/")
def home():
    return render_template("index.html", slots=slots)

# Admin login
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["password"] == "admin123":
            session["admin"] = True
            return redirect(url_for("dashboard"))
    return render_template("admin.html")

# Admin dashboard
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    return render_template("dashboard.html", slots=slots)

# Toggle slot (Admin only)
@app.route("/toggle/<int:id>")
def toggle(id):
    if not session.get("admin"):
        return redirect(url_for("admin"))

    if slots[id] == "Available":
        slots[id] = "Occupied"
    else:
        slots[id] = "Available"

    return redirect(url_for("dashboard"))

# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)