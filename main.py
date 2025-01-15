from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import bcrypt
import datetime

app = Flask(__name__)
app.secret_key = 'your_unique_secret_key_here'

# Routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title="Home")

@app.route('/today')
def today():
    return render_template('today.html', title="Today's Weather")

@app.route('/week')
def week():
    return render_template('week.html', title="This Week's Weather")

@app.route('/about')
def about():
    return render_template('about.html', title="About Us")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title="Login")

@app.route('/customer-login', methods=['GET', 'POST'])
def customer_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if '@admin' in email:
            flash("Admin accounts cannot log in here.", 'error')
            return redirect(url_for('admin_login'))
        
        try:
            with sqlite3.connect("weather.db") as con:
                cur = con.cursor()
                cur.execute("SELECT password, role FROM users WHERE email = ?", (email,))
                data = cur.fetchone()
                if data and bcrypt.check_password_hash(data[0], password):
                    session['email'] = email
                    session['role'] = data[1]
                    cur.execute("UPDATE users SET last_login = ? WHERE email = ?", (datetime.datetime.now(), email))
                    con.commit()
                    return redirect(url_for('account'))
                else:
                    error = "Invalid username or password"
        except sqlite3.Error as e:
            error = f"Database error: {e}"
    return render_template('customer-login.html', title="Customer Login", error=error)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if '@admin' not in email:
            flash("Only admin accounts can log in here.", 'error')
            return redirect(url_for('customer_login'))

        if password != "admin123":
            flash("Incorrect password. Please try again.", 'error')
            return redirect(url_for('admin_login'))

        try:
            with sqlite3.connect("weather.db") as con:
                cur = con.cursor()
                cur.execute("SELECT password, role FROM users WHERE email = ?", (email,))
                data = cur.fetchone()

                if data:
                    hashed_password, role = data
                    if bcrypt.check_password_hash(hashed_password, password) and role == 'admin':
                        session['email'] = email
                        session['role'] = role
                        cur.execute("UPDATE users SET last_login = ? WHERE email = ?", (datetime.datetime.now(), email))
                        con.commit()
                        return redirect(url_for('admin-panel'))
                    else:
                        error = "Invalid email or password"
                else:
                    error = "Invalid email or password"
        except sqlite3.Error as e:
            error = f"Database error: {e}"

    return render_template('admin-login.html', title="Admin Login", error=error)

@app.route('/admin-panel')
def admin_panel():
    return render_template('admin-panel.html', title="Admin Panel")

@app.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            error = "Passwords do not match."
        else:
            try:
                with sqlite3.connect("weather.db") as con:
                    cur = con.cursor()
                    cur.execute("SELECT email FROM users WHERE email = ?", (email,))
                    if cur.fetchone():
                        error = "Email already registered."
                    else:
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cur.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                                    (email, hashed_password, 'admin'))
                        con.commit()
                        flash("Admin account created successfully. Please log in.", 'success')
                        return redirect(url_for('admin_login'))
            except sqlite3.Error as e:
                error = f"Database error: {e}"

    return render_template('admin-register.html', title='Admin Registration', error=error)

@app.route('/customer-register', methods=['GET', 'POST'])
def customer_register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        phone_number = request.form['phoneNumber']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "Passwords do not match."
        else:
            try:
                with sqlite3.connect("weather.db") as con:
                    cur = con.cursor()
                    cur.execute("SELECT email FROM users WHERE email = ?", (email,))
                    if cur.fetchone():
                        error = "Email already registered."
                    else:
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cur.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                                    (email, hashed_password, 'customer'))
                        con.commit()
                        flash("Customer account created successfully. Please log in.", 'success')
                        return redirect(url_for('customer_login'))
            except sqlite3.Error as e:
                error = f"Database error: {e}"

    return render_template('customer-register.html', title='Customer Registration', error=error)

if __name__ == '__main__':
    app.run(debug=True)
