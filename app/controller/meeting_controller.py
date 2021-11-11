import json

from flask import jsonify

from app.model.meeting import MeetingDAO


class MeetingController:
    # Dictionary builders-----------------------------------------------------------------------------------------------

    @staticmethod
    def build_meeting_map_dict(row):
        result = {'mt_id': row[0],
                  'mt_name': row[1],
                  'mt_desc': row[2],
                  're_id': row[3],
                  're_date': row[4].strftime("%Y-%m-%d"),
                  're_startTime': row[5].strftime("%H:%M:%S"),
                  're_endTime': row[6].strftime("%H:%M:%S"),
                  'us_id': row[7],
                  'us_name': row[8],
                  'ro_id': row[9]}
        return result

    @staticmethod
    def build_user_map_dict(row):
        result = {'us_id': row[0],
                  'us_name': row[1],
                  'us_username': row[2]}
        return result

    @staticmethod
    def build_busiest_hour_map_dict(row):
        result = {'re_starTime': row[0].strftime("%H:%M:%S"),
                  're_endTime': row[1].strftime("%H:%M:%S"), 'count': row[2]}
        return result

    # Internals---------------------------------------------------------------------------------------------------------

    def get_all_meetings(self):
        dao = MeetingDAO()
        meeting_list = dao.getAllMeeting()
        meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
        return meetings

    def get_meeting_by_id(self, mt_id):
        dao = MeetingDAO()
        row = dao.getMeetingById(mt_id)
        if not row:
            return
        meeting = self.build_meeting_map_dict(row)
        return meeting

    def get_all_attending_meeting(self, mt_id):
        dao = MeetingDAO()
        user_list = dao.getMeetingAttending(mt_id)
        users = [self.build_user_map_dict(row) for row in user_list]
        return users

    def get_meetings_for_room_on(self, ro_id, date):
        dao = MeetingDAO()
        meeting_list = dao.getMeetingsForRoomOn(ro_id, date)
        meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
        return meetings

    def get_meetings_for_user_on(self, us_id, date):
        dao = MeetingDAO()
        meeting_list = dao.getMeetingsForUserOn(us_id, date)
        meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
        return meetings

    def get_meetings_for_room_during(self, ro_id, date, time):
        dao = MeetingDAO()
        row = dao.getMeetingInRoomAtTime(ro_id, date, time)
        if not row:
            return
        meeting = self.build_meeting_map_dict(row)
        return meeting

    def check_user_busy(self, us_id, date, start, end):
        dao = MeetingDAO()
        return dao.checkUserBusy(us_id, date, start, end)

    def check_meeting_busy(self, us_id, ro_id, date, start, end):
        dao = MeetingDAO()
        return dao.checkMeetingBusy(us_id, ro_id, date, start, end)

    def create_meeting(self, name, desc, date, start, end, us_id, ro_id):
        if self.check_meeting_busy(us_id, ro_id, date, start, end):
            return -1
        dao = MeetingDAO()
        return dao.insertEverythingForMeeting(name, desc, date, start, end, us_id, ro_id)

    def add_attending(self, mt_id, us_id):
        meeting = self.get_meeting_by_id(mt_id)
        if not meeting:
            return jsonify("MEETING NOT FOUND"), 404
        if self.check_user_busy(us_id, meeting["re_date"], meeting["re_startTime"], meeting["re_endTime"]):
            return jsonify("USER IS BUSY"), 400
        dao = MeetingDAO()
        return jsonify(dao.insertAttending(mt_id, us_id)), 201

    def update_meeting(self, mt_id, name, description):
        dao = MeetingDAO()
        return dao.updateMeeting(mt_id, name, description)

    def update_reservation(self, re_id, date, start, end):
        dao = MeetingDAO()
        return dao.updateReservation(self, re_id, date, start, end)

    def remove_attending(self, mt_id, us_id):
        dao = MeetingDAO()
        return dao.deleteAttending(mt_id, us_id)

    def remove_meeting(self, mt_id):
        dao = MeetingDAO()
        return dao.deleteMeeting(mt_id)

    # Controller Methods------------------------------------------------------------------------------------------------

    #
    def GetMeetings(self):
        return jsonify(self.get_all_meetings()), 200

    #
    def GetMeetingByID(self, mt_id):
        meeting = self.get_meeting_by_id(mt_id)
        if not meeting:
            return "NOT FOUND", 404
        return jsonify(meeting), 200

    #
    def GetAllAttendingMeeting(self, mt_id):
        return jsonify(self.get_all_attending_meeting(mt_id)), 200

    #
    def GetMeetingsForRoomOn(self, ro_id, date):
        # We don't actually check if the meeting exists but eh its not entirely necessary
        return jsonify(self.get_meetings_for_room_on(ro_id, date)), 200

    #
    def GetMeetingsForUserOn(self, us_id, date):
        return jsonify(self.get_meetings_for_user_on(us_id, date)), 200

    def GetMeetingForRoomDuring(self, ro_id, date, time):
        return jsonify(self.get_meetings_for_room_during(ro_id, date, time)), 200

    #
    def CreateMeeting(self, json):
        result = self.create_meeting(json['name'], json['desc'], json['date'], json['start'], json['end'],
                                     json['us_id'], json['ro_id'])
        if result == -1:
            return "CONFLICT FOUND", 400
        return jsonify(result), 200

    #
    def AddAttending(self, json):
        return self.add_attending(json['mt_id'], json['us_id'])  # Because Add Attending has 3 possibilities it handles
                                                                 # its own JSON and code generation.

    #
    def UpdateMeeting(self, json):
        return jsonify(self.update_meeting(json['id'], json['name'], json['desc'])), 200

    #
    def UpdateReservation(self, json):
        return jsonify(self.update_reservation(json['id'], json['date'], json['start'], json['end'])), 200

    #
    def RemoveAttending(self, json):
        success = self.remove_attending(json['mt_id'], json['us_id']), 200
        if not success:
            return jsonify("NOT FOUND"), 404
        return jsonify(success), 200

    #
    def RemoveMeeting(self, mt_id):
        success = self.remove_meeting(mt_id)
        if not success:
            return jsonify("OOPS"), 500
        return jsonify(success), 200

    #
    def get_busiest_hour(self):
        dao = MeetingDAO()
        meeting_list = dao.busiest_hour()
        for row in meeting_list:
            build = self.build_busiest_hour_map_dict(row)
            meeting = [build for row in meeting_list]
        return jsonify(meeting)