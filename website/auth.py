from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Group, User, Report, User_groups, Tag
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                session["user_id"] = user.id
                return redirect(url_for('report.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/Create_user', methods=['GET', 'POST'])
def Create_user():
    groups = get_all_groups()

    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'), role_id=2)
            db.session.add(new_user)
            db.session.commit()
            for group in request.form.getlist('groups'):
                add_user_groups = User_groups(group_id=group,user_id= new_user.id)
                db.session.add(add_user_groups)
            db.session.commit()

            flash('Account created!', category='success')
            return redirect(url_for('report.home'))

    return render_template("Create_user.html", user=current_user, groups=groups)

@auth.route('/Create_group', methods=['GET', 'POST'])
def Create_group():
    if request.method == 'POST':
        name = request.form.get('groupName')

        group = Group.query.filter_by(name=name).first()
        if group:
            flash('Group already exists.', category='error')
        else:
            new_group = Group(name=name)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created!', category='success')
            return redirect(url_for('report.home'))

    return render_template("Create_group.html", user=current_user)

@auth.route('/create_report', methods=['GET', 'POST'])
def create_report():
    user_groups = [r.Group for r in get_user_groups()]
    print(user_groups)
    tags = get_all_tags()
   
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('Description')
        creator_id = session.get("user_id")
        tag_id = request.form.get('tag')
        group_id = request.form.get('group')


        report = Report.query.filter_by(name=name).first()
        if report:
            flash('Group already exists.', category='error')
        else:
            new_group = Report(name=name,description=description, creator_id=creator_id, tag_id=tag_id, group_id=group_id)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created!', category='success')
            return redirect(url_for('report.home'))

    return render_template("create_report.html", user=current_user, groups= user_groups, tags=tags)

def get_user_groups():
    return (db.session.query(Group, User_groups)
        .filter(User_groups.user_id == session.get("user_id"))
        .filter(User_groups.group_id == Group.id)
        .all())

def get_all_tags():
    return (db.session.query(Tag).all())

def get_all_groups():
    return (db.session.query(Group).all())