from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model ánh xạ với bảng đã tạo sẵn trong PostgreSQL
class students(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.String(10), primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    
    # Quan hệ 1-n với Scores
    scores = db.relationship('Score', back_populates='student', cascade="all, delete")

    def __repr__(self):
        return f"<Student {self.student_id} - {self.student_name}>"


# Bảng Subjects
class subjects(db.Model):
    __tablename__ = 'subjects'
    
    subject_id = db.Column(db.String(10), primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)

    # Quan hệ 1-n với Scores
    scores = db.relationship('Score', back_populates='subject', cascade="all, delete")

    def __repr__(self):
        return f"<Subject {self.subject_id} - {self.subject_name}>"


# Bảng Scores
class scores(db.Model):
    __tablename__ = 'scores'
    
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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