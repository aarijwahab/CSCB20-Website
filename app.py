import sqlite3

from flask import Flask, session, escape, redirect, request, render_template, url_for, g

# the database file we are going to communicate with
DATABASE = './assignment3.db'

# connects to the database
def get_db():
    # if there is a database, use it
    db = getattr(g, '_database', None)
    if db is None:
        # otherwise, create a database to use
        db = g._database = sqlite3.connect(DATABASE)
    return db

# converts the tuples from get_db() into dictionaries
# (don't worry if you don't understand this code)
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))

# given a query, executes and returns the result
# (don't worry if you don't understand this code)
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app = Flask(__name__)

app.secret_key=b'b20'

# this function gets called when the Flask app shuts down
# tears down the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # close the database if we are connected to it
        db.close()

@app.route('/')
@app.route('/home')
def index():
	if 'username' in session:
		return render_template("index.html")
	else:
		return redirect(url_for('login'))

@app.route("/assignments")
def assignments():
    return render_template("assignments.html")

@app.route('/announcements')
def announcements():
    return render_template("announcements.html")

@app.route('/calendar')
def calendar():
    return render_template("calendar.html")

@app.route('/tests')
def tests():
    return render_template("tests.html")

@app.route('/labs')
def labs():
    return render_template("labs.html")

@app.route('/discussion')
def discussion():
    return render_template("discussion.html")

@app.route('/lectures')
def lectures():
    return render_template("lectures.html")

@app.route('/feedback')
def feedback():
    return render_template("feedback.html")

@app.route('/resources')
def resources():
    return render_template("resources.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		sql = """
			SELECT *
			FROM login
			"""
		results = query_db(sql, args=(), one=False)
		for result in results:
			if result[0]==request.form['usernameinput'].lower() and result[1] == request.form['passwordinput']:
				session['username']=request.form['usernameinput']
				return redirect(url_for('index'))
		return "Incorrect UserName/Password"
		# session['username']=request.form['usernameinput']
		# return redirect(url_for('index'))
	elif 'username' in session:
		return 'Logged in as %s <a href="/logout">Logout</a>' % escape(session['username'])
	else:
		return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method=='POST':
		user_input = request.form.get('user').lower()
		sql = """
			SELECT *
			FROM login
			"""
		results = query_db(sql, args=(), one=False)
		taken = False
		for result in results:
			if result[0].lower() == user_input:
				return "Username: %s taken" % user_input
				taken = True
		if taken == False:
			get_db().execute("INSERT INTO login VALUES(?)", [user_input])
			get_db().commit()
			get_db().close()
		return redirect(url_for('login'))
	elif 'username' in session:
		return 'Logged in as %s <a href="/logout">Logout</a>' % escape(session['username'])	
	else:
		return render_template("register.html")

@app.route('/registerStudent')
def registerStudent():
    user_input = request.args.get('user').lower()
    pass_input = request.args.get('pass')
    sql = """
		SELECT *
		FROM login
		"""
    results = query_db(sql, args=(), one=False)
    taken = False
    for result in results:
        if result[0].lower() == user_input:
            return "Username: %s taken" % user_input
            taken = True
    if taken == False:
        get_db().execute("INSERT INTO login VALUES(?, ?, ?)", [user_input, pass_input, "student"])
        get_db().commit()
        get_db().close()
    return redirect(url_for('login'))

@app.route('/registerInstructor')
def registerInstructor():
    user_input = request.args.get('user').lower()
    pass_input = request.args.get('pass')
    sql = """
		SELECT *
		FROM login
		"""
    results = query_db(sql, args=(), one=False)
    taken = False
    for result in results:
        if result[0].lower() == user_input:
            return "Username: %s taken" % user_input
            taken = True
    if taken == False:
        get_db().execute("INSERT INTO login VALUES(?, ?, ?)", [user_input, pass_input, "instructor"])
        get_db().commit()
        get_db().close()
    return redirect(url_for('login'))
	# elif 'username' in session:
	# 	return 'Logged in as %s <a href="/logout">Logout</a>' % escape(session['username'])	
	# else:
	# 	return render_template("register.html")


@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
