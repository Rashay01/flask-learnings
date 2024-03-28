from flask import Blueprint, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length
from app import User, db

user_bp = Blueprint("user", __name__)


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Sign Up")

    # def validate <field name>
    def validate_username(self, field):
        # WTF that there is an error
        found_user = User.query.filter_by(username=field.data).first()
        if found_user:
            raise ValidationError("Username taken")


@user_bp.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()

    if form.validate_on_submit():
        data = {"username": form.username.data, "password": form.password.data}
        new_user = User(**data)

        try:
            db.session.add(new_user)
            db.session.commit()
            return f"<h2>{data['username']} has been registered</h2>"
        except Exception as e:
            db.session.rollback()
            return "<h2>Error Occurred</h2>"

    return render_template("registration.html", form=form)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Login")

    def validate_username(self, field):
        found_user = User.query.filter_by(username=field.data).first()
        if not found_user:
            raise ValidationError("Username taken")

    def validate_password(self, field):
        found_user = User.query.filter_by(username=self.username.data).first()
        if found_user:
            user_found = found_user.to_dict()
            if user_found["password"] != field.data:
                raise ValidationError("Username taken")

    # def validate_password(self, field):
    #     found_user = User.query.filter_by(
    #         username=self.username.data, password=field.data
    #     ).first()
    #     if found_user is None:
    #         raise ValidationError("Invalid Credentials")

    # def validate_username(self, field):
    #     found_user = User.query.filter_by(
    #         username=field.value
    #     ).first()
    #     print(found_user)
    #     # if found_user is None:
    #     raise ValidationError("Invalid Credentials")

    #  found_user = User.query.filter_by(username=field.data, password = self.password.data).first()
    #  if found_user is None:
    #      raise ValidationError("Invalid Credentials")


@user_bp.route("/login", methods=["GET", "POST"])
def forms_page():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template("dashboard1.html", username=form.username.data)
    return render_template("forms.html", form=form)
