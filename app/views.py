from app import app
from app.model.db import *
from app.controller.rooms_controller import *
from app.controller.meeting_controller import MeetingController
from flask import render_template, request, redirect


@app.route('/')
def home():
    return render_template("form.html")

"""
                                        Room Views
"""
# Get all rooms
@app.route('/rooms')
def rooms():
    return get_all_rooms()

@app.route('/rooms/room-types')
def room_types():
    return get_all_room_types()

@app.route('/rooms/room-types/<name>')
def type_by_name(name):
    return get_room_type_by_name(name)

@app.route('/rooms/create-type', methods=['GET', 'POST'])
def create_type():
    if request.method == 'GET':
        return render_template("room_type_form.html")

    if request.method == 'POST':
        name = request.form['rt_name']
        level = request.form['rt_level']
        create_room_type(name, level)

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

"""
                                        Meeting Views
"""

@app.route('/meetings', methods=['GET', 'POST'])
def handleMeeting():
    if request.method == 'POST':
        return MeetingController().CreateMeeting(request.json)
    else:
        return MeetingController().GetMeetings()

@app.route('/meetings/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleMeetingById(id):
    if request.method == 'GET':
        return MeetingController().GetMeetingByID(id)
    elif  request.method == 'PUT':
        return MeetingController().UpdateMeeting(request.json)
    elif request.method == 'DELETE':
        return MeetingController().RemoveMeeting(id)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/meetings/<int:id>/reservation', methods=['PUT'])
def handleReservationUpdate(id):
    if request.method == 'PUT':
        return MeetingController().UpdateReservation(request.json)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/meetings/<int:id>/attending', methods=['GET', 'POST', 'DELETE'])
def handleAttendingById(id):
    if request.method == 'GET':
        return MeetingController().GetAllAttendingMeeting(id)
    elif  request.method == 'POST':
        return MeetingController().AddAttending(request.json)
    elif request.method == 'DELETE':
        return MeetingController().RemoveAttending(request.json)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/meetings/rooms/<int:id>/<string:d>', methods=['GET'])
def handleRoomMeetingSchedule(id,d):
    if request.method == 'GET':
        return MeetingController().GetMeetingsForRoomOn(id,d)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/meetings/rooms/<int:id>/<string:d>/<string:t>', methods=['GET'])
def handleRoomMeetingAt(id,d,t):
    if request.method == 'GET':
        return MeetingController().GetMeetingForRoomDuring(id,d,t)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/meetings/users/<int:id>/<string:d>', methods=['GET'])
def handleUserMeetingSchedule(id,d):
    if request.method == 'GET':
        return MeetingController().GetMeetingsForUserOn(id,d)
    else:
        return jsonify("Method Not Allowed"), 405
