from flask import Blueprint
from flask import  render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from models import db,Classroom,Student,Subject

from flask_login import LoginManager, login_required



classroom_bp = Blueprint('classroom_bp', __name__)

@classroom_bp.route('/classrooms')
@login_required
def classrooms():
    all_classrooms = Classroom.query.all()
    return render_template('classrooms.html', classrooms=all_classrooms)

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
    students = Student.query.filter_by(classroom_id=classroom_id).all()
    subjects = Subject.query.filter_by(classroom_id=classroom_id).all()
    return render_template('classroom_details.html', classroom=classroom, students=students, subjects=subjects)
