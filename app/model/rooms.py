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

    # pending
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
            print("Error executing create_room operation", error)
            self.db.connection = None

        finally:
            # closing the connection
            if self.db.connection is not None:
                ru_id = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return ru_id

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
            print("Error executing get_room operation", error)
            self.db.connection = None

        finally:
            # closing the connection
            if self.db.connection is not None:
                result = [row for row in cur]
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
            print("Error executing get_room operation", error)
            self.db.connection = None

        finally:
            # closing the connection
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
            # closing the connection
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
            # closing the connection
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def update_room(self, name, location, type_id, room_id):
        try:
            # preparing GET operation
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
            # executing GET operation
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
            # preparing GET operation
            cur = self.db.connection.cursor()
            query = """DELETE 
                       FROM "Room"
                       WHERE ro_id = %s;"""
            query_values = (room_id,)
            # executing GET operation
            cur.execute(query, query_values)
            affected_rows = cur.rowcount
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing delete_room operation", error)
            self.db.connection = None

        finally:
            # closing the connection
            if self.db.connection is not None:
                cur.close()
                self.db.close()
                return affected_rows != 0
