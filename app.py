import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import itertools
from geopy.geocoders import Nominatim


app = Flask(__name__)

# Secret key for session management (change this to a secret value in production)
app.secret_key = 'your_secret_key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # Use the correct path to your single SQLite database

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    

class Address(db.Model):
    __tablename__ = 'addresses'  # Associates the Address model with the 'addresses' database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    
with app.app_context():
    db.create_all()

    



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists. <a href="/register">Try again</a>'

        # Hash the password before storing it
        password_hash = generate_password_hash(password)

        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return 'Registration successful. <a href="/login">Log in</a>'
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            # Authentication successful
            session['user_id'] = user.id
            return render_template('home.html')
        else:
            # Authentication failed
            return render_template('login.html')
    
    # This part is for the initial page load (GET request)
    return render_template('login.html')  # Assuming you have a login.html template


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' in session:
            # User is logged in
            return render_template('home.html')
    else:
            # User is not logged in, redirect to the login page
            return render_template('dashboard.html')

def total_distance(tour, distances):
    distance = 0
    for i in range(len(tour) - 1):
        distance += distances[tour[i]][tour[i + 1]]
    distance += distances[tour[-1]][tour[0]]  # Return to the starting city
    return distance


@app.route('/get_route', methods=['GET', 'POST'])
def get_route():
    geolocator = Nominatim(user_agent="my_geocoder")
    locations = []
    addresses = ["710 Laurelwood Dr, Waterloo, Canada", "75 Lucerne Dr, Waterloo, Canada","40 Gail St,Waterloo, Canada"]
    for address in addresses:
        location = geolocator.geocode(address)
        if location:
            locations.append([location.latitude, location.longitude])
    
    print(locations)
    return render_template("route.html", locations=locations)


@app.route('/address_book', methods=['GET', 'POST'])
def address_book():
    addresses = Address.query.all()
    return render_template('address_book.html', addresses=addresses)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    name = ""
    if request.method == 'POST':

        return render_template('thank_you.html')
    return render_template('contact.html')

@app.route('/thank_you', methods=['GET', 'POST'])
def thank_you():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']
            return render_template('thank_you.html')
        return render_template('contact.html')
    
file_path = 'users.db'

@app.route('/')
def index():
    return render_template('dashboard.html')


