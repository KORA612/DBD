import mysql.connector
from flask import g, current_app

def connect_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME']
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_tables():
    with current_app.app_context():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(150) NOT NULL UNIQUE,
                email VARCHAR(150) NOT NULL UNIQUE,
                password VARCHAR(150) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dataset (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                file_path VARCHAR(150) NOT NULL,
                user_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        db.commit()
        cursor.close()

def insert_user(username, email, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO user (username, email, password) VALUES (%s, %s, %s)
    """, (username, email, password))
    db.commit()
    cursor.close()

def get_user_by_email(email):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_user_by_id(user_id):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

def insert_dataset(name, file_path, user_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO dataset (name, file_path, user_id) VALUES (%s, %s, %s)
    """, (name, file_path, user_id))
    db.commit()
    cursor.close()

def get_datasets_by_user_id(user_id):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dataset WHERE user_id = %s", (user_id,))
    datasets = cursor.fetchall()
    cursor.close()
    return datasets
