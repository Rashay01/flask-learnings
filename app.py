import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import uuid
from about_bp import about_bp
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length

load_dotenv()  # os env (environment variable)

# db = SQLAlchemy()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
# General pattern - mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

db = SQLAlchemy(app)
# db.init_app(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)


# local
movies = [
    {
        "id": "99",
        "name": "Vikram",
        "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
        "rating": 8.4,
        "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
    },
    {
        "id": "100",
        "name": "RRR",
        "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
        "rating": 8.8,
        "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
        "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
    },
    {
        "id": "101",
        "name": "Iron man 2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
        "rating": 7,
        "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
        "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
    },
    {
        "id": "102",
        "name": "No Country for Old Men",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
        "rating": 8.1,
        "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
        "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
    },
    {
        "id": "103",
        "name": "Jai Bhim",
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
        "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
        "rating": 8.8,
        "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
    },
    {
        "id": "104",
        "name": "The Avengers",
        "rating": 8,
        "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
        "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
        "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
    },
    {
        "id": "105",
        "name": "Interstellar",
        "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
        "rating": 8.6,
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
    },
    {
        "id": "106",
        "name": "Baahubali",
        "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
        "rating": 8,
        "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
        "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
    },
    {
        "id": "107",
        "name": "Ratatouille",
        "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
        "rating": 8,
        "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
        "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
    },
    {
        "name": "PS2",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
        "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
        "rating": 8,
        "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
        "id": "108",
    },
    {
        "name": "Thor: Ragnarok",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
        "rating": 8.8,
        "trailer": "https://youtu.be/NgsQ8mVkN8w",
        "id": "109",
    },
]

name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]


# Model (SQLAlchemy) = Schema
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100))
    poster = db.Column(db.String(255))
    rating = db.Column(db.Float)
    summary = db.Column(db.String(500))
    trailer = db.Column(db.String(255))

    # JSON - Keys
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "summary": self.summary,
            "trailer": self.trailer,
        }


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)  # should be 50
    password = db.Column(db.String(100), nullable=False)

    # JSON - Keys
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }


# try:
#     with app.app_context():
#         result = db.session.execute(text("Select 1")).fetchall()
#         print('print ans')


from movies_bp import movies_bp
from movie_list_bp import movies_list_bp
from users_bp import users_bp

# jinja2 - templates
app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movies_list_bp, url_prefix="/movies-list")
app.register_blueprint(users_bp, url_prefix="/user")


@app.route("/")
def hello_world():
    return "<p>Super, Cool! 😁</p>"


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", movies=movies)


@app.route("/profile")
def profile():
    return render_template("profile.html", name=name, hobbies=hobbies)


@app.route("/sample")
def sample():
    return render_template("sample.html")


# Task - /movies/add -> Add movie form (5 fields) -> Submit -> /movies-list


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


@app.route("/register", methods=["GET", "POST"])
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

    def validate_password(self, field):
        found_user = User.query.filter_by(
            username=field.data, password=self.password.data
        ).first()
        if found_user is None:
            raise ValidationError("Invalid Credentials")

    # def validate_password(self, field):
    #     print(field.data)
    #     found_user = User.query.filter_by(
    #         username=self.username.data, password=field.data
    #     ).first()
    #     print(found_user)
    #     # if found_user is None:
    #     raise ValidationError("Invalid Credentials")

    #  found_user = User.query.filter_by(username=field.data, password = self.password.data).first()
    #  if found_user is None:
    #      raise ValidationError("Invalid Credentials")


@app.route("/login", methods=["GET", "POST"])
def forms_page():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template("dashboard1.html", username=form.username.data)
    return render_template("forms.html", form=form)


# @app.route("/dashboard1", methods=["POST"])
# def dashboard1_page():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return render_template("dashboard1.html", username=form.username.data)
#     return
