from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from dotenv import load_dotenv
from model import db, students, subjects, scores

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

# Tài khoản mẫu
users = {
    "admin": "123456",
    "teacher": "giaovien123"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("score"))
        else:
            return render_template("login.html", error="Sai tài khoản hoặc mật khẩu!")

    return render_template("login.html")

@app.route("/score")
def score():
    if "username" in session:
        return render_template("score.html", username=session["username"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/student_score")
def student_score():
    if request.method == "POST":
        student_fullname = request.form["student_name"]
        id_student = request.form["student_id"]
        
        if student_fullname in students.student_name and id_student in students.student_id:
            return  render_template("student_score.html")
        else:
            return redirect(url_for("score"))
    
    return render_template("score.html")

if __name__ == "__main__":
    app.run(port=os.getenv("SV_PORT"),debug=True)
