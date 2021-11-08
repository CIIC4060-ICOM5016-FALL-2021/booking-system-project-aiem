from flask import jsonify

from app.model.meeting import MeetingDAO

#-Dictionary builders------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Library of functions to be used for any Room operations
def build_meeting_map_dict(row):
    result = {'mt_id': row[0],
              'mt_name': row[1], 
              'mt_desc': row[2],
              're_id': row[3],
              're_date': row[4],
              're_startTime': row[5], 
              're_endTime': row[6],
              'us_id': row[7],
              'us_name': row[8], 
              'ro_id': row[9] }
    return result


def build_user_map_dict(row):
    result = {'us_id':row[0], 'us_name':row[1], 'us_username':row[2]}
    return result

#-Internals------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_all_meetings(self):
    dao = MeetingDAO()
    meeting_list = dao.getAllMeeting()
    meetings = [build_meeting_map_dict(row) for row in meeting_list]
    return jsonify(meetings)

def get_meeting_by_id(self, id):
    dao = MeetingDAO()
    row = dao.getMeetingById(id)
    if not row: return
    meeting = build_meeting_map_dict(row)
    return meeting

def get_all_attending_meeting(self, id):
    dao = MeetingDAO()
    user_list = dao.getMeetingAttending(id)
    users = [build_users_map_dict(row) for row in users_list]
    return jsonify(users)

def get_meetings_for_room_on(self, id, date):
    dao = MeetingDAO()
    meeting_list = dao.getMeetingsForRoomOn(id,date)
    meetings = [build_meeting_map_dict(row) for row in meeting_list]
    return jsonify(meetings)

def get_meetings_for_user_on(self, id, date):
    dao = MeetingDAO()
    meeting_list = dao.getMeetingsForUserOn(id,date)
    meetings = [build_meeting_map_dict(row) for row in meeting_list]
    return jsonify(meetings)

def get_meetings_for_room_during(self, id, date, time):
    dao = MeetingDAO()
    row = dao.getMeetingInRoomAtTime(id,date,time)
    if not row: return
    meeting = build_meeting_map_dict(row)
    return meeting

def check_user_busy(self, id, date, start, end):
    dao = MeetingDAO()
    return dao.checkUserBusy(id,date,start,end)

def check_meeting_busy(self, us_id, ro_id, date, start, end):
    dao = MeetingDAO()
    return dao.checkUserBusy(id,date,start,end)

def create_meeitng(self, name, desc, date, start, end, us_id, ro_id):
    if not check_meeting_busy(us_id,ro_id,date,start,end): 
        return -1
    dao = MeetingDAO()
    return dao.insertEverythingForMeeting(name,desc,date,start,end,us_id,ro_id)

def add_attending(self, mt_id,us_id):
    dao = MeetingDAO()
    return dao.insertAttending(mt_id,us_id)

def update_meeting(self, id, name, description):
    dao = MeetingDAO()
    return dao.updateMeeting(id,name,description)

def update_reservation(self, id,date,start,end):
    dao=MeetingDAO()
    return dao.updateReservation(id,date,start,end)

def remove_attending(self, mt_id,us_id):
    dao=MeetingDAO()
    return dao.deleteAttending(mt_id,us_id)

def remove_meeting(self, mt_id):
    dao=MeetingDAO()
    return dao.deleteMeeting(mt_id)

#-Controller Methods------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#
def GetMeetings(self):
    return get_all_meetings(self),200

#
def GetMeetingByID(self, id):
    meeting = get_meeting_by_id(self, id)
    if not meeting: return "NOT FOUND",404
    return meeting,200

#
def GetAllAttendingMeeting(self, id):
    return get_all_attending_meeting(self, id),200


def GetMeetingsForRoomOn(self, id, date):
    return get_meetings_for_room_on(self, id, date),200 #We don't actually check if the meeting exists but eh its not entirely necessary

def GetMeetingsForUserOn(self, id, date, time):
    return get_meetings_for_user_on(self, id, date),200

def GetMeetingForRoomDuring(self, id, date, time):
    return get_meetings_for_room_during(self, id, date, time),200

#
def CreateMeeting(self, json):
    result = create_meeitng(self, json['name'], json['desc'], json['date'], json['start'], json['end'], json['us_id'], json['ro_id'])
    if result = -1: return "CONFLICT FOUND",400
    return result,200

#
def AddAttending(self, json):
    return add_attending(self, json['mt_id'], json['us_id']),200

#
def UpdateMeeting(self, json):
    return update_meeting(self, json['id'], json['name'], json['desc']),200

#
def UpdateReservation(self, json):
    return update_reservation(self, json['id'], json['date'], json['start'], json['end']),200

#
def RemoveAttending(self, json):
    success = remove_attending(self, json['mt_id'], json['us_id']),200
    if not success: return "NOT FOUND",404
    return success,200

#
def RemoveMeeting(self, id):
    success = remove_meeting(self, id)
    if not success: return "OOPS",500
    return success,200
    