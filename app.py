from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # ชื่อของ function สำหรับหน้าล็อกอิน
login_manager.init_app(app)

db.init_app(app)


UPLOAD_FOLDER = 'static/userprofile'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html') 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        id_card = request.form.get('id_card')  # รับข้อมูล id_card

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return 'Username already exists'

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, first_name=first_name, last_name=last_name, gender=gender, email=email, password=hashed_password, id_card=id_card)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        id_card = request.form['id_card']
        email = request.form['email']
        # อัปเดตข้อมูลผู้ใช้ที่นี่

        file = request.files['profile_image']
        if file and allowed_file(file.filename):
            # ปรับขนาดและครอปภาพที่นี่
            image = Image.open(file)
            image.thumbnail((200, 200))  # หรือใช้ image.resize((200, 200)) ถ้าต้องการขนาดที่แน่นอน
            new_filename = f"{current_user.id_card}.jpg"  # บันทึกเป็น .jpg
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            image.save(file_path, format='JPEG')  # บันทึกเป็น JPEG

            # อัปเดตรูปภาพโปรไฟล์ในฐานข้อมูล
            current_user.profile_image = new_filename
            db.session.commit()

            flash('Your profile has been updated!', 'success')
            return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit Profile')

if __name__ == '__main__':
    with app.app_context():
         db.create_all()

    app.run(debug=True,port=8000)
