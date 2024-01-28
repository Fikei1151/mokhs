from flask import Blueprint
from flask import  render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from models import db,Classroom

from flask_login import LoginManager, login_user, login_required



classroom_bp = Blueprint('classroom_bp', __name__)

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
    db.session.commit()
    flash('Classroom updated successfully', 'success')
    return redirect(url_for('classrooms'))

@classroom_bp.route('/delete_classroom/<int:classroom_id>', methods=['POST'])
@login_required
def delete_classroom(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    db.session.delete(classroom)
    db.session.commit()
    flash('Classroom deleted successfully', 'success')
    return redirect(url_for('classrooms'))
