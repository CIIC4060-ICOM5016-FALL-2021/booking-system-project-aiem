from flask import jsonify

from app.model.room_type import RoomTypeDAO
from app.model.rooms import RoomsDAO


# Library of functions to be used for any Room operations
def build_room_map_dict(row):
    result = {'ro_id': row[0], 'ro_name': row[1], 'ro_location': row[2], 'rt_id': row[3]}
    return result


def build_room_type_map_dict(row):
    result = {'rt_id': row[0], 'rt_name': row[1], 'rt_level': row[2]}
    return result


def get_all_rooms():
    dao = RoomsDAO()
    rooms_list = dao.get_all_rooms()
    rooms = [build_room_map_dict(row) for row in rooms_list]
    return jsonify(rooms)


def get_all_room_types():
    dao = RoomTypeDAO()
    room_types_list = dao.get_all_room_types()
    room_types = [build_room_type_map_dict(row) for row in room_types_list]
    return jsonify(room_types)


def get_room_type_by_name(name):
    dao = RoomTypeDAO()
    room_type = [build_room_type_map_dict(dao.get_room_type_by_name(name))]
    return jsonify(room_type)


# operating under the assumption that there already exists a room type of type_name
def create_room(name, location, type_name):
    r_dao = RoomsDAO()
    rt_dao = RoomTypeDAO()
    # building rt dictionary and extracting id
    rt_dict = build_room_type_map_dict(rt_dao.get_room_type_by_name(type_name))
    rt_id = rt_dict.get('rt_id')
    r_dao.create_room(name, location, rt_id)


def create_room_type(name, level):
    dao = RoomTypeDAO()
    dao.create_room_type(name, level)