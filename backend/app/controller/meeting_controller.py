from flask import jsonify

from backend.app.model.meeting import MeetingDAO
from backend.app.controller.level_validation_controller import *

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

    @staticmethod
    def build_available_meeting_time_dict(row):
        result = {'start_time': row[0].strftime("%H:%M:%S"),
                  'end_time': row[1].strftime("%H:%M:%S")}
        return result

    # Init--------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.dao = MeetingDAO()

    # Internals---------------------------------------------------------------------------------------------------------

    # This will kinda be like an Admin Function?
    def get_all_meetings(self):
        meeting_list = self.dao.getAllMeeting()
        meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
        return meetings

    # A USER THAT IS AN ATENDEE CAN DO THIS - Done
    def get_meeting_by_id(self, mt_id, session_id):
        attending = UserLevelValidationController().validate_attendee(session_id, mt_id)

        if attending:
            row = self.dao.getMeetingById(mt_id)
            if not row:
                return
            meeting = self.build_meeting_map_dict(row)
            return meeting
        else:
            return "User is not attending this meeting.", 403

    # AN ATENDEE CAN DO THIS - Done
    def get_all_attending_meeting(self, mt_id, session_id):
        attending = UserLevelValidationController().validate_attendee(session_id, mt_id)

        if attending:
            user_list = self.dao.getMeetingAttending(mt_id)
            users = [self.build_user_map_dict(row) for row in user_list]
            return users
        else:
            return "User is not attending this meeting.", 403

    # ONLY SOMEONE WHO MEETS ROOM REQUIREMENTS CAN DO THIS - DONE
    def get_meetings_for_room_on(self, ro_id, date, session_id):
        validate = UserLevelValidationController().validate_permission_to_create(session_id, ro_id)

        if validate:
            meeting_list = self.dao.getMeetingsForRoomOn(ro_id, date)
            meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
            return meetings
        else:
            return "User does not have permission for this room", 403

    # This will kinda be like an Admin Function?
    def get_meetings_for_user_on(self, us_id, date):
        meeting_list = self.dao.getMeetingsForUserOn(us_id, date)
        meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
        return meetings

    # ONLY SOMEONE WHO MEETS ROOM REQUIREMENTS CAN DO THIS - DONE
    def get_meetings_for_room_during(self, ro_id, date, time, session_id):
        validate = UserLevelValidationController().validate_permission_to_create(session_id, ro_id)

        if validate:
            row = self.dao.getMeetingInRoomAtTime(ro_id, date, time)
            if not row:
                return
            meeting = self.build_meeting_map_dict(row)
            return meeting
        else:
            return "User does not have permission for this room", 403

    # This will kinda be like an Admin Function?
    def check_user_busy(self, us_id, date, start, end):
        return self.dao.checkUserBusy(us_id, date, start, end)

    # This will kinda be like an Admin Function?
    def check_meeting_busy(self, attendees, ro_id, date, start, end):
        return self.dao.checkMeetingBusy(attendees, ro_id, date, start, end)

    # ONLY A USER THAT MEETS ROOM LEVEL CAN DO THIS - DONE
    def create_meeting(self, name, desc, date, start, end, us_id, ro_id, attendees):
        validate = UserLevelValidationController().validate_permission_to_create(us_id, ro_id)
        if validate:
            conflicts = self.check_meeting_busy(attendees, ro_id, date, start, end)
            if conflicts >= 1:
                return jsonify(conflicts + " Conflict(s) Found"), 400
            return jsonify(
                self.dao.insertEverythingForMeeting(name, desc, date, start, end, us_id, ro_id, attendees)), 201
        else:
            return jsonify("User does not have permission for this room"), 403

    # ONLY OWNER CAN DO THIS - DONE
    def update_meeting(self, mt_id, name, description, session_id):
        ownership = UserLevelValidationController().validate_owner_through_mt_id(session_id, mt_id)
        if ownership:
            return self.dao.updateMeeting(mt_id, name, description)
        else:
            return "User is not creator of the meeting. Cannot modify", 403

    # ONLY OWNER CAN DO THIS TO OTHER PEOPLE, UNLESS YOU WANT TO REMOVE YOURSELF - DONE
    def remove_attending(self, mt_id, us_id, session_id):
        ownership = UserLevelValidationController().validate_owner_through_mt_id(session_id, mt_id)

        if ownership or (us_id == session_id):
            return self.dao.deleteAttending(mt_id, us_id)
        else:
            return "User is not creator of this meeting, or non-creator user is trying to remove another user", 403

    def remove_meeting(self, mt_id):
        return self.dao.deleteMeeting(mt_id)

    # Controller Methods------------------------------------------------------------------------------------------------

    #
    def GetMeetings(self):
        result = self.get_all_meetings()
        self.dao.dispose()
        return jsonify(result), 200

    #
    def GetMeetingByID(self, mt_id, session_id):
        meeting = self.get_meeting_by_id(mt_id, session_id)
        self.dao.dispose()
        if not meeting:
            return "NOT FOUND", 404
        return jsonify(meeting), 200

    #
    def GetAllAttendingMeeting(self, mt_id, session_id):
        result = self.get_all_attending_meeting(mt_id, session_id)
        self.dao.dispose()
        return jsonify(result), 200

    #
    def GetMeetingsForRoomOn(self, ro_id, date, session_id):
        # We don't actually check if the meeting exists but eh its not entirely necessary
        result = self.get_meetings_for_room_on(ro_id, date, session_id)
        self.dao.dispose()
        return jsonify(result), 200

    #
    def GetMeetingsForUserOn(self, us_id, date):
        result = self.get_meetings_for_user_on(us_id, date)
        self.dao.dispose()
        return jsonify(result), 200

    def GetMeetingForRoomDuring(self, ro_id, date, time, session_id):
        result = self.get_meetings_for_room_during(ro_id, date, time, session_id)
        self.dao.dispose()
        return jsonify(result), 200

    #
    def CreateMeeting(self, json):
        # NOTE! ATTENDEES *MUST* INCLUDE THE RESERVING PARTY
        result = self.create_meeting(json['name'], json['desc'], json['date'], json['start'], json['end'],
                                     json['us_id'], json['ro_id'], tuple(json['attendees']))
        self.dao.dispose()
        return result  # Crete Meeting now handles this

    #
    def UpdateMeeting(self, json, us_id):
        result = self.update_meeting(json['id'], json['name'], json['desc'], us_id)
        self.dao.dispose()
        return jsonify(result), 200

    #
    def RemoveAttending(self, json, session_id):
        success = self.remove_attending(json['mt_id'], json['us_id'], session_id), 200
        self.dao.dispose()
        if not success:
            return jsonify("NOT FOUND"), 404
        return jsonify(success), 200

    #
    def RemoveMeeting(self, mt_id):
        success = self.remove_meeting(mt_id)
        self.dao.dispose()
        if not success:
            return jsonify("OOPS"), 500
        return jsonify(success), 200

    def getAvailableMeetingTime(self, json):
        time_slots = self.dao.get_available_time_attendees(json['date'],
                                                           tuple(json['attendees']))
        time_slot_dict = [self.build_available_meeting_time_dict(time_slot) for time_slot in time_slots]
        self.dao.dispose()
        return jsonify(time_slot_dict), 200

    def getReserverByTime(self, ro_id, start_time, date):
        reserver = self.dao.get_reserver_by_time(ro_id, start_time, date)
        self.dao.dispose()
        if reserver:
            return jsonify(self.build_user_map_dict(reserver)), 200
        else:
            return jsonify("Room not booked at this time"), 404

    def get_busiest_hour(self):
        meeting_list = self.dao.busiest_hour()
        meeting = [self.build_busiest_hour_map_dict(row) for row in meeting_list]
        self.dao.dispose()
        return jsonify(meeting)
