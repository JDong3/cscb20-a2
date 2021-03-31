import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for, g, current_app

# TODO: hook up database, create db, put data, check login vs database
app = Flask(__name__)

@app.route('/')
def main():
    if 'user' in session:
        return redirect('/index')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # check if username exists
        rows = query('select * from users')
        if request.form['username'] in [row['username'] for row in rows]:
        session['user'] = request.form['username']
        return redirect('/index')
    if request.method == 'GET':
        return render_template('login.html')

def query(q):
    db = get_db()
    cur = db.cursor()
    cur.execute(q)
    return cur.fetchall()

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/<page>')
def pages(page=None):
    if not 'user' in session:
        return redirect('/login')

    if page == 'assignments':
        return render_template('assignments.html')
    elif page == 'index':
        return render_template('index.html')
    elif page == 'calendar':
        return render_template('calendar.html')
    elif page == 'feedback':
        return render_template('feedback.html')
    elif page == 'lectures':
        return render_template('lectures.html')
    elif page == 'tests':
        return render_template('tests.html')
    elif page == 'tutorials':
        return render_template('tutorials.html')

def get_db():
    if not 'db' in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if not db is None:
        db.close()


app.teardown_appcontext(close_db)
app.secret_key = 'applepen'
app.config['DATABASE'] = 'app.db'
