from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model ánh xạ với bảng đã tạo sẵn trong PostgreSQL

# Bảng users
class User(db.Model):
    __tablename__ = 'users'
    
    user_fullname = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), primary_key=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    user_phonenumber = db.Column(db.String(15), nullable=False)
    
# Bảng students
class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.String(10), primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    
    # Quan hệ 1 học sinh - nhiều scores
    scores = db.relationship(
        'Score', 
        back_populates='student', 
        cascade="all, delete")

    def __repr__(self):
        return f"<Student {self.student_id} - {self.student_name}>"


# Bảng subjects
class Subject(db.Model):
    __tablename__ = 'subjects'
    
    subject_id = db.Column(db.String(10), primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)

    # Quan hệ 1 môn - nhiều Scores
    scores = db.relationship(
        'Score', 
        back_populates='subject', 
        cascade="all, delete")

    def __repr__(self):
        return f"<Subjects {self.subject_id} - {self.subject_name}>"


# Bảng scores
class Score(db.Model):
    __tablename__ = 'scores'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('students.student_id', ondelete="CASCADE"))
    subject_id = db.Column(db.String(10), db.ForeignKey('subjects.subject_id', ondelete="CASCADE"))
    attendance = db.Column(db.Float)
    midterm = db.Column(db.Float)
    final_exam = db.Column(db.Float)
    overall = db.Column(db.Float)

    # Quan hệ ngược
    student = db.relationship('Student', back_populates='scores')
    subject = db.relationship('Subject', back_populates='scores')

    def __repr__(self):
        return f"<Score {self.student_id} - {self.subject_id}: {self.overall}>"
    
    