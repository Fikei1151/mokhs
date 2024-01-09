from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
login_manager = LoginManager(app)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return 'Username already exists'

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, first_name=first_name, last_name=last_name, gender=gender, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        username = request.form.get('username')
        password = request.form.get('password')

        # ตรวจสอบผู้ใช้ในฐานข้อมูล
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # ผู้ใช้ถูกต้อง, จัดการ session ที่นี่
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')


if __name__ == '__main__':
    with app.app_context():
         db.create_all()

    app.run(debug=True,port=8000)
