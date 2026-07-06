from flask import Flask, render_template, request, flash, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "xfactor-semi-secret"

# ── Change this password to whatever you want ──
SITE_PASSWORD = "xfactor2026"


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == SITE_PASSWORD:
            session["authenticated"] = True
            return redirect(request.args.get("next") or "/")
        flash("Incorrect password. Please try again.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    return render_template("home.html")


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/services")
@login_required
def services():
    return render_template("services.html")


@app.route("/case-studies")
@login_required
def case_studies():
    return render_template("case_studies.html")


@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if name and email and message:
            flash("Thank you! Your message has been received. We will get back to you shortly.", "success")
        else:
            flash("Please fill in all required fields.", "danger")
        return redirect(url_for("contact"))
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
