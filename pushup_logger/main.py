from flask import Blueprint, flash, redirect,render_template, request,url_for
from flask_login import login_required, current_user
from . import db 
from . models import User
from . models import Workout
main = Blueprint('main',__name__)




@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name) 

@main.route('/new')
@login_required
def new_workout():

    return render_template('create_workout.html')



@main.route('/new', methods=['POST'])
@login_required
def new_workout_post():

    pushups = request.form.get('pushups')
    comments = request.form.get('comment')

    workout = Workout(pushups=pushups, comment=comments, author=current_user)
    db.session.add(workout)
    db.session.commit()
    flash("Your Workout has been added! ")

    return redirect(url_for('main.user_workouts'))


    

@main.route('/all')
@login_required
def user_workouts():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workouts = user.workouts
    return render_template('all_workouts.html', workouts=workouts, user=user) 
     
@main.route("/workout/<int:workout_id>/update", methods=['GET','POST'])
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        flash("Your workout has been updated!")
        return redirect(url_for('main.user_workouts'))
    return render_template('update_workout.html', workout=workout)

