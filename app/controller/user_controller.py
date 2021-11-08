from flask import jsonify

from app.model.user import UserDAO
from app.model.user_type import UserTypeDAO


def build_user_map_dict(row):
    result = {'us_id': row[0], 'us_name': row[1], 'us_username': row[2], 'ut_id': row[4]}
    return result


def build_user_type_dict(row):
    result = {'ut_id': row[0], 'ut_name': row[1], 'ut_isAdmin': row[2], 'ut_level': row[3]}
    return result


def get_all_users():
    dao = UserDAO()
    user_list = dao.get_all_users()
    users = [build_user_map_dict(row) for row in user_list]
    return jsonify(users)


def get_all_room_types():
    dao = UserTypeDAO()
    user_types_list = dao.get_all_user_types()
    user_types = [build_user_type_dict(row) for row in user_types_list]
    return jsonify(user_types)