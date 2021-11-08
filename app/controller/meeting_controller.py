from flask import jsonify

from app.model.meeting import MeetingDAO

class MeetingController:
    #-Dictionary builders------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def build_meeting_map_dict(self,row):
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


    def build_user_map_dict(self,row):
        result = {'us_id':row[0], 'us_name':row[1], 'us_username':row[2]}
        return result

    #-Internals------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_all_meetings(self):
        dao = MeetingDAO()
        meeting_list = dao.getAllMeeting()
        meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
        return jsonify(meetings)

    def get_meeting_by_id(self, id):
        dao = MeetingDAO()
        row = dao.getMeetingById(id)
        if not row: return
        meeting = self.build_meeting_map_dict(row)
        return meeting

    def get_all_attending_meeting(self, id):
        dao = MeetingDAO()
        user_list = dao.getMeetingAttending(id)
        users = [self.build_user_map_dict(row) for row in user_list]
        return jsonify(users)

    def get_meetings_for_room_on(self, id, date):
        dao = MeetingDAO()
        meeting_list = dao.getMeetingsForRoomOn(id,date)
        meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
        return jsonify(meetings)

    def get_meetings_for_user_on(self, id, date):
        dao = MeetingDAO()
        meeting_list = dao.getMeetingsForUserOn(id,date)
        meetings = [self.build_meeting_map_dict(row) for row in meeting_list]
        return jsonify(meetings)

    def get_meetings_for_room_during(self, id, date, time):
        dao = MeetingDAO()
        row = dao.getMeetingInRoomAtTime(id,date,time)
        if not row: return
        meeting = self.build_meeting_map_dict(row)
        return meeting

    def check_user_busy(self, id, date, start, end):
        dao = MeetingDAO()
        return dao.checkUserBusy(id,date,start,end)

    def check_meeting_busy(self, us_id, ro_id, date, start, end):
        dao = MeetingDAO()
        return dao.checkUserBusy(id,date,start,end)

    def create_meeitng(self, name, desc, date, start, end, us_id, ro_id):
        if not self.check_meeting_busy(us_id,ro_id,date,start,end):
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
        return dao.updateReservation(self,id,date,start,end)

    def remove_attending(self, mt_id,us_id):
        dao=MeetingDAO()
        return dao.deleteAttending(mt_id,us_id)

    def remove_meeting(self, mt_id):
        dao=MeetingDAO()
        return dao.deleteMeeting(mt_id)

    #-Controller Methods------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #
    def GetMeetings(self):
        return jsonify(self.get_all_meetings()),200

    #
    def GetMeetingByID(self, id):
        meeting = self.get_meeting_by_id(id)
        if not meeting: return "NOT FOUND",404
        return jsonify(meeting),200

    #
    def GetAllAttendingMeeting(self, id):
        return jsonify(self.get_all_attending_meeting(id)),200

    #
    def GetMeetingsForRoomOn(self, id, date):
        return jsonify(self.get_meetings_for_room_on(id, date)),200 #We don't actually check if the meeting exists but eh its not entirely necessary

    #
    def GetMeetingsForUserOn(self, id, date):
        return jsonify(self.get_meetings_for_user_on(id, date)),200

    def GetMeetingForRoomDuring(self, id, date, time):
        return jsonify(self.get_meetings_for_room_during(id, date, time)),200

    #
    def CreateMeeting(self, json):
        result = self.create_meeitng(json['name'], json['desc'], json['date'], json['start'], json['end'], json['us_id'], json['ro_id'])
        if result == -1: return "CONFLICT FOUND",400
        return result,200

    #
    def AddAttending(self, json):
        return self.add_attending(json['mt_id'], json['us_id']),200

    #
    def UpdateMeeting(self, json):
        return self.update_meeting(json['id'], json['name'], json['desc']),200

    #
    def UpdateReservation(self, json):
        return self.update_reservation(json['id'], json['date'], json['start'], json['end']),200

    #
    def RemoveAttending(self, json):
        success = self.remove_attending(json['mt_id'], json['us_id']),200
        if not success: return "NOT FOUND",404
        return success,200

    #
    def RemoveMeeting(self, id):
        success = self.remove_meeting(id)
        if not success: return "OOPS",500
        return success,200
