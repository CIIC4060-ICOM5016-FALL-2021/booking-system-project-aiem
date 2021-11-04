from flask import jsonify

from app.model.rooms import RoomsDAO


def build_map_dict(row):
    result = {'ro_id': row[0], 'ro_name': row[1], 'ro_location': row[2], 'rt_id': row[3]}
    return result


def get_all_rooms():
    dao = RoomsDAO()
    part_list = dao.get_all_rooms()
    return jsonify([build_map_dict(row) for row in part_list])
