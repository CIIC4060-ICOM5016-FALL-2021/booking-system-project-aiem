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

    def mark_user_unavailability(self, uu_date, start_time, end_time, user_id):
        try:
            cur = self.db.connection.cursor()
            query = """INSERT INTO "UserUnavailability"(uu_id, uu_date, "uu_startTime", "uu_endTime", us_id)
                       VALUES(DEFAULT, %s, %s, %s, %s)
                       RETURNING uu_id;"""
            query_values = (
                uu_date,
                start_time,
                end_time,
                user_id
            )
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing mark_user_unavailability", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                uu_id = cur.fetchone()[0]
                cur.close()
                self.db.close()
                return uu_id

    def delete_user_unavailability(self, start_time, end_time, user_id):
        try:
            cur = self.db.connection.cursor()
            query = """DELETE FROM "UserUnavailability"
                       WHERE "uu_startTime" = %s AND "uu_endTime" = %s AND us_id = %s;"""
            query_value = (start_time,
                           end_time,
                           user_id)
            cur.execute(query, query_value)
            affected_rows = cur.rowcount
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing delete_user_unavailability (By us_id, start_time and end_time)"), error
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()
                return affected_rows != 0

    def delete_user_unavailability_by_id(self, uu_id):
        try:
            cur = self.db.connection.cursor()
            query = """DELETE FROM "UserUnavailability"
                       WHERE uu_id = %s;"""
            query_values = (uu_id,)
            cur.execute(query, query_values)
            affected_rows = cur.rowcount
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing delete_user_unavailability_by_id"), error
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()
                return affected_rows != 0

    def get_user_unavailability(self, us_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT uu_id, uu_date, "uu_startTime", "uu_endTime", us_id
                       FROM "UserUnavailability" WHERE us_id = %s; """
            query_values = (us_id,)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user_unavailability", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = [row for row in cur]
                cur.close()
                self.db.close()
                return result

    def get_user_unavailability_date(self, us_id, date):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT uu_id, uu_date, "uu_startTime", "uu_endTime", us_id
                       FROM "UserUnavailability" WHERE us_id = %s AND uu_date = %s; """
            query_values = (us_id, date)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user_unavailability_date", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = [row for row in cur]
                cur.close()
                self.db.close()
                return result

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

    def check_user(self, username, password):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT us_id
                       FROM "User"
                       WHERE us_username = %s and us_password = %s;"""
            query_values = (username,password)
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
                if result is None:
                    return -1
                else:
                    return result[0]

    def get_user_schedule(self, us_id, date):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT rstart, rend, title, rdesc FROM ((
                                        SELECT res."re_startTime" as rstart, res."re_endTime" as rend, met.mt_name AS title, met.mt_desc AS rdesc
                                        FROM (SELECT * FROM "Reservation" WHERE re_date = %s) as res,
                                             (SELECT * FROM "Meeting") as met,
                                             (SELECT * FROM "Attending") as att
                                        WHERE met.re_id = res.re_id
                                        AND met.mt_id = att.mt_id
                                        AND %s in (att.us_id)
                                    )UNION(
                                        SELECT "uu_startTime" AS rstart, "uu_endTime" AS rend, 'Unavailable' AS title, '' AS rdesc
                                        FROM "UserUnavailability"
                                        WHERE uu_date = %s
                                        AND us_id = %s
                                    )) AS schedule ORDER BY rstart;"""
            query_values = (date,
                            us_id,
                            date,
                            us_id)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_user_schedule operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = [row for row in cur]
                cur.close()
                self.db.close()
                return result

    def get_complete_user_schedule(self, us_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT date, "start", "end", title, "desc", room, creator, username, id
                        FROM ((
                            SELECT res.re_date AS date,
                                   res."re_startTime" AS "start",
                                   res."re_endTime" AS "end",
                                   met.mt_name AS title,
                                   met.mt_desc AS "desc",
                                   rm.ro_name AS room,
                                   usr.us_name AS creator,
                                   usr.us_username AS username,
                                   met.mt_id AS id
                            FROM (SELECT * FROM "Reservation") AS res,
                                 (SELECT * FROM "Meeting") AS met,
                                 (SELECT * FROM "Attending") AS att,
                                 (SELECT * FROM "User") AS usr,
                                 (SELECT * FROM "Room") AS rm
                            WHERE met.re_id = res.re_id
                                AND met.mt_id = att.mt_id
                                AND usr.us_id = res.us_id
                                AND res.ro_id = rm.ro_id
                                AND %s in (att.us_id)
                        )UNION(
                            SELECT uu.uu_date AS date,
                                   uu."uu_startTime" AS "start",
                                   uu."uu_endTime" AS "end",
                                   'Unavailable' AS title,
                                   '' AS "desc",
                                   '' AS room,
                                   usr.us_name AS creator,
                                   usr.us_username AS username,
                                   uu.uu_id AS id
                            FROM (SELECT * FROM "UserUnavailability") AS uu,
                                 (SELECT * FROM "User") AS usr
                            WHERE usr.us_id = %s
                                AND usr.us_id = uu.us_id
                        )) AS schedule
                        ORDER BY "date", "start";"""
            query_values = (us_id,
                            us_id)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing get_complete_user_schedule operation", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = [row for row in cur]
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
                    from "Reservation" Natural Inner Join "User"
                    group by us_name order by count(us_id) DESC LIMIT 10"""
        cur.execute(query)
        users_list = [row for row in cur]
        return users_list

    def most_used_room(self, us_id):
        try:
            cur = self.db.connection.cursor()
            query = """select us_name, ro_name, count(ro_id)
                       from "Room" Natural Inner Join "User" 
                       Natural Inner Join "Reservation"
                       Where us_id=%s group by us_name, ro_name
                       order by count(ro_id) DESC LIMIT 10"""
            query_values = (us_id,)
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

            query = """select us_name as Name, count(us_name)
            from (
                select M.mt_id, M.us_id
                from (select mt_id as MT1
                      from "Attending" where us_id = %s) as A,
                "Attending" as M
                where M.mt_id = A.MT1
                EXCEPT (SELECT mt_id, us_id FROM "Attending" 
                where us_id = %s)
            ) as R  natural inner join "User"
            group by us_name
            order by count(us_id) DESC LIMIT 1"""
            query_values = (
                us_id,
                us_id,
            )

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
