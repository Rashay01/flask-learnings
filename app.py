from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, Sanlam! 😁</p>"


@app.route("/about")
def about():
    return "<h1 style ='font-size: 50px'>About Page</h1>"
