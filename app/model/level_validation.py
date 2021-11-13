import psycopg2

from app.model.db import Database


class UserLevelValidationDAO:
    def __init__(self):
        self.db = Database()

    def get_user_level(self, us_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT ut_level FROM "UserType" 
                       WHERE ut_id = (SELECT ut_id FROM "User"
                       WHERE us_id = %s);"""
            query_values = (us_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user_level operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def get_room_level(self, ro_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT rt_level FROM "RoomType" 
                       WHERE rt_id = (SELECT rt_id FROM "Room"
                       WHERE ro_id = %s);"""
            query_values = (ro_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_room_level", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

