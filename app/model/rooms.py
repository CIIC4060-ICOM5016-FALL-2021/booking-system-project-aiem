import psycopg2

from app.model.db import Database


# Contains all necessary functions for direct operations in the Room table
class RoomsDAO:
    def __init__(self):
        self.db = Database()

    def get_all_rooms(self):
        cur = self.db.connection.cursor()
        query = """SELECT ro_id, ro_name, ro_location, rt_id FROM "Room";"""
        cur.execute(query)
        rooms_list = [row for row in cur]
        return rooms_list

    def set_room_unavailability(self, date, start, end, room_id):
        try:
            # preparing INSERT operation
            cur = self.db.connection.cursor()
            query = """INSERT INTO "RoomUnavailability"(ru_id, ru_date, "ru_startTime", "ru_endTime", ro_id)
                       VALUES(DEFAULT, %s, %s, %s, %s)
                       RETURNING ru_id;"""
            query_values = (
                date,
                start,
                end,
                room_id
            )
            # executing INSERT operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing set_room_unavailability operation", error)
            self.db.connection = None

        finally:
            # closing the connection and returning id of the seperated unavailable time
            if self.db.connection is not None:
                ru_id = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return ru_id

    def update_room_unavailability(self, room_uid, date, start, end, room_id):
        try:
            # preparing UPDATE operation
            cur = self.db.connection.cursor()
            query = """UPDATE "RoomUnavailability"
                       SET ru_date = %s, "ru_startTime" = %s, "ru_endTime" = %s, ro_id = %s
                       WHERE ru_id = %s;"""
            query_values = (
                date,
                start,
                end,
                room_id,
                room_uid
            )
            # executing UPDATE operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing update_room_unavailability operation", error)
            self.db.connection = None

        finally:
            # closing the connection
            if self.db.connection is not None:
                cur.close()
                self.db.close()

    def get_room_unavailability(self, room_id):
        try:
            # preparing GET operation
            cur = self.db.connection.cursor()
            query = """SELECT ru_id, ru_date, "ru_startTime", "ru_endTime", ro_id
                        FROM "RoomUnavailability"
                        WHERE ro_id = %s;"""
            query_values = (room_id,)
            # executing GET operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing get_room_unavailability operation", error)
            self.db.connection = None

        finally:
            # closing the connection and returning the list of unavailable times for a room
            if self.db.connection is not None:
                result = [row for row in cur]
                cur.close()
                self.db.close()
                return result

    def get_room_unavailability_by_id(self, room_uid, room_id):
        try:
            # preparing GET operation
            cur = self.db.connection.cursor()
            query = """SELECT ru_id, ru_date, "ru_startTime", "ru_endTime", ro_id
                        FROM "RoomUnavailability"
                        WHERE ru_id = %s
                        AND ro_id = %s;"""
            query_values = (
                room_uid,
                room_id
            )
            # executing GET operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing get_room_unavailability_by_id operation", error)
            self.db.connection = None

        finally:
            # closing the connection and returning the unavailable slot for a room
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def get_room_unavailability_date(self, room_id, date):
        try:
            # preparing GET operation
            cur = self.db.connection.cursor()
            query = """SELECT ru_id, ru_date, "ru_startTime", "ru_endTime", ro_id
                        FROM "RoomUnavailability"
                        WHERE ro_id = %s
                        AND ru_date = %s;"""
            query_values = (
                room_id,
                date
            )
            # executing GET operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing get_room_unavailability_date operation", error)
            self.db.connection = None

        finally:
            # closing the connection and returning the list of unavailable times
            # for a room at a specific date
            if self.db.connection is not None:
                result = [row for row in cur]
                cur.close()
                self.db.close()
                return result

    def get_room_schedule(self, room_id, date):
        try:
            # preparing GET operation
            cur = self.db.connection.cursor()
            query = """SELECT rstart, rend, title, rdesc FROM ((
                            SELECT "re_startTime" AS rstart, "re_endTime" AS rend, mt_name AS title, mt_desc AS rdesc
                            FROM "Reservation" NATURAL INNER JOIN "Meeting"
                            WHERE re_date = %s
                            AND ro_id = %s
                        )UNION(
                            SELECT "ru_startTime" AS rstart, "ru_endTime" AS rend, 'Unavailable' AS title, '' AS rdesc
                            FROM "RoomUnavailability"
                            WHERE ru_date = %s
                            AND ro_id = %s
                        )) AS schedule ORDER BY rstart ASC;"""
            query_values = (
                date,
                room_id,
                date,
                room_id
            )
            # executing GET operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing get_room_schedule operation", error)
            self.db.connection = None

        finally:
            # closing the connection and returning the all day schedule of a room
            # including unavailable times and names and descriptions of meetings
            if self.db.connection is not None:
                result = [row for row in cur]
                cur.close()
                self.db.close()
                return result

    def get_available_by_date_and_time(self, date, start, end):
        try:
            # preparing GET operation
            cur = self.db.connection.cursor()
            query = """SELECT ro_id, ro_name, ro_location, rt_id
                       FROM "Room"
                       WHERE ro_id
                           NOT IN (
                              SELECT ro_id
                              FROM "RoomUnavailability"
                                       NATURAL INNER JOIN "Reservation"
                              WHERE (ru_date = %s AND re_date = %s)
                                AND (("re_startTime" >= %s AND "re_endTime" <= %s)
                                  OR ("ru_startTime" >= %s AND "ru_endTime" <= %s))
                          )
                       GROUP BY ro_id;"""
            query_values = (
                date,
                date,
                start,
                end,
                start,
                end
            )
            # executing GET operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing get_available_by_date_and_time", error)
            self.db.connection = None

        finally:
            # closing the connection and returning a list of available rooms
            # at the specified date and time frame
            if self.db.connection is not None:
                result = [row for row in cur]
                cur.close()
                self.db.close()
                return result

    def create_room(self, name, location, type_id):
        try:
            # preparing INSERT operation
            cur = self.db.connection.cursor()
            query = """INSERT INTO "Room"(ro_id, ro_name, ro_location, rt_id)
                       VALUES(DEFAULT, %s, %s, %s)
                       RETURNING ro_id;"""
            query_values = (
                name,
                location,
                type_id
            )
            # executing INSERT operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing create_room operation", error)
            self.db.connection = None

        finally:
            # closing the connection and returning the id of the created room
            if self.db.connection is not None:
                ro_id = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return ro_id

    def get_room(self, room_id):
        try:
            # preparing GET operation
            cur = self.db.connection.cursor()
            query = """SELECT ro_id, ro_name, ro_location, rt_id 
                       FROM "Room"
                       WHERE ro_id = %s;"""
            query_values = (room_id,)
            # executing GET operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing get_room operation", error)
            self.db.connection = None

        finally:
            # closing the connection and returning the room
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def update_room(self, name, location, type_id, room_id):
        try:
            # preparing UPDATE operation
            cur = self.db.connection.cursor()
            query = """ UPDATE "Room"
                        SET ro_name = %s, ro_location = %s, rt_id = %s
                        WHERE ro_id = %s;"""
            query_values = (
                name,
                location,
                type_id,
                room_id
            )
            # executing UPDATE operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing update_room operation", error)
            self.db.connection = None

        finally:
            # closing the connection
            if self.db.connection is not None:
                cur.close()
                self.db.close()

    def delete_room(self, room_id):
        try:
            # preparing DELETE operation
            cur = self.db.connection.cursor()
            query = """DELETE 
                       FROM "Room"
                       WHERE ro_id = %s;"""
            query_values = (room_id,)
            # executing DELETE operation
            cur.execute(query, query_values)
            affected_rows = cur.rowcount
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing delete_room operation", error)
            self.db.connection = None

        finally:
            # closing the connection and returning affected rows status
            if self.db.connection is not None:
                cur.close()
                self.db.close()
                return affected_rows != 0

    # Global Statistic
    def most_booked_rooms(self):
        cur = self.db.connection.cursor()
        query = """select ro_name, count(ro_id)
                    from "RoomUnavailability" Natural Inner Join "Room"
                    group by ro_name order by count(ro_id) DESC LIMIT 10"""
        cur.execute(query)
        rooms_list = [row for row in cur]
        return rooms_list
