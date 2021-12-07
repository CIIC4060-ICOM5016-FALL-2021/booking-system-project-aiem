from flask import jsonify

from datetime import datetime
from backend.app.model.user import UserDAO
from backend.app.model.meeting import MeetingDAO
from backend.app.model.user_type import UserTypeDAO
from backend.app.controller.level_validation_controller import UserLevelValidationController


class UserController:

    @staticmethod
    def build_user_map_dict(row):
        result = {'us_id': row[0], 'us_name': row[1], 'us_username': row[2],'us_password': row[3], 'ut_id': row[4]}
        return result

    @staticmethod
    def build_user_type_map_dict(row):
        result = {'ut_id': row[0], 'ut_name': row[1], 'ut_isAdmin': row[2], 'ut_level': row[3]}
        return result

    @staticmethod
    def build_user_availability_map_dict(row):
        result = {'uu_id': row[0], 'uu_date': row[1], 'uu_startTime': row[2].strftime("%H:%M:%S"), 'uu_endTime': row[3].strftime("%H:%M:%S"), 'us_id': row[4]}
        return result

    @staticmethod
    def build_user_schedule_map_dict(row):
        result = {'rstart': row[0].strftime("%H:%M:%S"),
                  'rend': row[1].strftime("%H:%M:%S"),
                  'title': row[2],
                  'rdesc': row[3]}
        return result

    @staticmethod
    def build_complete_user_schedule_dict(row):
        result = {'date': row[0].strftime("%Y-%m-%d"),
                  'start': row[1].strftime("%H:%M:%S"),
                  'end': row[2].strftime("%H:%M:%S"),
                  'title': row[3],
                  'desc': row[4],
                  'room': row[5],
                  'creator': row[6],
                  'username': row[7],
                  'mt_id': row[8]}
        return result

    @staticmethod
    def  build_most_booked_user_map_dict(row):
        result = {'us_name': row[0], 'count': row[1]}
        return result

    @staticmethod
    def build_user_most_used_room_map_dict(row):
        result = {'us_name': row[0], 'ro_name': row[1], 'count': row[2]}
        return result

    def update_user(self, us_id, json):
        us_dao = UserDAO()
        user_exists = us_dao.get_user(us_id)
        if user_exists:
            us_dao = UserDAO()
            us_dao.update_user(json['us_name'], json['us_username'], json['us_password'], json['ut_id'], us_id)
            user = (us_id,
                    json['us_name'],
                    json['us_username'],
                    json['us_password'],
                    json['ut_id'])
            us_dict = self.build_user_map_dict(user)
            return jsonify(us_dict), 200
        else:
            return jsonify("No such user"), 404

    def delete_user(self, us_id):
        us_dao = UserDAO()

        # Check that there's no meetings
        mt_dao = MeetingDAO()  # Create a MeetDAO
        cnt = mt_dao.getUserAttendingCount(us_id)  # Get the count
        mt_dao.dispose()  # Dispose the meeting DAO

        if cnt > 0:  # If there are meetings
            return jsonify("USER HAS MEETINGS"), 400  # n o

        result = us_dao.delete_user(us_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def delete_user_unavailability(self, json, session_id):
        us_dao = UserDAO()
        user_exists = us_dao.get_user(json['us_id'])
        if user_exists:
            us_dao = UserDAO()
            if json['us_id'] == session_id:
                result = us_dao.delete_user_unavailability(json['uu_startTime'], json['uu_endTime'], json['us_id'])
                if result:
                    return jsonify("DELETED"), 200
                else:
                    return jsonify("NOT FOUND"), 404
            else:
                return jsonify("User cannot delete a different user's availability"), 403
        else:
            return jsonify("User does not exist"), 404

    def delete_user_unavailability_by_id(self, uu_id, session_id):
        us_dao = UserDAO()
        uv_cont = UserLevelValidationController()
        us_id = uv_cont.get_us_id_from_uu_id(uu_id)
        user_exists = us_dao.get_user(us_id)
        if user_exists:
            uv_cont = UserLevelValidationController()
            us_id = uv_cont.get_us_id_from_uu_id(uu_id)
            print("This is us_id: ", us_id)
            if us_id == session_id:
                us_dao = UserDAO()
                result = us_dao.delete_user_unavailability_by_id(uu_id)
                if result:
                    return jsonify("DELETED"), 200
                else:
                    return jsonify("NOT FOUND"), 404
            else:
                return jsonify("User cannot delete a different user's availability"), 403
        else:
            return jsonify("User does not exist"), 404

    def create_user(self, json):
        u_dao = UserDAO()
        u_id = u_dao.create_user(json['us_name'], json['us_username'], json['us_password'], json['ut_id'])
        user = (u_id,
                json['us_name'],
                json['us_username'],
                json['us_password'],
                json['ut_id'])
        u_dict = self.build_user_map_dict(user)
        return jsonify(u_dict), 201

    def create_user_type(self, json):
        if 4 > json['ut_level'] > 0:
            ut_dao = UserTypeDAO()
            ut_id = ut_dao.create_user_type(json['ut_name'], json['ut_isAdmin'], json['ut_level'])
            user_type = (ut_id,
                         json['ut_name'],
                         json['ut_isAdmin'],
                         json['ut_level'])
            ut_dict = self.build_user_type_map_dict(user_type)
            return jsonify(ut_dict), 201
        else:
            return jsonify("Invalid level number"), 422

    def mark_user_unavailability(self, json, session_id):
        us_dao = UserDAO()
        user_exists = us_dao.get_user(json['us_id'])
        if user_exists:
            us_dao = UserDAO()
            us_id = json['us_id']
            if us_id == session_id:
                uu_id = us_dao.mark_user_unavailability(json['uu_date'], json['uu_startTime'], json['uu_endTime'], json['us_id'])
                unavailability = (uu_id,
                                  datetime.strptime(json["uu_date"], "%Y-%m-%d").date(),
                                  datetime.strptime(json["uu_startTime"], "%H:%M:%S").time(),
                                  datetime.strptime(json["uu_endTime"], "%H:%M:%S").time(),
                                  json['us_id'])
                ua_dict = self.build_user_availability_map_dict(unavailability)
                return jsonify(ua_dict), 201
            else:
                return jsonify("User cannot mark a different user as unavailable"), 403
        else:
            return jsonify("User does not exist"), 404

    def get_user_unavailability(self, us_id):
        us_dao = UserDAO()
        user_exists = us_dao.get_user(us_id)
        if user_exists:
            us_dao = UserDAO()
            user_unavailability_list = us_dao.get_user_unavailability(us_id)
            uu_dict = [self.build_user_availability_map_dict(row) for row in user_unavailability_list]
            return jsonify(uu_dict), 200
        else:
            return jsonify("No such user"), 404

    def get_user_schedule(self, us_id, r_date):
        us_dao = UserDAO()
        user_exists = us_dao.get_user(us_id)
        if user_exists:
            us_dao = UserDAO()
            if r_date is not None:
                user_schedule = us_dao.get_user_schedule(us_id, r_date)
                schedule_dict = [self.build_user_schedule_map_dict(row) for row in user_schedule]
                return jsonify(schedule_dict), 200
            else:
                user_schedule = us_dao.get_complete_user_schedule(us_id)
                schedule_dict = [self.build_complete_user_schedule_dict(row) for row in user_schedule]
                return jsonify(schedule_dict), 200
        else:
            return jsonify("No such user"), 404

    def get_user(self, us_id):
        us_dao = UserDAO()
        user = us_dao.get_user(us_id)
        if not user:
            return jsonify("Not Found"), 404
        else:
            us_dict = self.build_user_map_dict(user)
            return jsonify(us_dict), 200

    def check_user(self, json):
        us_dao = UserDAO()
        user = us_dao.check_user(json['username'], json['password'])
        if user == -1:
            return jsonify("Incorrect username or password"), 400
        else:
            return jsonify(user), 200  # if we had a session manager, this is where we'd generate that

    def get_user_type(self, ut_id):
        ut_dao = UserTypeDAO()
        user_type = ut_dao.get_user_type(ut_id)
        if not user_type:
            return jsonify("Not Found"), 404
        else:
            ut_dict = self.build_user_type_map_dict(user_type)
            return jsonify(ut_dict), 200

    def get_user_level(self, us_id):
        us_dao = UserDAO()
        user_level = us_dao.get_user_level(us_id)
        return user_level

    def get_all_users(self):
        dao = UserDAO()
        user_list = dao.get_all_users()
        users = [self.build_user_map_dict(row) for row in user_list]
        return jsonify(users)

    def get_all_user_types(self):
        dao = UserTypeDAO()
        user_types_list = dao.get_all_user_types()
        user_types = [self.build_user_type_map_dict(row) for row in user_types_list]
        return jsonify(user_types)

    def get_admin_status(self, us_id):
        dao = UserDAO()
        return dao.get_admin_status(us_id)

    def get_most_booked_users(self):
        dao = UserDAO()
        users_list = dao.most_booked_user()
        users = [self.build_most_booked_user_map_dict(row) for row in users_list]
        return jsonify(users)

    def get_user_most_used_room(self, us_id):
        us_dao = UserDAO()
        user_exist = us_dao.get_user(us_id)
        if user_exist:
            dao = UserDAO()
            users_list = dao.most_used_room(us_id)
            users = [self.build_user_most_used_room_map_dict(row) for row in users_list]
            return jsonify(users)
        else:
            return jsonify("Not Found"), 404

    def get_user_most_meeting_with_user(self, us_id):
        us_dao = UserDAO()
        user = us_dao.get_user(us_id)
        if not user:
            return jsonify("Not Found"), 404
        else:
            dao=UserDAO()
            users_list = dao.user_most_meeting_with_user(us_id)
            users = [self.build_most_booked_user_map_dict(row) for row in users_list]
            return jsonify(users)
        
