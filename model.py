from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model ánh xạ với bảng đã tạo sẵn trong PostgreSQL

# Bảng users
class User(db.Model):
    __tablename__ = 'users'
    
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), primary_key=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    user_phonenumber = db.Column(db.INTEGER, nullable=False)
    
# Bảng students
class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.String(10), primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    
    # Quan hệ 1-n với scores
    scores = db.relationship(
        'Score', 
        back_populates='students', 
        cascade="all, delete")

    def __repr__(self):
        return f"<Student {self.student_id} - {self.student_name}>"


# Bảng subjects
class Subject(db.Model):
    __tablename__ = 'subjects'
    
    subject_id = db.Column(db.String(10), primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)

    # Quan hệ 1-n với Scores
    scores = db.relationship('Score', back_populates='subjects', cascade="all, delete")

    def __repr__(self):
        return f"<Subjects {self.subject_id} - {self.subject_name}>"


# Bảng scores
class Score(db.Model):
    __tablename__ = 'scores'
    
    # Không có primary key trong bảng Scores → NÊN thêm cột id hoặc set PK composite
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    student_id = db.Column(db.String(10), db.ForeignKey('Students.student_id', ondelete="CASCADE"))
    subject_id = db.Column(db.String(10), db.ForeignKey('Subjects.subject_id', ondelete="CASCADE"))
    
    attendance = db.Column(db.Float)
    midterm = db.Column(db.Float)
    final_exam = db.Column(db.Float)
    overall = db.Column(db.Float)

    # Quan hệ ngược
    student = db.relationship('Student', back_populates='Scores')
    subject = db.relationship('Subject', back_populates='Scores')

    def __repr__(self):
        return f"<Score {self.student_id} - {self.subject_id}: {self.overall}>"
    
    