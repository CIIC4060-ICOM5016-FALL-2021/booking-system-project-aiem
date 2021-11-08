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

    