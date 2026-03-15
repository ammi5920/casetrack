from flask import Flask, render_template, request, redirect, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"

DATA_FILE = "cases.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE,"w") as f:
        json.dump([],f)


def load_cases():
    with open(DATA_FILE) as f:
        return json.load(f)


def save_cases(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=2)


@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        if request.form["username"]=="admin" and request.form["password"]=="admin123":
            session["user"]="admin"
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    cases = load_cases()

    return render_template("dashboard.html", cases=cases)


@app.route("/create", methods=["GET","POST"])
def create():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        cases = load_cases()

        case = {
            "id": len(cases)+1,
            "title": request.form["title"],
            "status": request.form["status"],
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        cases.append(case)

        save_cases(cases)

        return redirect("/dashboard")

    return render_template("create_case.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run()