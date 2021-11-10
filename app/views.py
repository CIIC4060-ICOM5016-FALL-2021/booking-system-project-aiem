from app import app
from app.model.db import *
from app.controller.rooms_controller import *
from app.controller.meeting_controller import MeetingController
from app.controller.user_controller import *
from flask import render_template, request, redirect


@app.route('/')
def home():
    return render_template("home.html")

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


"""
                                        User Views
"""

=======
#@app.route('/user/create-user', methods=['GET', 'POST'])
#def create_new_user():
#    if request.method == 'GET':
#        return render_template("user_form.html")

#    if request.method == 'POST':
#        us_name = request.form['us_name']
#        us_username = request.form['us_username']
#        us_password = request.form['us_password']
#        ut_level = request.form['ut_level']
#        create_user(us_name, us_username, us_password, ut_level)

#    return redirect("home.html")


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        return create_user(request.json)
    else:
        return get_all_users()


@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def users_by_id(id):
    if request.method == 'PUT':
        return update_user(id, request.json)
    if request.method == 'DELETE':
        return delete_user(id)
    return get_user(id)


@app.route('/users/user-types/<id>', methods=['GET', 'PUT', 'DELETE'])
def user_types_by_id(id):
    if request.method == 'PUT':
        return "UNDER CONSTRUCTION"
    if request.method == 'DELETE':
        return "UNDER CONSTRUCTION"
    else:
        return get_user_type(id)


@app.route('/users/user-types', methods=['GET', 'POST'])
def user_types():
    if request.method == 'POST':
        return create_user_type(request.json)
    else:
        return get_all_user_types()
