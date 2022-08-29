from flask import render_template, url_for, flash, redirect, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Routes for index page"""
    return render_template('index.html', title="Home")

@app.route('/queries')
@login_required
def queries():
    """Routes for queries"""
    return render_template('queries.html', title="Queries")

@app.route('/downloads')
@login_required
def downloads():
    """Routes for downloads page"""
    return render_template('downloads.html', title="Downloads")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))