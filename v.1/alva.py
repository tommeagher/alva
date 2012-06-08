#all the imports
import sqlite3
#for a heavier-duty app, we could use sqlalchemy
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
import local_settings
import re
from flaskext.babel import Babel
from flaskext.babel import format_date

#Link to config settings
#ALVA_SETTINGS = 'local_settings.py'

#create our application
app = Flask(__name__)
app.config.from_pyfile('local_settings.py')
babel = Babel(app)

#connect to db
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
        
#initialize the db
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())  
        db.commit()
        
#create db connections for functions
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def sluggify(string):
    string = re.sub(r"[^\w]+", " ", string)
    string = "-".join(string.lower().strip().split())
    return string

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text, publishdate, status, notes, private, id, slug from entries order by id desc')
#TODO - fix date
#    fixdate = format_date('publishdate')
    entries = [dict(title=row[0], text=row[1], publishdate=row[2], status=row[3], notes=row[4], private=row[5], id=row[6], slug=row[7]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

#create post
#@app.route('/')
#def show_entries():
#    cur = g.db.execute('select title, text, publishdate, status, notes, private, id from entries order by id desc')
#TODO - fix date
#    fixdate = format_date('publishdate')
#    entries = [dict(title=row[0], text=row[1], publishdate=row[2], status=row[3], notes=row[4], private=row[5], id=row[6]) for row in cur.fetchall()]
#    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text, publishdate, status, notes, private, slug) values (?, ?, ?, ?, ?, ?, ?)', [request.form['title'], request.form['text'], request.form['publish'], request.form['status'], request.form['notes'], request.form['private'], sluggify(request.form['title'])])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    
#fire up development server as a standalone application
if __name__ == '__main__':
    app.run()