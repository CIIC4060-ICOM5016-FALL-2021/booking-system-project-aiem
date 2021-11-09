from app import app
from app.model.db import *
from app.controller.rooms_controller import *
from flask import render_template, request, redirect


@app.route('/')
def home():
    return render_template("form.html")

"""
                                        Room Views
"""
# Get all rooms
@app.route('/rooms')
def Vrooms():
    return get_all_rooms()

@app.route('/rooms/<id>')
def Vroom_by_id(id):
    return get_room(id)

# Requires further development to implement create/update at once
@app.route('/rooms/update', methods=['GET', 'POST'])
def Vupdate_room():
    if request.method == 'GET':
        return render_template("room_form.html")

    if request.method == 'POST':
        name = request.form['ro_name']
        location = request.form['ro_location']
        type = request.form['rt_name']
        room_id = request.form['ro_id']
        update_room(name, location, type, room_id)

# View all room types or create a new one
@app.route('/rooms/room-types', methods=['GET', 'POST'])
def Vroom_types():
    if request.method == 'POST':
        return create_room_type(request.json)
    else:
        return get_all_room_types()

# View/update/delete specific room type
@app.route('/rooms/room-types/<name>')
def Vroom_type_by_name(name):
    return get_room_type_by_name(name)

# @app.route('/rooms/create-type', methods=['GET', 'POST'])
# def Vcreate_room_type():
#     if request.method == 'GET':
#         return render_template("room_type_form.html")
#
#     if request.method == 'POST':
#         name = request.form['rt_name']
#         level = request.form['rt_level']
#         create_room_type(name, level)

"""
                                        User Views
"""
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
