
from flask import Flask, redirect, url_for, render_template, session, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=15)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20))
    email = db.Column('email', db.String(50))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('user'))
    else:
        if request.method == 'POST':
            user = request.form['username']
            session['user'] = user
            found_user = users.query.filter_by(name=user).first()
            if found_user:
                email = found_user.email
                session['email'] = email
                flash('Logged in successfully')
                return redirect(url_for('user'))
            else:
                usr = users(user, '')
                db.session.add(usr)
                db.session.commit()
                flash('Logged in successfully')
                return redirect(url_for('user'))
        else:
            return render_template('login.html')

@app.route('/user/',  methods=['POST', 'GET'])
def user():
    email = ''
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash('Email was saved')
        else:
            if 'email' in session:
                email = session['email']
        return render_template('user.html', user=user, email=email)
    else:
        flash('You are not logged in')
        return redirect(url_for('login'))

@app.route('/view/')
def view():
    return render_template('view.html', values=users.query.filter_by().all())

@app.route('/logout/')
def logout():
    if 'user' in session:
        flash('You have been logged out')
        session.pop('user', None)
        session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)