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

    grades_dict = {}
    if request.method == 'POST':
        for student in students:
            grade_value = request.form.get(f'grade_{student.id}')
            grade = Grade.query.filter_by(student_id=student.id, subject_id=subject_id, classroom_id=classroom_id).first()
            if not grade:
                grade = Grade(student_id=student.id, subject_id=subject_id, classroom_id=classroom_id, grade_value=grade_value)
                db.session.add(grade)
            else:
                grade.grade_value = grade_value
            db.session.commit()
            grades_dict[student.id] = grade_value
        flash('Grades updated successfully', 'success')
    else:
        for student in students:
            grade = Grade.query.filter_by(student_id=student.id, subject_id=subject_id, classroom_id=classroom_id).first()
            if grade:
                grades_dict[student.id] = grade.grade_value
            else:
                grades_dict[student.id] = 'null'

    return render_template('enter_grades.html', classroom=classroom, subject=subject, students=students, grades_dict=grades_dict)

@grades_bp.route('/user/<int:user_id>/grades')
@login_required
def user_grades(user_id):
    user = User.query.get_or_404(user_id)
    if user.account_type == 'student':
        grades_details = db.session.query(Subject.name, Subject.credit_units, Grade.grade_value)\
                                   .join(Grade, Grade.subject_id == Subject.id)\
                                   .filter(Grade.student_id == user_id)\
                                   .all()
        return render_template('student_grades.html', grades_details=grades_details, user=user)
    else:
        return render_template('access_denied.html', user=user)
