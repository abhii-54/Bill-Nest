from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # User Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    # Admin Table
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    conn.commit()
    conn.close()

init_db()


# --- ROUTES ---
@app.route('/')
def front():
    return render_template('1st page.html')


# USER REGISTRATION
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                      (name, email, password))
            conn.commit()
            flash("User registered successfully!", "success")
            return redirect(url_for('user_login'))
        except:
            flash("Email already exists!", "danger")
        finally:
            conn.close()

    return render_template('register.html')


# USER LOGIN
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            flash("User login successful!", "success")
            return redirect(url_for('front'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')


# ADMIN REGISTRATION
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO admins (name, email, password) VALUES (?, ?, ?)",
                      (name, email, password))
            conn.commit()
            flash("Admin registered successfully!", "success")
            return redirect(url_for('admin_login'))
        except:
            flash("Email already exists!", "danger")
        finally:
            conn.close()

    return render_template('register_admin.html')


# ADMIN LOGIN
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE email=? AND password=?", (email, password))
        admin = c.fetchone()
        conn.close()

        if admin:
            flash("Admin login successful!", "success")
            return redirect(url_for('front'))
        else:
            flash("Invalid admin credentials!", "danger")

    return render_template('login_admin.html')


if __name__ == '__main__':
    app.run()
