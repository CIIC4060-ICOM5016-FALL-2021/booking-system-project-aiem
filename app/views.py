from app import app
from app.db import *
from flask import render_template, request, redirect
import psycopg2


@app.route('/')
def home():
    return render_template("form.html")


#Create a new user in the table
@app.route('/submit-user-info', methods=['POST'])
def create():

    #Setup the DB
    db = Database
    con = db.create_db_connection(db)
    cur = con.cursor()

    #Get info from HTML form
    us_name = request.form['us_name']
    us_username = request.form['us_username']
    us_password = request.form['us_password']

    #Submit the information into the Database
    cur.execute("""INSERT INTO "User"(us_name, us_username, us_password) VALUES(%s, %s, %s)""", (us_name, us_username, us_password))
    con.commit()
    cur.close()
    con.close()

    return redirect("form.html")