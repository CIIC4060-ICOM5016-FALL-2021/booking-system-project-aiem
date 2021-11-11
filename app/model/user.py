import psycopg2

from app.model.db import Database


class UserDAO:
    def __init__(self):
        self.db = Database()

    def create_user(self, name, username, password, type_id):
        try:
            cur = self.db.connection.cursor()
            query = """ INSERT INTO "User"(us_id, us_name, us_username, us_password, ut_id)
                        VALUES(DEFAULT, %s, %s, %s, %s)
                        RETURNING us_id;"""
            query_values = (
                name,
                username,
                password,
                type_id
            )
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing create_user operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                us_id = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return us_id

    def get_user(self, user_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT us_id, us_name, us_username, us_password, ut_id
                       FROM "User"
                       WHERE us_id = %s;"""
            query_values = (user_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def get_all_users(self):
        cur = self.db.connection.cursor()
        query = """SELECT us_id, us_name, us_username, us_password, ut_id FROM "User";"""
        cur.execute(query)
        user_list = [row for row in cur]
        return user_list

    def update_user(self, name, username, password, type_id, user_id):
        try:
            cur = self.db.connection.cursor()
            query = """ UPDATE "User" 
                    SET us_name = %s, us_username = %s, us_password = %s, ut_id = %s
                    WHERE us_id = %s;"""
            query_values = (
                name,
                username,
                password,
                type_id,
                user_id
            )
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing update_user operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()

    def delete_user(self, user_id):
        try:
            cur = self.db.connection.cursor()
            query = """DELETE FROM "User" 
                       WHERE us_id = %s;"""
            query_values = (user_id,)
            cur.execute(query, query_values)
            affected_rows = cur.rowcount
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing delete_user operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()
                return affected_rows != 0


        # Global Statistic to find top 10 most booking user
    def most_booked_user(self):
        cur = self.db.connection.cursor()
        query =  """select us_name, count(us_id)
                    from "UserUnavailability" Natural Inner Join "User"
                    group by us_name order by count(us_id) DESC LIMIT 10"""
        cur.execute(query)
        users_list = [row for row in cur]
        return users_list

    def most_used_room(self, us_name):
        try:
            cur = self.db.connection.cursor()
            query = """select us_name, ro_name, count(ro_id)
                       from "Room" Natural Inner Join "User" 
                       Natural Inner Join "Reservation"
                       Where us_name=%s group by us_name, ro_name
                       order by count(ro_id) DESC LIMIT 1"""
            query_values = (us_name,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing most_used_room operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result