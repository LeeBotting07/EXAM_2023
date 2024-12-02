from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)

# Routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title="Home")
