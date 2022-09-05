from flask import render_template, url_for, flash, redirect, request
from app import app, models
from app.forms import LoginForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Users, Students
from werkzeug.urls import url_parse

"""@app.route('/')
#@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('admin/', title="Home")

@app.route('/queries', methods=["GET", "POST"])
@login_required
def queries():
    if request.method == "POST":
        data = dict(request.form)
        student = Student.query.get(data['search'])
        print(student)
    else:
        student = {}
    return render_template('queries.html', title="Queries", student=student)


@app.route('/downloads')
@login_required
def downloads():
    return render_template('downloads.html', title="Downloads")
"""
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))