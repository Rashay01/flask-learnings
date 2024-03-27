from flask import Blueprint, request, render_template
from app import User, db

users_bp = Blueprint("users", __name__)

users = [
    {"id": "1", "username": "Test", "password": "password01"},
    {"id": "2", "username": "Rashay", "password": "password1"},
]


@users_bp.route("/login", methods=["GET"])
def forms_page():
    return render_template("forms.html")


@users_bp.route("/dashboard1", methods=["POST"])
def dashboard1_page():
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return render_template("dashboard1.html", username=username)


@users_bp.route("/sign-up", methods=["GET"])
def sign_up_page():
    return render_template("register.html")
