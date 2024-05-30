from flask import Flask, render_template, redirect, url_for, flash, request, session, g
from werkzeug.utils import secure_filename
import os

from forms import RegistrationForm, LoginForm, DatasetUploadForm
import db

app = Flask(__name__)
app.config.from_object('config.Config')

@app.before_request
def before_request():
    db.connect_db()

@app.teardown_appcontext
def teardown_db(exception):
    db.close_db(exception)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db.insert_user(form.username.data, form.email.data, form.password.data)
        flash('Account created!', 'success')
        # Redirect to dashboard after successful registration
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_email(form.email.data)
        if user and user['password'] == form.password.data:
            session['user_id'] = user['id']
            # Redirect to dashboard after successful login
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    datasets = db.get_datasets_by_user_id(user_id)
    return render_template('dashboard.html', datasets=datasets)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = DatasetUploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(file_path)
        user_id = session['user_id']
        db.insert_dataset(form.name.data, file_path, user_id)
        flash('Dataset uploaded successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('upload.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_tables()
    app.run(debug=True)
