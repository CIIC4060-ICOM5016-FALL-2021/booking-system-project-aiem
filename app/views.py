from app import app
from app.model.db import *
from app.controller.rooms_controller import RoomsController
from app.controller.meeting_controller import MeetingController
from app.controller.user_controller import *
from flask import render_template, request, redirect


@app.route('/')
def home():
    return render_template("home.html")

"""
                                        Room Views
"""
# View all rooms or create a new one
@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'POST':
        return RoomsController().create_room(request.json)
    else:
        return RoomsController().get_all_rooms()

# View/update/delete specific room
@app.route('/rooms/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def rooms_by_id(id):
    if request.method == 'PUT':
        return RoomsController().update_room(id, request.json)
    if request.method == 'DELETE':
        return RoomsController().delete_room(id)
    else:
        return RoomsController().get_room(id)

@app.route('/rooms/<int:id>/schedule-unavailable', methods=['GET', 'POST'])
def rooms_schedule_by_id(id):
    if request.method == 'POST':
        admin = get_admin_status(request.json['us_id'])
        return RoomsController().set_room_unavailability(id, admin, request.json)
    else:
        if request.args:
            return RoomsController().get_room_unavailability(id,request.args.get("date"))
        else:
            return RoomsController().get_room_unavailability(id,None)

# View all room types or create a new one
@app.route('/rooms/room-types', methods=['GET', 'POST'])
def room_types():
    if request.method == 'POST':
        return RoomsController().create_room_type(request.json)
    else:
        return RoomsController().get_all_room_types()

# View/update/delete specific room type
@app.route('/rooms/room-types/<id>')
def room_types_by_id(id):
        return RoomsController().get_room_type(id)


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
