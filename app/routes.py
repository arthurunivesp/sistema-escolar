from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/aba1")
def aba1():
    return render_template("aba1.html")

@main.route("/aba2")
def aba2():
    return render_template("aba2.html")

@main.route("/acesso")
def acesso():
    return render_template("acesso.html")
