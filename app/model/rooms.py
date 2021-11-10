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

    def create_room(self, name, location, type_id):
        try:
            # preparing INSERT operation
            cur = self.db.connection.cursor()
            query = """INSERT INTO "Room"(ro_id, ro_name, ro_location, rt_id)
                       VALUES(DEFAULT, %s, %s, %s);"""
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
                cur.close()
                self.db.close()

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

    def update_room(self):
        return

    def delete_room(self):
        return

    #Global Statistic
    def most_booked_rooms(self):
        cur = self.db.connection.cursor()
        query =  """select ro_name, count(ro_id)
                    from "RoomUnavailability" Natural Inner Join "Room"
                    group by ro_name order by count(ro_id) DESC LIMIT 10"""
        cur.execute(query)
        rooms_list = [row for row in cur]
        return rooms_list
