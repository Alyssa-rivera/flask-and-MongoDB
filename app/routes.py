import os
from app import app
from flask import render_template, request, redirect, url_for, session # added url_for, session
from bson.objectid import ObjectId # added for page/post

# set some random secret key for session
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/index')

def index():
    collection = mongo.db.events
    events = collection.find({})

    message = ''
    if 'username' in session:
        message = 'You are logged in as ' + session['username'] + '.'

    return render_template('index.html', events = events, message = message)


# Sign up for MongoDB Atlas Account
# in Terminal: pip install flask-pymongo
# in Terminal: pip install dnspython (for +srv)

# Click on cluster name > Collections > Create Database (give database a name, give first collection a name - can be a dummy name)
# Create a user: From Overview, "Add New User" (can autogenerate a password, save the password somewhere)

from flask_pymongo import PyMongo

app.config['MONGO_DBNAME'] = 'test-mongo' # name of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:AtIHE3q3O8HKWBOc@jeffreylancaster-kxrbn.mongodb.net/test-mongo?retryWrites=true' # Command Line Tools, Connect Instructions, Secure Database (Whitelist IP), connection method (Connect Your Application) > Copy > replace password w/ password
# same for node.js > 3.0 and Python > 3.6

mongo = PyMongo(app)

# check for connection? (not sure)

# CONNECT TO DB

@app.route('/add')

def add():
    user = mongo.db.users
    user.insert({'name':'Your Name'})
    return 'Added User!'

# Check collection for new user(s)

# NEW EVENT

@app.route('/events/new', methods=['GET', 'POST'])

def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        user_name = request.form['user_name']
        event_name = request.form['event_name']
        event_date = request.form['event_date']

        events = mongo.db.events
        events.insert({'event': event_name, 'date': event_date, 'user': user_name})
        return redirect('/')


# EVENT PAGE (INDIVIDUAL POST)

@app.route('/events/<eventID>')

def event(eventID):
    collection = mongo.db.events
    event = collection.find_one({'_id' : ObjectId(eventID)})

    return render_template('event.html', event = event)
