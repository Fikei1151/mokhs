from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db, Grade, Student, Subject 

grades_bp = Blueprint('grades_bp', __name__, template_folder='templates')

@grades_bp.route('/classroom/<int:classroom_id>/subject/<int:subject_id>/add_grade', methods=['GET', 'POST'])
def add_grade(classroom_id, subject_id):
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        grade_value = request.form.get('grade_value')
        new_grade = Grade(student_id=student_id, subject_id=subject_id, grade_value=grade_value)
        db.session.add(new_grade)
        db.session.commit()
        flash('Grade added successfully', 'success')
        return redirect(url_for('grades_bp.view_grades', classroom_id=classroom_id, subject_id=subject_id))
   
