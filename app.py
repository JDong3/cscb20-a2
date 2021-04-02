import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for, g, current_app

app = Flask(__name__)
SESSION_KEYS = ['login_again', 'login_username', 'login_password',
                'signup_user', 'signup_password_no_match', 'signup_good',
                'signup_username', 'signup_password', 'signup_password_repeat',
                'is_student']
"""
session variables
    login_again: bool
    signup_user_taken: bool, whether the username requested is taken
    signup_password_no_match: bool
    signup_good: bool
    is_student: bool
"""

@app.route('/')
def main():
    if 'user' in session:
        return redirect('/index')
    else:
        return redirect('/login')

@app.route('/trylogin', methods=['POST'])
def login():
    # check if username exists
    authFailed = False
    username = request.form['username']
    password = request.form['password']

    session['login_username'] = username
    session['login_password'] = password

    users = query('select * from users where username = ?', [username])
    if len(users) == 1 and users[0]['password'] == password:
        session['user'] = username
        session['is_student'] = users[0]['type'] == 'student'
        return redirect('/index')
    else:
        print('here')
        session['login_again'] = True
        return main()

@app.route('/trysignup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    password_repeat = request.form['passwordRepeat']
    account_type = request.form['accountType']

    user_taken = query('select * from users where username = ?', [username])
    user_taken = len(user_taken) == 1
    password_no_match = not password == password_repeat
    empty_field = not (username and password and password_repeat)

    session['signup_user_taken'] = user_taken
    session['signup_password_no_match'] = password_no_match
    session['signup_empty_field'] = empty_field
    session['signup_username'] = username
    session['signup_password'] = password
    session['signup_password_repeat'] = password_repeat
    session['signup_account_type'] = account_type

    if user_taken or password_no_match or empty_field:
        session['signup_good'] = False
        return redirect('/signup')
    else:
        session['signup_good'] = True
        insert('insert into users(username, password, type) values (?, ?, ?)', [username, password, account_type])
        return redirect('/signup')

def query(q, param):
    db = get_db()
    cur = db.cursor()
    cur.execute(q, param)
    return cur.fetchall()

def insert(q, param):
    db = get_db()
    cur = db.cursor()
    cur.execute(q, param)
    db.commit()
    return cur.lastrowid

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/login')

@app.route('/<page>')
def router(page=None):
    fix_session()

    if page == 'login':
        return render_template('login.html', **session)
    elif page == 'signup':
        return render_template('signup.html', **session)

    if not 'user' in session:
        return redirect('/login')

    if page == 'assignments':
        return render_template('assignments.html', **session)
    elif page == 'index':
        return render_template('index.html', **session)
    elif page == 'calendar':
        return render_template('calendar.html', **session)
    elif page == 'feedback':
        return render_template('feedback.html', **session)
    elif page == 'lectures':
        return render_template('lectures.html', **session)
    elif page == 'tests':
        return render_template('tests.html', **session)
    elif page == 'tutorials':
        return render_template('tutorials.html', **session)
    elif page == 'signup':
        return render_template('signup.html', **session)
    elif page == 'marks':
        return render_template('marks.html', **session)
    elif page == 'manage' and session['is_student'] == False:
        return render_template('manage.html', **session)
    else:
        return 'What are you doing, please go back.'

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


def fix_session():
    for key in SESSION_KEYS:
        if not key in session:
            session[key] = False

app.teardown_appcontext(close_db)
app.secret_key = 'applepen'
app.config['DATABASE'] = 'app.db'
