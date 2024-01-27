from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_card = db.Column(db.String(20))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    account_type = db.Column(db.String(50))

    def __repr__(self):
        return '<User %r>' % self.username
    
class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(20))
    subjects = db.relationship('Subject', backref='classroom', lazy=True)
    students = db.relationship('Student', backref='classroom', lazy=True)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credit_units = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    # เพิ่ม fields อื่นๆ ที่ต้องการ
   