from flask import Flask, render_template, redirect, url_for, flash, request, session, g, send_from_directory
from werkzeug.utils import secure_filename
import os
import pandas as pd
from forms import RegistrationForm, LoginForm, DatasetUploadForm
import db
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

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
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_email(form.email.data)
        if user and user['password'] == form.password.data:
            session['user_id'] = user['id']
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

@app.route('/select_features/<int:dataset_id>', methods=['GET', 'POST'])
def select_features(dataset_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    dataset = db.get_dataset_by_id(dataset_id)
    if dataset:
        df = pd.read_csv(dataset['file_path'])
        features = df.columns.tolist()
        if request.method == 'POST':
            x_feature = request.form['x_feature']
            y_feature = request.form['y_feature']
            plot_choice = request.form['plot_choice']
            return redirect(url_for('plot_result', dataset_id=dataset_id, x_feature=x_feature, y_feature=y_feature, plot_choice=plot_choice))
        return render_template('select_features.html', features=features, dataset_id=dataset_id)
    flash('Dataset not found', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/plot_result/<int:dataset_id>', methods=['GET'])
def plot_result(dataset_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    dataset = db.get_dataset_by_id(dataset_id)
    if dataset:
        df = pd.read_csv(dataset['file_path'])
        x_feature = request.args['x_feature']
        y_feature = request.args['y_feature']
        plot_choice = request.args['plot_choice']
        plot_filename = plot_features(df, x_feature, y_feature, plot_choice, dataset['file_path'])
        return render_template('plot_result.html', plot_url=url_for('static', filename=plot_filename))
    flash('Dataset not found', 'danger')
    return redirect(url_for('dashboard'))

def adjust_tick_labels(ax):
    """Adjust the distance between tick labels."""
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10))

def plot_features(df, x_feature, y_feature, plot_choice, file_path):
    """Plot the chosen features using the specified plot type."""
    sns.set_theme(style="whitegrid")
    sns.set_palette("muted")
    
    plt.figure(figsize=(10, 6))
    if plot_choice == '1':
        ax = sns.scatterplot(data=df, x=x_feature, y=y_feature)
        plt.title(f'Scatter Plot of {x_feature} vs {y_feature}')
    elif plot_choice == '2':
        ax = sns.lineplot(data=df, x=x_feature, y=y_feature)
        plt.title(f'Line Plot of {x_feature} vs {y_feature}')
    elif plot_choice == '3':
        plt.figure(figsize=(14, 6))
        plt.subplot(1, 2, 1)
        ax1 = sns.histplot(df[x_feature], kde=True)
        plt.title(f'Histogram of {x_feature}')
        adjust_tick_labels(ax1)
        plt.subplot(1, 2, 2)
        ax2 = sns.histplot(df[y_feature], kde=True)
        plt.title(f'Histogram of {y_feature}')
        adjust_tick_labels(ax2)
        return
    elif plot_choice == '4':
        plt.figure(figsize=(14, 6))
        plt.subplot(1, 2, 1)
        ax1 = sns.boxplot(y=df[x_feature])
        plt.title(f'Box Plot of {x_feature}')
        adjust_tick_labels(ax1)
        plt.subplot(1, 2, 2)
        ax2 = sns.boxplot(y=df[y_feature])
        plt.title(f'Box Plot of {y_feature}')
        adjust_tick_labels(ax2)
        return
    elif plot_choice == '5':
        ax = sns.pairplot(df[[x_feature, y_feature]])
        plt.title(f'Pair Plot of {x_feature} and {y_feature}')
    
    adjust_tick_labels(ax)
    plt.xlabel(x_feature)
    plt.ylabel(y_feature)
    
    # Save the plot as an image file in the 'results/' directory
    if not os.path.exists(app.config['RESULT_FOLDER']):
        os.makedirs(app.config['RESULT_FOLDER'])
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plot_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{x_feature}_vs_{y_feature}_{plot_choice}_{timestamp}.png"
    plot_path = os.path.join(app.config['RESULT_FOLDER'], plot_filename)
    plt.savefig(plot_path)
    plt.close()
    return os.path.join('results', plot_filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_tables()
    app.run(debug=True)
