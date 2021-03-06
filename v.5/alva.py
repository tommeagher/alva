#all the imports
import sqlite3
#for a heavier-duty app, we could use sqlalchemy
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
import local_settings
import re
from datetime import date, datetime

#Link to config settings
ALVA_SETTINGS = 'local_settings.py'

#create our application
app = Flask(__name__)
app.config.from_pyfile('local_settings.py')

#TODO obviously doesn't work
@app.template_filter('dateformat')
def dateformat(value):
    date=datetime.date(value)
    today=date.strftime("%m/%d/%y")
    return value

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
    if hasattr(g, 'db'):
        g.db.close()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

def sluggify(string):
    string = re.sub(r"[^\w]+", " ", string)
    string = "-".join(string.lower().strip().split())
    return string

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, subhed, publishdate, private, id, slug from entries order by id desc')
    entries = [dict(title=row[0], subhed=row[1], publishdate=row[2], private=row[3], id=row[4], slug=row[5]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/colophon')
def colophon():
    return render_template('colophon.html')


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.route('/entries/<slug>.html')
def show_entry(slug):
    entry = query_db('select * from entries where slug=?', [slug], one=True)
    if entry is None:
        abort(404)
    else:
        return render_template('entry.html', entry=entry)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, subhed, publishdate, status, descript, private, slug) values (?, ?, ?, ?, ?, ?, ?)', [request.form['title'], request.form['subhed'], request.form['publishdate'], request.form['status'], request.form['descript'], request.form['private'], sluggify(request.form['title'])])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/edit/<slug>.html')
def entry_edit(slug):
    entry = query_db('select * from entries where slug=?', [slug], one=True)
    if entry is None:
        abort(404)
    else:
        return render_template('edit_entry.html', entry=entry)    
    
@app.route('/edit', methods=['POST'])
def make_edit():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('update entries set title=?, subhed=?, publishdate=?, status=?, descript=?, private=? where slug=?', [request.form['title'], request.form['subhed'], request.form['publishdate'], request.form['status'], request.form['descript'], request.form['private'], request.form['slug']])
    g.db.commit()
    slug=request.form['slug']
    flash('Entry was successfully edited')
    return redirect(url_for('entry_edit', slug=slug))

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
