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
# View all rooms or create a new one
@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'POST':
        return create_room(request.json)
    else:
        return get_all_rooms()

# View/update/delete specific room
@app.route('/rooms/<id>', methods=['GET', 'PUT', 'DELETE'])
def rooms_by_id(id):
    if request.method == 'PUT':
        return update_room(id, request.json)
    if request.method == 'DELETE':
        return "Not ready yet"
    return get_room(id)

# View all room types or create a new one
@app.route('/rooms/room-types', methods=['GET', 'POST'])
def room_types():
    if request.method == 'POST':
        return create_room_type(request.json)
    else:
        return get_all_room_types()

# View/update/delete specific room type
@app.route('/rooms/room-types/<id>', methods=['GET', 'PUT', 'DELETE'])
def room_types_by_id(id):
    if request.method == 'PUT':
        return "Not ready yet"
    if request.method == 'DELETE':
        return "Not ready yet"
    else:
        return get_room_type(id)

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
