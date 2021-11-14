import psycopg2

from app.model.db import Database


class UserLevelValidationDAO:
    def __init__(self):
        self.db = Database()

    def get_user_level_from_us_id(self, us_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT ut_level FROM "UserType" 
                       WHERE ut_id = (SELECT ut_id FROM "User"
                       WHERE us_id = %s);"""
            query_values = (us_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user_level_from_us_id operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result

    def get_user_level_from_ut_id(self, ut_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT ut_level FROM "UserType" 
                       WHERE ut_id = %s;"""
            query_values = (ut_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user_level_from_ut_id operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result

    def get_room_level_from_ro_id(self, ro_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT rt_level FROM "RoomType" 
                       WHERE rt_id = (SELECT rt_id FROM "Room"
                       WHERE ro_id = %s);"""
            query_values = (ro_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_room_level_from_ro_id", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result

    def get_room_level_from_rt_id(self, rt_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT rt_level FROM "RoomType" 
                       WHERE rt_id = %s;"""
            query_values = (rt_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_room_level_from_rt_id", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result

    def get_room_id_from_meeting_id(self, mt_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT ro_id FROM "Reservation"
                       WHERE re_id = (SELECT re_id FROM
                       "Meeting" WHERE mt_id = %s);"""
            query_values = (mt_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_room_id_from_meeting", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result

    def get_owner_id_from_mt_id(self, mt_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT us_id FROM "Reservation"
                       WHERE re_id = (SELECT re_id FROM
                       "Meeting" WHERE mt_id = %s);"""
            query_value = (mt_id,)
            cur.execute(query, query_value)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_owner_id_from_mt_id", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result

    def get_owner_id_from_re_id(self, re_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT us_id FROM "Reservation"
                       WHERE re_id = %s;"""
            query_value = (re_id,)
            cur.execute(query, query_value)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_owner_id_from_re_id", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result

    def confirm_attending(self, mt_id, session_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT mt_id, us_id FROM "Attending"
                       WHERE mt_id = %s AND us_id = %s; """
            query_value = (mt_id, session_id)
            cur.execute(query, query_value)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_owner_id_from_re_id", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def get_us_id_from_uu_id(self, uu_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT us_id FROM "UserUnavailability"
                       WHERE uu_id = %s;"""
            query_value = (uu_id,)
            cur.execute(query, query_value)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_us_id_from_uu_id", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result
