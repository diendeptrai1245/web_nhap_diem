from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from dotenv import load_dotenv
from model import db, Student, Subject, Score, User

load_dotenv()

app = Flask(__name__)

# Kết nối PostgreSQL
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




app.secret_key = os.getenv('API_TOKEN')  # Bảo mật session
app.permanent_session_lifetime = timedelta(minutes=30)


# SIGN IN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userID = request.form["user_email"]
        password = request.form["password"]

        user = User.query.filter_by(user_email=userID).First()
        
        if user and User.user_password == password:
            session["username"] = user.user_email
        
            return redirect(url_for("score"))
        else:
            return render_template("login.html", error="Sai tài khoản hoặc mật khẩu!")

    return render_template("login.html")

#SCORE
@app.route("/score")
def score():
    if "username" in session:
        return render_template("score.html", username=session["username"])
    return redirect(url_for("login"))

#LOG OUT
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

#STUDENT SCORE
@app.route("/student_score")
def student_score():
    if request.method == "POST":
        student_fullname = request.form["student_name"]
        id_student = request.form["student_id"]
        
        if student_fullname in Student.student_name and id_student in Student.student_id:
            return  render_template("student_score.html")
        else:
            return redirect(url_for("score"))
    
    return render_template("score.html")

#SIGN UP
@app.route("/register")
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        # if email = 

if __name__ == "__main__":
    app.run(port=os.getenv("SV_PORT"),debug=True)
