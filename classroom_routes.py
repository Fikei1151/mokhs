from flask import Blueprint
from flask import  render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from models import db,Classroom,Student,Subject,User

from flask_login import LoginManager, login_required



classroom_bp = Blueprint('classroom_bp', __name__)

@classroom_bp.route('/classrooms')
@login_required
def classrooms():
    all_classrooms = Classroom.query.all()
    return render_template('classrooms_all.html', classrooms=all_classrooms)

@classroom_bp.route('/create_classroom', methods=['GET', 'POST'])
@login_required
def create_classroom():
    if request.method == 'POST':
   
        classroom_name = request.form.get('classroom_name')
        year = request.form.get('year')
        new_classroom = Classroom(name=classroom_name, year=year)
        db.session.add(new_classroom)
        db.session.commit()

        return redirect(url_for('classroom_bp.classrooms'))
    
    return render_template('create_classroom.html')
@classroom_bp.route('/edit_classroom/<int:classroom_id>', methods=['GET'])
@login_required
def edit_classroom(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    return render_template('edit_classroom.html', classroom=classroom)

@classroom_bp.route('/update_classroom/<int:classroom_id>', methods=['POST'])
@login_required
def update_classroom(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    classroom.name = request.form['name']
    classroom.year = request.form['year']
    classroom.details = request.form['details']  # Update the details field
    db.session.commit()
    flash('Classroom updated successfully', 'success')
    return redirect(url_for('classroom_bp.classrooms'))


@classroom_bp.route('/delete_classroom/<int:classroom_id>', methods=['POST'])
@login_required
def delete_classroom(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    db.session.delete(classroom)
    db.session.commit()
    flash('Classroom deleted successfully', 'success')
    return redirect(url_for('classroom_bp.classrooms'))

@classroom_bp.route('/classroom_details/<int:classroom_id>')
@login_required
def classroom_details(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    students = db.session.query(User).join(Student, Student.user_id == User.id).filter(Student.classroom_id == classroom_id).all()
    subjects = Subject.query.filter_by(classroom_id=classroom_id).all()
    return render_template('classroom_details.html', classroom=classroom, students=students, subjects=subjects)

@classroom_bp.route('/classroom/<int:classroom_id>/add_student')
@login_required
def add_student(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    students_without_classroom = db.session.query(User).outerjoin(Student, Student.user_id == User.id).filter(User.account_type == 'student', Student.user_id.is_(None)).all()
    return render_template('add_student.html', classroom_id=classroom_id, classroom=classroom, students=students_without_classroom)


@classroom_bp.route('/classroom/<int:classroom_id>/add_student_to_classroom/<int:user_id>', methods=['POST'])
@login_required
def add_student_to_classroom(classroom_id, user_id):

    new_student = Student(user_id=user_id, classroom_id=classroom_id)
    db.session.add(new_student)
    db.session.commit()
    flash('Student added successfully', 'success')
    return redirect(url_for('classroom_bp.classroom_details', classroom_id=classroom_id))

@classroom_bp.route('/classroom/<int:classroom_id>/remove_student/<int:student_id>', methods=['POST'])
@login_required
def remove_student(classroom_id, student_id):
    student_to_remove = Student.query.filter_by(user_id=student_id, classroom_id=classroom_id).first()
    if student_to_remove:
        db.session.delete(student_to_remove)
        db.session.commit()
        flash('Student removed successfully', 'success')
    else:
        flash('Student not found in this classroom', 'danger')
    return redirect(url_for('classroom_bp.classroom_details', classroom_id=classroom_id))


@classroom_bp.route('/classroom/<int:classroom_id>/add_subject', methods=['GET', 'POST'])
@login_required
def add_subject(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    if request.method == 'POST':
        # Process form data and create a new Subject
        name = request.form.get('name')
        credit_units = request.form.get('credit_units')
        description = request.form.get('description')
        new_subject = Subject(name=name, credit_units=credit_units, description=description, classroom_id=classroom_id)
        db.session.add(new_subject)
        db.session.commit()
        flash('Subject added successfully', 'success')
        return redirect(url_for('classroom_bp.classroom_details', classroom_id=classroom_id))
    return render_template('add_subject.html', classroom_id=classroom_id, classroom=classroom)

@classroom_bp.route('/classroom/<int:classroom_id>/remove_subject/<int:subject_id>', methods=['POST'])
@login_required
def remove_subject(classroom_id, subject_id):
    subject_to_remove = Subject.query.filter_by(id=subject_id, classroom_id=classroom_id).first()
    if subject_to_remove:
        db.session.delete(subject_to_remove)
        db.session.commit()
        flash('Subject removed successfully', 'success')
    else:
        flash('Subject not found in this classroom', 'danger')
    return redirect(url_for('classroom_bp.classroom_details', classroom_id=classroom_id))

@classroom_bp.route('/classroom/<int:classroom_id>/subjects')
@login_required
def classroom_subjects(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    subjects = Subject.query.filter_by(classroom_id=classroom_id).all()
    return render_template('classroom_subjects.html', classroom=classroom, subjects=subjects)
