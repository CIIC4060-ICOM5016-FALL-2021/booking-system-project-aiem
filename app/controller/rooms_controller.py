from datetime import datetime

from flask import jsonify

from app.model.room_type import RoomTypeDAO
from app.model.rooms import RoomsDAO


class RoomsController:
    # Library of functions to be used for any Room operations
    @staticmethod
    def build_room_dict(row):
        result = {'ro_id': row[0],
                  'ro_name': row[1],
                  'ro_location': row[2],
                  'rt_id': row[3]}
        return result

    @staticmethod
    def build_room_type_dict(row):
        result = {'rt_id': row[0],
                  'rt_name': row[1],
                  'rt_level': row[2]}
        return result

    @staticmethod
    def build_room_unavailability_dict(row):
        result = {'ru_id': row[0],
                  'ru_date': row[1].strftime("%Y-%m-%d"),
                  'ru_startTime': row[2].strftime("%H:%M:%S"),
                  'ru_endTime': row[3].strftime("%H:%M:%S"),
                  'ro_id': row[4]}
        return result

    @staticmethod
    def build_room_schedule_dict(row):
        result = {'rstart': row[0].strftime("%H:%M:%S"),
                  'rend': row[1].strftime("%H:%M:%S"),
                  'title': row[2],
                  'rdesc': row[3]}
        return result

    @staticmethod
    def build_most_booked_room_map_dict(row):
        result = {'ro_name': row[0], 'count': row[1]}
        return result

    def get_all_rooms(self):
        ro_dao = RoomsDAO()
        rooms_list = ro_dao.get_all_rooms()
        rooms = [self.build_room_dict(row) for row in rooms_list]
        return jsonify(rooms), 200

    def get_all_room_types(self):
        rt_dao = RoomTypeDAO()
        room_types_list = rt_dao.get_all_room_types()
        room_types = [self.build_room_type_dict(row) for row in room_types_list]
        return jsonify(room_types), 200

    def set_room_unavailability(self, ro_id, admin, json):
        ro_dao = RoomsDAO()
        if admin:
            ru_id = ro_dao.set_room_unavailability(json["ru_date"],
                                                   json["ru_startTime"],
                                                   json["ru_endTime"],
                                                   ro_id)
            unavailability = (ru_id,
                              json["ru_date"],
                              json["ru_startTime"],
                              json["ru_endTime"],
                              ro_id)
            ru_dict = self.build_room_unavailability_dict(unavailability)
            return jsonify(ru_dict), 201
        else:
            return jsonify("Forbidden"), 403

    def update_room_unavailability(self, ru_id, ro_id, admin, json):
        ro_dao = RoomsDAO()
        if admin:
            ro_dao.update_room_unavailability(ru_id,
                                              json["ru_date"],
                                              json["ru_startTime"],
                                              json["ru_endTime"],
                                              ro_id)
            unavailability = (ru_id,
                              datetime.strptime(json["ru_date"], "%Y-%m-%d").date(),
                              datetime.strptime(json["ru_startTime"], "%H:%M:%S").time(),
                              datetime.strptime(json["ru_endTime"], "%H:%M:%S").time(),
                              ro_id)
            ru_dict = self.build_room_unavailability_dict(unavailability)
            return jsonify(ru_dict), 201
        else:
            return jsonify("Forbidden"), 403

    def get_room_unavailability_by_id(self, ru_id, ro_id):
        ro_dao = RoomsDAO()
        unavailable = ro_dao.get_room_unavailability_by_id(ru_id, ro_id)
        if not unavailable:
            return jsonify("Not Found"), 404
        else:
            ru_dict = self.build_room_unavailability_dict(unavailable)
            return jsonify(ru_dict), 200

    def get_room_unavailability(self, ro_id, ru_date):
        ro_dao = RoomsDAO()
        if ru_date is not None:
            room_unavailable_list = ro_dao.get_room_unavailability_date(ro_id, ru_date)
            ru_dict = [self.build_room_unavailability_dict(row) for row in room_unavailable_list]
            return jsonify(ru_dict), 200
        else:
            room_unavailable_list = ro_dao.get_room_unavailability(ro_id)
            ru_dict = [self.build_room_unavailability_dict(row) for row in room_unavailable_list]
            return jsonify(ru_dict), 200

    def get_room_schedule(self, ro_id, r_date):
        ro_dao = RoomsDAO()
        room_schedule = ro_dao.get_room_schedule(ro_id, r_date)
        schedule_dict = [self.build_room_schedule_dict(row) for row in room_schedule]
        return jsonify(schedule_dict), 200

    def get_available_by_date_and_time(self, r_date, r_start, r_end):
        ro_dao = RoomsDAO()
        available_rooms = ro_dao.get_available_by_date_and_time(r_date, r_start, r_end)
        available_dict = [self.build_room_dict(row) for row in available_rooms]
        return jsonify(available_dict), 200

    # operating under the assumption that there already exists a room type of type_name
    def create_room(self, json):
        ro_dao = RoomsDAO()
        # extract new id -> build room = [id, name, location, type id] -> build dict
        ro_id = ro_dao.create_room(json['ro_name'], json['ro_location'], json['rt_id'])
        room = (ro_id,
                json['ro_name'],
                json['ro_location'],
                json['rt_id'])
        ro_dict = self.build_room_dict(room)
        return jsonify(ro_dict), 201

    def get_room(self, ro_id):
        ro_dao = RoomsDAO()
        room = ro_dao.get_room(ro_id)
        if not room:
            return jsonify("Not Found"), 404
        else:
            ro_dict = self.build_room_dict(room)
            return jsonify(ro_dict), 200

    def update_room(self, ro_id, json):
        ro_dao = RoomsDAO()
        ro_dao.update_room(json['ro_name'], json['ro_location'], json['rt_id'], ro_id)
        room = (ro_id,
                json['ro_name'],
                json['ro_location'],
                json['rt_id'])
        ro_dict = self.build_room_dict(room)
        return jsonify(ro_dict), 200

    def delete_room(self, ro_id):
        ro_dao = RoomsDAO()
        result = ro_dao.delete_room(ro_id)
        if result:
            return jsonify("Deleted"), 200
        else:
            return jsonify("Not Found"), 404

    def create_room_type(self, json):
        dao = RoomTypeDAO()
        rt_id = dao.create_room_type(json['rt_name'], json['rt_level'])
        room_type = (rt_id,
                     json['rt_name'],
                     json['rt_level'])
        rt_dict = self.build_room_type_dict(room_type)
        return jsonify(rt_dict), 201

    def get_room_type(self, rt_id):
        dao = RoomTypeDAO()
        room_type = self.build_room_type_dict(dao.get_room_type(rt_id))
        return jsonify(room_type)

    def get_most_booked_room(self):
        dao = RoomsDAO()
        room_list = dao.most_booked_rooms()
        rooms = [self.build_most_booked_room_map_dict(row) for row in room_list]
        return jsonify(rooms)
