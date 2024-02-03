from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db, Grade, Student, Subject,Classroom,User
from flask_login import login_required
grades_bp = Blueprint('grades_bp', __name__, template_folder='templates')

@grades_bp.route('/classroom/<int:classroom_id>/subject/<int:subject_id>/grades', methods=['GET', 'POST'])
@login_required
def enter_grades(classroom_id, subject_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    subject = Subject.query.get_or_404(subject_id)
    students = db.session.query(User).join(Student, Student.user_id == User.id).filter(Student.classroom_id == classroom_id).all()

    if request.method == 'POST':
        # Process form submission and update grades
        for student in students:
            grade_value = request.form.get(f'grade_{student.id}')
            grade = Grade.query.filter_by(student_id=student.id, subject_id=subject_id).first()
            if not grade:
                grade = Grade(student_id=student.id, subject_id=subject_id, grade_value=grade_value)
                db.session.add(grade)
            else:
                grade.grade_value = grade_value
            db.session.commit()
        flash('Grades updated successfully', 'success')
        return redirect(url_for('grades_bp.enter_grades', classroom_id=classroom_id, subject_id=subject_id))

    return render_template('enter_grades.html', classroom=classroom, subject=subject, students=students)
