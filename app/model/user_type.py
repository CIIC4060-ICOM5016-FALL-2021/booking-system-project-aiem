import psycopg2

from app.model.db import Database


class UserTypeDAO:
    def __init__(self):
        self.db = Database()

    def create_user_type(self, name, is_admin, level):
        try:
            cur = self.db.connection.cursor()
            query = """INSERT INTO "UserType"(ut_id, ut_name, "ut_isAdmin", ut_level) 
                        VALUES(DEFAULT, %s, %s, %s);"""

            query_values = (
                name,
                is_admin,
                level
            )

            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing create_user_type operation", error)
            self.db.connection = None

        finally:

            if self.db.connection is not None:
                cur.close()
                self.db.close()

    def get_user_type_by_name(self, name):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT ut_id, ut_name, "ut_isAdmin", ut_level
                       FROM "UserType"
                       WHERE ut_name = %s;"""
            query_values = (name,)

            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user_type_by_name operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def get_all_user_types(self):
        cur = self.db.connection.cursor()
        query = """SELECT ut_id, ut_name, "ut_isAdmin", ut_level
                   FROM "UserType"; """
        cur.execute(query)
        user_types_list = [row for row in cur]
        return user_types_list

    def get_user_type(self, ut_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT ut_id, ut_name, "ut_isAdmin", ut_level
                       FROM "UserType" WHERE ut_id = %s; """
            query_values = (ut_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user_type operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result



