#!/usr/bin/python3
from flask import Flask, render_template, request, g, jsonify, redirect, make_response, render_template_string
import sqlite3, os, sys, requests, hashlib, base64
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, set_access_cookies, 
    set_refresh_cookies, unset_jwt_cookies
)

app = Flask(__name__)
app.database = "sample.db"
app.config['JWT_SECRET_KEY'] = '12345678'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)

def reverse(s):
	s = s.encode('utf-8')
	s = base64.urlsafe_b64encode(s)
	s = s.decode('utf-8')
	return s[::-1]

def connect_db():
    return sqlite3.connect(app.database)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		login = request.form.get('login')
		password = request.form.get('password')
		g.db = connect_db()
		cur = g.db.execute("""SELECT * FROM users WHERE login = ? AND password = ?""", (login,password))
		if cur.fetchone():
			access_token = create_access_token(identity=login)
			refresh_token = create_refresh_token(identity=login)
			response = make_response(redirect('/account'))
			set_access_cookies(response, access_token)
			set_refresh_cookies(response, refresh_token)
			return response
		else:
			login_error = 'Cant login with %s !' % login
			error_login = render_template_string(login_error)
			return render_template('login.html', error = error_login)
		g.db.close()
	return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
	response = make_response(redirect('/'))
	unset_jwt_cookies(response)
	return response

@app.route('/account', methods=['GET','POST'])
@jwt_required()
def account():
	login = get_jwt_identity()
	if login != login:
		return render_template('index.html')
	else:	
		g.db = connect_db()
		curs = g.db.execute("""SELECT balance FROM users WHERE login = ? """, (login,))
		balance = curs.fetchone()
		g.db.close()
		mumble = reverse(login)
		return render_template('account.html', mumble=mumble, login=login, balance=balance)

@app.route('/transfer', methods=['POST','GET'])
@jwt_required()
def transfer():
	login = get_jwt_identity()
	if request.method == 'POST':
		g.db = connect_db()
		balance = request.form.get('balance')
		nickname = request.form.get('nickname')
		notes = request.form.get('notes')
		curs1 = g.db.execute("""UPDATE users SET balance = balance + ? WHERE login = ?""",(balance, nickname))	
		curs2 = g.db.execute("""UPDATE users SET balance = balance - ? WHERE login = ?""",(balance, login))	
		curs3 = g.db.execute("""INSERT INTO history(owner,value,target,notes)  VALUES(?,?,?,?)""",(login, balance, nickname, notes))		
		g.db.commit()
		g.db.close()
		response = make_response(redirect('/account'))
		return response
	return render_template('transfer.html')

@app.route('/history')
@jwt_required()
def history():
	login = get_jwt_identity()
	url = request.args.get('url')
	info = requests.get(url).text
	return render_template('history.html', info=info)

@app.route('/users', methods=['GET','POST'])
@jwt_required()
def users():
	if request.method == 'POST':
		g.db = connect_db()
		user = request.form.get('user')
		curs = g.db.execute("SELECT login FROM users WHERE login = '%s'" % user)
		users = curs.fetchall()
		return render_template('users.html', users=users)
	return render_template('users.html')

@app.route('/registration', methods=['GET','POST'])
def registr():
	if request.method == 'POST':
		g.db = connect_db()
		login = request.form.get('login')
		password = request.form.get('password')
		balance = 1000
		curs = g.db.execute("""INSERT INTO users(login,password,balance) VALUES(?,?,?)""", (login,password,balance))
		g.db.commit()
		g.db.close()
		response = make_response(redirect('/'))
		return response
	else:
		return render_template('registration.html')

if __name__=='__main__':
	try:
		if not os.path.exists(app.database):
			with sqlite3.connect(app.database) as connection:
				c = connection.cursor()
				c.execute("""CREATE TABLE users(login TEXT, password TEXT, balance TEXT)""")
				c.execute("""CREATE TABLE history(owner TEXT, value TEXT, target TEXT, notes TEXT)""")
				connection.commit()
				connection.close()
	except Exception as e:
		print("DATABASE SUCCESFULLY CREATE, RUN AGAIN")
		sys.exit(0)
	app.run(host='0.0.0.0', debug=True, port=8080)