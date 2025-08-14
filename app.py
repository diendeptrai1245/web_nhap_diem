from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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
# db = SQLAlchemy(app)
db.init_app(app)

app.secret_key = os.getenv('API_TOKEN')  # Bảo mật session
app.permanent_session_lifetime = timedelta(minutes=30)


# SIGN IN
@app.route("/", methods=["GET", "POST"])
def login():
    message = request.args.get("message")
    if request.method == "POST":
        userID = request.form["user_email"]
        password = request.form["password"]
        
        # Kiểm tra trống
        if not userID or not password:
            return render_template("login.html", error="Please input both email and password")

        user = User.query.filter_by(user_email=userID).first()
        
        if user and user.user_password == password:
            session["username"] = user.user_fullname
        
            return redirect(url_for("score"))
        else:
            return render_template("login.html", error="Wrong email or password!")

    return render_template("login.html")

# SIGN UP FUNCTON
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        phonenumber = request.form["phone_number"]
        
        account = User.query.filter_by(user_email=email).first()
        if account and account.user_email:
            return render_template("register.html", error="Email existed!")

        #Create new account
        new_user = User(
            user_fullname = fullname,
            user_email = email,
            user_password = password,
            user_phonenumber = phonenumber
        )
        
        #Save in database
        db.session.add(new_user)
        db.session.commit()
        
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))  
    
    return render_template("register.html")
  
@app.route("/search_student", methods=["POST"])
def search_student():
    student_id = request.form["student_id"].strip()
    student = students_scores.get(student_id)
    if student:
        return jsonify({"status": "found", "student": student, "id": student_id})
    else:
        return jsonify({"status": "not_found"})
    
# LOG OUT
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# STUDENT SCORE
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


if __name__ == "__main__":
    app.run(port=os.getenv("SV_PORT"),debug=True)