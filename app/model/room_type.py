import psycopg2

from app.model.db import Database


# Contains all the necessary functions for direct operations in the RoomType table
class RoomTypeDAO:
    def __init__(self):
        self.db = Database()

    def get_all_room_types(self):
        cur = self.db.connection.cursor()
        query = """SELECT rt_id, rt_name, rt_level FROM "RoomType";"""
        cur.execute(query)
        room_types_list = [row for row in cur]
        return room_types_list

    def create_room_type(self, name, level):
        try:
            # preparing INSERT operation
            cur = self.db.connection.cursor()
            query = """INSERT INTO "RoomType"(rt_id, rt_name, rt_level)
                       VALUES(DEFAULT, %s, %s);"""
            query_values = (
                name,
                level
            )
            # executing INSERT operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing create_room_type operation", error)
            self.db.connection = None

        finally:
            # closing the connection
            if self.db.connection is not None:
                cur.close()
                self.db.close()

    def get_room_type_by_name(self, name):
        try:
            # preparing GET operation
            cur = self.db.connection.cursor()
            query = """SELECT rt_id, rt_name, rt_level
                       FROM "RoomType"
                       WHERE rt_name = %s;"""
            query_values = (name,)
            # executing GET operation
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            # error handling
            print("Error executing get_room_type_by_name operation", error)
            self.db.connection = None

        finally:
            # closing the connection
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result
