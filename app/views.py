from app import app
from app.model.db import *
from app.controller.rooms_controller import get_all_rooms
from flask import render_template, request, redirect


@app.route('/')
def home():
    return render_template("form.html")

# ****************** ROOM ROUTES ***************************
# Get all rooms in database
@app.route('/rooms/add-room', methods=['POST'])
def create_room():
    return print("Placeholder")

@app.route('/rooms/all-rooms')
def rooms():
    return get_all_rooms()


# **********************************************************

# Create a new user in the table
@app.route('/submit-user-info', methods=['POST'])
def create():
    # Setup the DB
    db = Database()
    con = db.connection
    cur = con.cursor()

    # Get info from HTML form
    us_name = request.form['us_name']
    us_username = request.form['us_username']
    us_password = request.form['us_password']

    # Submit the information into the Database
    # cur.execute("""INSERT INTO "User"(us_name, us_username, us_password) VALUES(%s, %s, %s)""",
    # (us_name, us_username, us_password))
    con.commit()
    cur.close()
    db.close()

    return redirect("form.html")
