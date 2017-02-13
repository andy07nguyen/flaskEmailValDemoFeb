from flask import Flask, render_template, redirect, request, flash
import re
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "bootsandpants"
mysql = MySQLConnector(app, 'emaildb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if EMAIL_REGEX.match(request.form['email']):
        print "this is a valid email!"
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW());"
        data = {"email":request.form['email']}
        mynewid = mysql.query_db(query, data)

        flash("This is valid! Your email {} is valid!".format(request.form['email']))
        return redirect('/success')
    else:
        print "this is not a valid email!"
        flash("This is not a valid email!")
    return redirect('/')

@app.route('/success')
def success():
    query = "SELECT * FROM emails"
    listofemails = mysql.query_db(query)
    for em in listofemails:
        em['created_at'] = em['created_at'].strftime("%m/%d/%Y %I:%M %p")
    return render_template('success.html', emails = listofemails)

@app.route('/details/<id>')
def details(id):
    print "got the id", id
    query = "SELECT * FROM emails WHERE id = {}".format(id)
    mysql.query_db(query)
    return redirect('/')



















app.run(debug=True)
