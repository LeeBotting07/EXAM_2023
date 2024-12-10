from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)


# Routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title="Home")

@app.route('/weather')
def weather():
    return render_template('weather.html', title="Weather")

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

if __name__ == '__main__':
    app.run(debug=True)

