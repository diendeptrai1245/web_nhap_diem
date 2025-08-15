from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from sqlalchemy import func
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
        
            return redirect(url_for("function"))
        else:
            return render_template("login.html", error="Wrong email or password!")

    return render_template("login.html")

# SIGN OUT
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

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
  
# FUNCTION  
@app.route("/function")
def function():
    return render_template("function.html", username=session.get("username"))
    
# FINDING STUDENT
@app.route("/find_student", methods=["GET", "POST"])
def find_student():
    if request.method == "POST":
        student_ID = request.form["student_id"]
        
        student = Student.query.filter(func.lower(Student.student_id) == student_ID.lower()).first()     
        
        if student:
            session["student_id"] = student.student_id
            session["student_name"] = student.student_name
            
            return redirect(url_for("input_student_score"))
        else:
            return render_template("find_student.html", username=session.get("username"), error="Student ID does not exist")
  
    return render_template("find_student.html", username=session.get("username"))

# INPUT STUDENT SCORE
@app.route("/input_student_score", methods=["GET", "POST"])
def input_student_score():
    if request.method == "POST":
        subjects = Subject.query.all()
        for subject in subjects:
            attendance = request.form.get(f"attendance_{subject.subject_id}")
            midterm = request.form.get(f"midterm_{subject.subject_id}")
            final_exam = request.form.get(f"final_exam_{subject.subject_id}")
            overall = request.form.get(f"overall_{subject.subject_id}")

            new_score = Score(
                student_id=session.get("student_id"),
                student_name=session.get("student_name"),
                subject_id=subject.subject_id,
                subject_name=subject.subject_name,
                attendance=float(attendance),
                midterm=float(midterm),
                final_exam=float(final_exam),
                overall=float(overall)
            )
            db.session.add(new_score)

        db.session.commit()
        return "Scores saved successfully!"
    
    return render_template("input_student_score.html", student_id = session.get("student_id"), student_name = session.get("student_name"))

# STUDENT SCORE
@app.route("/student_score")
def student_score():
    if request.method == "POST":
        student_fullname = request.form["student_name"]
        id_student = request.form["student_id"]
        
        if student_fullname in Student.student_name and id_student in Student.student_id:
            return  render_template("student_score.html")
        else:
            return redirect(url_for("logout"))
    
    return render_template("student_score.html")


if __name__ == "__main__":
    app.run(port=os.getenv("SV_PORT"),debug=True)