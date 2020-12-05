from app import app, db
from app.forms import UploadForm, LoginForm, RegistrationForm
from app.models import User, UploadedFile
from app.helpers import csv_reader, scatterplot, barplot
from flask import render_template, request, redirect, url_for, abort, current_app, flash
import os
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from werkzeug.urls import url_parse
import csv

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return render_template('userindex.html', username=current_user.username)
    return render_template('index.html')


@app.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file_data = form.file.data
        filename = current_user.username + '_' + secure_filename(file_data.filename)
        file_data.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('File uploaded.')
        file_upload = UploadedFile(filename=filename, user_id=current_user.get_id())
        db.session.add(file_upload)
        db.session.commit()
    return render_template('upload.html', form = form)

@app.route('/uploads')
@login_required
def uploads():
    files = UploadedFile.query.filter_by(user_id=current_user.get_id())
    filenames=[]
    for file in files:
        if not file.filename in filenames:
            filenames.append(file.filename)
    return render_template('uploads.html', filenames=filenames)


@app.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    if request.method == "POST":
        filename = request.form.get("filename")
        fields, rows = csv_reader("uploads/" + filename)
        return render_template('analysis.html', fields=fields, rows=rows, filename=filename )
    else:
        return redirect(url_for("uploads"))

@app.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    if request.method == "POST":
        filename = request.form.get("filename")
        fields, rows = csv_reader("uploads/" + filename)
        return render_template('table.html', fields=fields, rows=rows)
    else:
        return redirect(url_for("uploads"))


@app.route('/scatter', methods=['GET', 'POST'])
@login_required
def scatter():
    if request.method == "POST":
        filename = request.form.get("filename")
        xcol = int(request.form.get("selcolx"))
        ycol = int(request.form.get("selcoly"))
        fit = request.form.get("selfit")
        fields, rows = csv_reader("uploads/" + filename)
        try:
            plot_url, coeff = scatterplot(fields, rows, xcol, ycol, fit)
        except ValueError:
            flash("Non-numeric data found")
            flash("Note: Check if your csv file has an extra line if you are sure your data is numeric.")
            return redirect(url_for('analysis'), code=307)
        return render_template('scatter.html', plot_url=plot_url, coeff=coeff)
    else:
        return redirect(url_for("uploads"))

@app.route('/bar', methods=['GET', 'POST'])
@login_required
def bar():
    if request.method == "POST":
        filename = request.form.get("filename")
        xcol = int(request.form.get("selcolx"))
        ycol = int(request.form.get("selcoly"))
        fields, rows = csv_reader("uploads/" + filename)
        try:
            plot_url = barplot(fields, rows, xcol, ycol)
        except ValueError:
            flash("Non-numeric data found in heights")
            flash("Note: Check if your csv file has an extra line if you are sure your data is numeric.")
            return redirect(url_for('analysis'), code=307)
        return render_template('bar.html', plot_url=plot_url)
    else:
        return redirect(url_for("uploads"))

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
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413
