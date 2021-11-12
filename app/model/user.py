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

    def get_admin_status(self, user_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT "ut_isAdmin"
                       FROM "User" natural inner join "UserType"
                       WHERE us_id = %s;"""
            query_values = (user_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_admin_status operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return result

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

    def user_most_meeting_with_user(self, us_id):
        try:
            cur = self.db.connection.cursor()

            #Three queries:
            #   1st we find us_id meetings
            #   2nd we find all others who are connected in that meeting, except user
            #   3rd we count to find the user who connects the most with the input

            query = """select us_name as Name, count(us_id)
            from (
                select M.mt_id, M.us_id
                from (select mt_id as MT1
                      from "Attending"
                      where us_id = %s) as A,
                "Attending" as M
                where M.mt_id = A.MT1
                EXCEPT (SELECT * FROM "Attending" where us_id = 11)
            ) as R  natural inner join "User"
            group by us_name
            order by count(us_id) DESC LIMIT 1"""
            query_values = (us_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing user_most_meeting_with_user operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result
