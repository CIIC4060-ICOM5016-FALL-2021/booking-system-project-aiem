from flask import jsonify

from app.model.user import UserDAO
from app.model.user_type import UserTypeDAO


def build_user_map_dict(row):
    result = {'us_id': row[0], 'us_name': row[1], 'us_username': row[2],'us_password': row[3], 'ut_id': row[4]}
    return result


def build_user_type_map_dict(row):
    result = {'ut_id': row[0], 'ut_name': row[1], 'ut_isAdmin': row[2], 'ut_level': row[3]}
    return result


def update_user(us_id, json):
    us_dao = UserDAO()
    us_dao.update_user(json['us_name'], json['us_username'], json['us_password'], json['ut_id'], us_id)
    user = (us_id,
            json['us_name'],
            json['us_username'],
            json['us_password'],
            json['ut_id'])
    us_dict = build_user_map_dict(user)
    return jsonify(us_dict), 200


def delete_user(us_id):
    us_dao = UserDAO()
    result = us_dao.delete_user(us_id)
    if result:
        return jsonify("DELETED"), 200
    else:
        return jsonify("NOT FOUND"), 404


def create_user(json):
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
    u_dict = build_user_map_dict(user)
    return jsonify(u_dict), 201


def create_user_type(json):
    ut_dao = UserTypeDAO()
    ut_id = ut_dao.create_user_type(json['ut_name'], json['ut_isAdmin'], json['ut_level'])
    user_type = (ut_id,
                 json['ut_name'],
                 json['ut_isAdmin'],
                 json['ut_level'])
    ut_dict = build_user_type_map_dict(user_type)
    return jsonify(ut_dict), 201


def get_user(us_id):
    us_dao = UserDAO()
    user = us_dao.get_user(us_id)
    if not user:
        return jsonify("Not Found"), 404
    else:
        us_dict = build_user_map_dict(user)
        return jsonify(us_dict), 200


def get_user_type(ut_id):
    ut_dao = UserTypeDAO()
    user_type = build_user_type_map_dict(ut_dao.get_user_type(ut_id))
    return jsonify(user_type)


def get_all_users():
    dao = UserDAO()
    user_list = dao.get_all_users()
    users = [build_user_map_dict(row) for row in user_list]
    return jsonify(users)


def get_all_user_types():
    dao = UserTypeDAO()
    user_types_list = dao.get_all_user_types()
    user_types = [build_user_type_map_dict(row) for row in user_types_list]
    return jsonify(user_types)


def get_admin_status(us_id):
    dao = UserDAO()
    return dao.get_admin_status(us_id)
