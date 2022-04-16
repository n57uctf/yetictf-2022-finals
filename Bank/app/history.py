#!/usr/bin/python3
from flask import Flask, render_template, request, g, jsonify, redirect, make_response
import sqlite3, os, base64

app = Flask(__name__)
app.database = "sample.db"

def deverse(s):
	s = s[::-1]
	s = base64.urlsafe_b64decode(s)
	return s.decode('utf-8')

def connect_db():
    return sqlite3.connect(app.database)

@app.route('/<owner>', methods=['GET'])
def search(owner):
    g.db = connect_db()
    tumble = deverse(owner)
    curs = g.db.execute("SELECT * FROM history WHERE owner = '%s'" % tumble) 
    results = [dict(owner=row[0], balance=row[1], target=row[2], notes=row[3]) for row in curs.fetchall()]
    g.db.close()
    return jsonify(results)

if __name__=='__main__':
    app.run(host='127.0.0.1', port=8081)