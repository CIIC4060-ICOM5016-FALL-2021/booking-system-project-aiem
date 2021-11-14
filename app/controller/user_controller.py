from flask import jsonify

from app.model.user import UserDAO
from app.model.user_type import UserTypeDAO


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
        result = {'uu_id': row[0], 'uu_date': row[1], 'uu_startTime': row[2], 'uu_endTime': row[3], 'us_id': row[4]}
        return result

    @staticmethod
    def build_user_schedule_map_dict(row):
        result = {'rstart': row[0].strftime("%H:%M:%S"),
                  'rend': row[1].strftime("%H:%M:%S"),
                  'title': row[2],
                  'rdesc': row[3]}
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
        us_dao.update_user(json['us_name'], json['us_username'], json['us_password'], json['ut_id'], us_id)
        user = (us_id,
                json['us_name'],
                json['us_username'],
                json['us_password'],
                json['ut_id'])
        us_dict = self.build_user_map_dict(user)
        return jsonify(us_dict), 200

    def delete_user(self, us_id):
        us_dao = UserDAO()
        result = us_dao.delete_user(us_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def delete_user_unavailability(self, json):
        us_dao = UserDAO()
        result = us_dao.delete_user_unavailability(json['uu_startTime'], json['uu_endTime'], json['us_id'])
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def delete_user_unavailability_by_id(self, uu_id):
        us_dao = UserDAO()
        result = us_dao.delete_user_unavailability_by_id(uu_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def create_user(self, json):
        u_dao = UserDAO()
        #Old Method
        #ut_dao = UserTypeDAO()
        #ut_dict = build_user_type_dict(ut_dao.get_user_type_by_name(type_name))
        #ut_id = ut_dict.get('ut_id')
        #u_dao.create_user(name, username, password, ut_id)

        u_id = u_dao.create_user(json['us_name'], json['us_username'], json['us_password'], json['ut_id'])
        user = (u_id,
                json['us_name'],
                json['us_username'],
                json['us_password'],
                json['ut_id'])
        u_dict = self.build_user_map_dict(user)
        return jsonify(u_dict), 201

    def create_user_type(self, json):
        ut_dao = UserTypeDAO()
        ut_id = ut_dao.create_user_type(json['ut_name'], json['ut_isAdmin'], json['ut_level'])
        user_type = (ut_id,
                     json['ut_name'],
                     json['ut_isAdmin'],
                     json['ut_level'])
        ut_dict = self.build_user_type_map_dict(user_type)
        return jsonify(ut_dict), 201

    def mark_user_unavailability(self, json):
        us_dao = UserDAO()
        uu_id = us_dao.mark_user_unavailability(json['uu_date'], json['uu_startTime'], json['uu_endTime'], json['us_id'])
        unavailability = (uu_id,
                          json['uu_date'],
                          json['uu_startTime'],
                          json['uu_endTime'],
                          json['us_id'])
        ua_dict = self.build_user_availability_map_dict(unavailability)
        return jsonify(ua_dict), 201

    def get_user_unavailability(self, us_id, uu_date):
        us_dao = UserDAO()
        if uu_date is not None:
            user_unavailability_list = us_dao.get_user_unavailability_date(us_id, uu_date)
            uu_dict = [self.build_user_availability_map_dict(row) for row in user_unavailability_list]
            return jsonify(uu_dict), 200
        else:
            user_unavailability_list = us_dao.get_user_unavailability(us_id)
            uu_dict = [self.build_user_availability_map_dict(row) for row in user_unavailability_list]
            return jsonify(uu_dict), 200

    def get_user_schedule(self, us_id, r_date):
        us_dao = UserDAO()
        user_schedule = us_dao.get_user_schedule(us_id, r_date)
        schedule_dict = [self.build_user_schedule_map_dict(row) for row in user_schedule]
        return jsonify(schedule_dict), 200

    def get_user(self, us_id):
        us_dao = UserDAO()
        user = us_dao.get_user(us_id)
        if not user:
            return jsonify("Not Found"), 404
        else:
            us_dict = self.build_user_map_dict(user)
            return jsonify(us_dict), 200

    def get_user_type(self, ut_id):
        ut_dao = UserTypeDAO()
        user_type = self.build_user_type_map_dict(ut_dao.get_user_type(ut_id))
        return jsonify(user_type)

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

    def get_user_most_used_room(self, us_name):
        dao = UserDAO()
        users_list = dao.most_used_room(us_name)
        users = [self.build_user_most_used_room_map_dict(row) for row in users_list]
        return jsonify(users)

    def get_user_most_meeting_with_user(self, us_name):
        dao = UserDAO()
        users_list = dao.user_most_meeting_with_user(us_name)
        users = [self.build_most_booked_user_map_dict(row) for row in users_list]
        return jsonify(users)