from flask import render_template, request, jsonify

from backend.app import app


@app.route('/')
def home():
    return render_template("templates/home.html")


"""
                                        ==========
                                        Room Views
                                        ==========
"""


# View all rooms or create a new one
@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'POST':
        return RoomsController().create_room(request.json)
    else:
        return RoomsController().get_all_rooms()


# View all available rooms at given date and time
@app.route('/rooms/available/<int:session_id>')
def rooms_available(session_id):
    #user_level = UserController.get_user_type(UserController.get_user(session_id)['ut_id'])['ut_level']
    print(UserController().get_user_level(session_id))
    return RoomsController().get_available_by_date_and_time(UserController().get_user_level(session_id),
                                                            request.args.get("date"),
                                                            request.args.get("start"),
                                                            request.args.get("end"))


# View/update/delete specific room
@app.route('/rooms/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def rooms_by_id(id):
    if request.method == 'PUT':
        return RoomsController().update_room(id, request.json)
    if request.method == 'DELETE':
        return RoomsController().delete_room(id)
    else:
        return RoomsController().get_room(id)


@app.route('/rooms/<int:id>/schedule')
def rooms_schedule(id):
    return RoomsController().get_room_schedule(id, request.args.get("date"))


@app.route('/rooms/<int:id>/schedule-unavailable', methods=['GET', 'POST'])
def rooms_unavailable_by_room(id):
    if request.method == 'POST':
        admin = UserController().get_admin_status(request.json['us_id'])
        return RoomsController().set_room_unavailability(id, admin, request.json)
    else:
        if request.args:
            return RoomsController().get_room_unavailability(id, request.args.get("date"))
        else:
            return RoomsController().get_room_unavailability(id, None)


@app.route('/rooms/<int:ro_id>/schedule-unavailable/<int:ru_id>', methods=['GET', 'PUT', 'DELETE'])
def rooms_unavailable_by_id(ro_id, ru_id):
    if request.method == 'PUT':
        admin = UserController().get_admin_status(request.json['us_id'])
        return RoomsController().update_room_unavailability(ru_id, ro_id, admin, request.json)
    if request.method == 'DELETE':
        return RoomsController().delete_room_unavailability(ru_id)
    else:
        return RoomsController().get_room_unavailability_by_id(ru_id, ro_id)


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


@app.route('/rooms/most-booked')
def most_booked_rooms():
    return RoomsController().get_most_booked_room()


"""
                                        =============
                                        Meeting Views
                                        =============
"""


@app.route('/meetings', methods=['GET', 'POST'])
def handleMeeting():
    if request.method == 'POST':
        return MeetingController().CreateMeeting(request.json)
    else:
        return MeetingController().GetMeetings()


@app.route('/meetings/<int:id>/<int:session_id>', methods=['GET', 'PUT', 'DELETE'])
def handleMeetingById(id, session_id):
    if request.method == 'GET':
        return MeetingController().GetMeetingByID(id, session_id)
    elif request.method == 'PUT':
        return MeetingController().UpdateMeeting(request.json, session_id)
    elif request.method == 'DELETE':
        return MeetingController().RemoveMeeting(id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/meetings/<int:id>/attending/<int:session_id>', methods=['GET', 'DELETE'])
def handleAttendingById(id, session_id):
    if request.method == 'GET':
        return MeetingController().GetAllAttendingMeeting(id, session_id)
    elif request.method == 'DELETE':
        return MeetingController().RemoveAttending(request.json, session_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/meetings/rooms/<int:id>/<string:d>/<int:session_id>', methods=['GET'])
def handleRoomMeetingSchedule(id, d, session_id):
    if request.method == 'GET':
        return MeetingController().GetMeetingsForRoomOn(id, d, session_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/meetings/rooms/<int:id>/<string:d>/<string:t>/<int:session_id>', methods=['GET'])
def handleRoomMeetingAt(id, d, t, session_id):
    if request.method == 'GET':
        return MeetingController().GetMeetingForRoomDuring(id, d, t, session_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/meetings/users')
def getUserInfoByRoomAndTime():
    return MeetingController().getReserverByTime(request.args.get("room"),
                                                 request.args.get("time"),
                                                 request.args.get("date"))


@app.route('/meetings/users/available', methods=['POST'])
def getDefaultMeetingTime():
    return MeetingController().getAvailableMeetingTime(request.json)


@app.route('/meetings/users/<int:id>/<string:d>', methods=['GET'])
def handleUserMeetingSchedule(id, d):
    if request.method == 'GET':
        return MeetingController().GetMeetingsForUserOn(id, d)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/meetings/busiest')
def busiest_hour():
    result = MeetingController()
    return result.get_busiest_hour()


"""
                                        ==========
                                        User Views
                                        ==========
"""


# @app.route('/user/create-user', methods=['GET', 'POST'])
# def create_new_user():
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
        return UserController().create_user(request.json)
    else:
        return UserController().get_all_users()


@app.route('/Auth', methods=['POST'])
def auth():
    if request.method == 'POST':
        return UserController().check_user(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def users_by_id(id):
    if request.method == 'PUT':
        return UserController().update_user(id, request.json)
    if request.method == 'DELETE':
        return UserController().delete_user(id)
    else:
        return UserController().get_user(id)


@app.route('/users/user-types/<id>', methods=['GET'])
def user_types_by_id(id):
    return UserController().get_user_type(id)


@app.route('/users/user-types', methods=['GET', 'POST'])
def user_types():
    if request.method == 'POST':
        return UserController().create_user_type(request.json)
    else:
        return UserController().get_all_user_types()


@app.route('/users/availability/<int:session_id>', methods=['POST', 'DELETE'])
def user_availability(session_id):
    if request.method == 'POST':
        return UserController().mark_user_unavailability(request.json, session_id)
    if request.method == 'DELETE':
        return UserController().delete_user_unavailability(request.json, session_id)


@app.route('/users/availability/<id>/<int:session_id>', methods=['GET', 'DELETE'])
def user_availability_by_id(id, session_id):
    if request.method == 'DELETE':
        return UserController().delete_user_unavailability_by_id(id, session_id)
    else:
        return UserController().get_user_unavailability(id)


@app.route('/users/<int:id>/schedule')
def user_schedule(id):
    return UserController().get_user_schedule(id, request.args.get("date"))


@app.route('/users/most-booked')
def most_booked_user():
    return UserController().get_most_booked_users()


@app.route('/users/most-rooms/<int:id>')
def most_used_rooms(id):
    return UserController().get_user_most_used_room(id)


@app.route('/users/meetings/<int:id>')
def most_meeting_users(id):
    return UserController().get_user_most_meeting_with_user(id)
