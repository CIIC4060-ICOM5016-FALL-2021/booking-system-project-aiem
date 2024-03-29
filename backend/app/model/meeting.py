from backend.app.model.db import Database


# Handles Meeting/meeting attending DAO Operations
class MeetingDAO:

    # Reusable SQL Snippets --------------------------------------------------------------------------------------------

    GET_MEETING = """select mt_id, mt_name, mt_desc, re_id, re_date, "re_startTime", "re_endTime", us_id, us_name, ro_id
                    , ro_name 
                     from "Meeting" natural inner join "Reservation" natural inner join "User" natural inner join "Room"
                  """
    ORDER_DATE_DESCENDING = """ order by re_date desc, "re_startTime" desc;"""
    
    # order by snippets which may or may not be used later (in fact they could be used elsewhere :thinking:)
    ORDER_BY_X = " order by %s"  # these snippets are only usable for ordering by one column pero oops
    ASC = ";"  # Since asc is default we can just add a semicolon because yes
    DESC = " desc;"  # Specify desc then continue

    def __init__(self):
        self.conn = Database().connection  # this is so I don't have to radically alter the code

    # Gets--------------------------------------------------------------------------------------------------------------

    # Gets all meetings (along with some additional linked information including linked Reservation details, Who
    # reserved it (User ID/Name), and where it is reserved (Room ID/Name))
    def getAllMeeting(self):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + self.ORDER_DATE_DESCENDING
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # Gets a specified meeting
    def getMeetingById(self, mt_id):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + " where mt_id = %s;"  # since we only get one we don't need to order
        cursor.execute(query, (mt_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
        
    # Gets a list of every user that is attending a given meeting
    def getMeetingAttending(self, mt_id):
        cursor = self.conn.cursor()
        query = """select us_id, us_name, us_username 
                   from "User" natural inner join "Attending" 
                   where mt_id=%s;"""
        cursor.execute(query, (mt_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getUserAttendingCount(self, us_id):
        cursor = self.conn.cursor()
        query = """select count(*) from "Attending" where us_id=%s;"""
        cursor.execute(query, (us_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0]


    # Gets meetings reserved by given reserving party ordered by date descending
    def getMeetingsByReserver(self, us_id):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + " where us_id = %s" + self.ORDER_DATE_DESCENDING
        cursor.execute(query, (us_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # Gets meetings for a certain date in certain room
    def getMeetingsForRoomOn(self, ro_id, re_date):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + " where ro_id = %s and re_date = %s" + self.ORDER_DATE_DESCENDING
        cursor.execute(query, (ro_id, re_date,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # Gets meetings for a certain date with certain user
    def getMeetingsForUserOn(self, us_id, re_date):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + """ where re_date  = %s and mt_id IN
                                    (select mt_id from "Meeting" natural inner join "Attending" 
                                    where us_id = %s)""" + self.ORDER_DATE_DESCENDING
        cursor.execute(query, (re_date, us_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # Gets meeting that is occurring at a given time in a given room
    def getMeetingInRoomAtTime(self, ro_id, date, time):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + """ where ro_id = %s and re_date = %s 
                                        and "re_startTime" < %s and "re_endTime" > %s;"""
        cursor.execute(query, (ro_id, date, time, time,))
        result = cursor.fetchone()
        cursor.close()
        return result

    # def getAvailableRoomAtTimeRange(self, date, start, end):
        # get the rooms that are unavailable #this belongs on the room DAO I think
    # return null

    # Check if a user is busy during a certain time range (IE If the user is busy or unavailable). Used to check if we
    # can add them as attending
    def checkUserBusy(self, us_id, date, start, end): #this function may now actually be unused
        cursor = self.conn.cursor()
        query = """select count(*) from (
                     select "re_startTime" as startp, "re_endTime" as endp, re_date as datep
                     from "Meeting" natural inner join "Reservation"
                     where mt_id in (select mt_id from "Attending" where us_id=%s)
                     union (
                         select "uu_startTime" as startp, "uu_endTime" as endp, uu_date as datep
                         from "UserUnavailability"
                         where us_id = %s
                         )
                    ) as UnavailableTimes where datep = %s and (
                        (startp < %s and endp > %s) or --Checks if the given start is between the start and endtime of 
                                                       --an unavailability period
                        (startp < %s and endp > %s) or --Checks if the given end is between the start and endtime of an 
                                                       --unavailability period
                        (startp > %s and endp < %s) --Checks if an existing unavailability period exists between the 
                                                    --given start and end times
                    )
                ; 
        """
        cursor.execute(query, (us_id, us_id, date, start, start, end, end, start, end,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] >= 1  # if there's 1 or more in these things, the user is busy

    # Check if a meeting is possible (IE The reserve user is not busy/unavailable and the room is not busy/unavailable).
    # Used to check if we should create a meeting or not
    def checkMeetingBusy(self, attendees, ro_id, date, start, end):
        cursor = self.conn.cursor()
        query = """select count(*) from (
                    --Times that are unavailable because either the user is in a meeting or the room is busy
                     select "re_startTime" as startp, "re_endTime" as endp, re_date as datep 
                     from "Meeting" natural inner join "Reservation"
                     where mt_id in (select mt_id from "Attending" where us_id in %s) or ro_id = %s
                     union ( --User unavailable times just because they said so
                         select "uu_startTime" as startp, "uu_endTime" as endp, uu_date as datep
                         from "UserUnavailability"
                         where us_id in %s )
                     union ( --Room is unavailable because the department said so
                        select "ru_startTime" as startp, "ru_endTime" as endp, ru_date as datep
                        from "RoomUnavailability"
                        where ro_id=%s )
                     ) as UnavailableTimes
                    where datep = %s and (
                        (startp < %s and endp > %s) or --Checks if the given start is between the start and endtime 
                                                       --of an unavailability period
                        (startp < %s and endp > %s) or --Checks if the given end is between the start and endtime of an 
                                                       --unavailability period
                        (startp > %s and endp < %s) --Checks if an existing unavailability period exists between the 
                                                    --given start and end times
                    )
                ;"""
        cursor.execute(query, (attendees, ro_id, attendees, ro_id, date, start, start, end, end, start, end,))
        result = cursor.fetchone()
        cursor.close()
        return result[0]  # if there's 1 or more in these things, the user or the room is busy or unavailable
        
    # Insert------------------------------------------------------------------------------------------------------------
    def insertMeeting(self, mt_name, mt_desc, re_id):
        cursor = self.conn.cursor()
        query = """insert into "Meeting" (mt_name, mt_desc, re_id) values (%s,%s,%s) returning mt_id;"""
        cursor.execute(query, (mt_name, mt_desc, re_id,))
        mt_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return mt_id

    # This should be done BEFORE insert meeting
    def insertReservation(self, re_date, re_startTime, re_endTime, us_id, ro_id):
        cursor = self.conn.cursor()
        query = """insert into "Reservation" (re_date, "re_startTime","re_endTime",us_id,ro_id) values 
                                (%s,%s,%s,%s,%s) returning re_id;"""
        cursor.execute(query, (re_date, re_startTime, re_endTime, us_id, ro_id,))
        re_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return re_id

    # Does both in order
    def insertEverythingForMeeting(self, mt_name, mt_desc, re_date, re_startTime, re_endTime, us_id, ro_id, attendees):
        re_id = self.insertReservation(re_date, re_startTime, re_endTime, us_id, ro_id)  # Create the reservation
        mt_id = self.insertMeeting(mt_name, mt_desc, re_id)  # Create the meeting
        for a in attendees:
            self.insertAttending(mt_id, a)  # Register those who are attending
        self.insertAttending(mt_id, us_id)
        return mt_id  # finally we're done after three requests que lindo

    # Adds an attending user
    def insertAttending(self, mt_id, us_id):
        cursor = self.conn.cursor()
        query = """insert into "Attending" (mt_id,us_id) values (%s,%s);"""
        cursor.execute(query, (mt_id, us_id,))
        # re_id = cursor.fetchone()[0] #Here we don't actually need to fetch anything
        self.conn.commit()
        cursor.close()
        return True

    # Update------------------------------------------------------------------------------------------------------------
    def updateMeeting(self, mt_id, mt_name, mt_description):
        cursor = self.conn.cursor()
        query = """update "Meeting" set mt_name=%s, 
                                       mt_desc=%s 
                  where mt_id=%s;"""
        cursor.execute(query, (mt_name, mt_description, mt_id,))
        self.conn.commit()
        cursor.close()
        return True

    # We never need to update any of the reservation data
    # There is no update for attending. You either create it or delete it. That's it

    # delete------------------------------------------------------------------------------------------------------------
    # Delete just the meeting
    def deleteMeeting(self, mt_id):

        # Reservation wasn't being deleted so we need to add a delete from reservation
        # because of the cascade, if we delete the reservation, we delete the meeting, and then delete the attending
        # Therefore:

        return self.deleteReservation(mt_id)

        # And that's it

        # cursor = self.conn.cursor()
        # query = """delete from "Meeting" where mt_id=%s;"""
        # cursor.execute(query, (mt_id,))
        
        # determine affected rows
        # affected_rows = cursor.rowcount
        # self.conn.commit()
        
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        # cursor.close()
        # return affected_rows != 0

    # Deletes a meeting's tied reservation
    def deleteReservation(self, mt_id):
        cursor = self.conn.cursor()
        query = """delete from "Reservation" where re_id in (select re_id from "Meeting" where mt_id = %s)"""
        cursor.execute(query, (mt_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        cursor.close()
        return affected_rows != 0

    # Delete a specific attender
    def deleteAttending(self, mt_id, us_id):
        cursor = self.conn.cursor()
        query = """delete from "Attending" where mt_id=%s and us_id=%s;"""
        cursor.execute(query, (mt_id, us_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        cursor.close()
        return affected_rows != 0
    
    # Delete all those attending a certain meeting
    def deleteAllAttending(self, mt_id):
        cursor = self.conn.cursor()
        query = """delete from "Attending" where mt_id=%s;"""
        cursor.execute(query, (mt_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        cursor.close()
        return affected_rows != 0

    def get_reserver_by_time(self, ro_id, start_time, date):
        cursor = self.conn.cursor()
        query = """ select person.us_id, person.us_name, person.us_username, person.us_password, person.ut_id
                    from (select us_id
                          from "Reservation"
                          where "re_startTime" = %s
                            and "re_date" = %s
                            and ro_id = %s) as reserver,
                         "User" as person
                    where person.us_id = reserver.us_id;"""
        values = (
            start_time,
            date,
            ro_id
        )
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        self.conn.close()
        cursor.close()
        return result

    # Returns a tuple of start and end time as a default for a meeting made up of
    # attendees who will go at a certain date
    def get_available_time_attendees(self, date, attendees):
        cursor = self.conn.cursor()
        query = """ SELECT ts.start, ts.finish
                    FROM (SELECT min(start) AS start, max(finish) AS finish
                          FROM ((
                                    SELECT "re_startTime" AS start, "re_endTime" AS finish, us_id
                                    FROM "Reservation"
                                             NATURAL INNER JOIN "Meeting"
                                             NATURAL INNER JOIN "Attending"
                                    WHERE re_date = %s
                                ) UNION
                                (
                                    SELECT "uu_startTime" AS start, "uu_endTime" AS finish, us_id
                                    FROM "UserUnavailability"
                                    WHERE uu_date = %s
                                )) AS schedule
                          WHERE us_id IN %s) AS us,
                         (SELECT sslots.slots AS start, eslots.slots AS finish
                          FROM (SELECT row_number() OVER (ORDER BY slots) AS sid, slots::time
                                FROM generate_series(TIMESTAMP '1969-12-30',
                                                     TIMESTAMP '1969-12-31 23:40:00',
                                                     INTERVAL '20 min') t(slots)) AS sslots,
                               (SELECT row_number() OVER (ORDER BY slots) AS sid, slots::time
                                FROM generate_series(TIMESTAMP '1969-12-30 00:20:00',
                                                     TIMESTAMP '1969-12-31',
                                                     INTERVAL '20 min') t(slots)) AS eslots
                          WHERE sslots.sid = eslots.sid) AS ts
                    WHERE (ts.start < us.start OR ts.start >= us.finish)
                    AND (ts.finish <= us.start OR ts.finish > us.finish)
                    ORDER BY ts.start;"""
        values = (
            date,
            date,
            attendees
        )
        cursor.execute(query, values)
        result = [row for row in cursor]
        cursor.close()
        self.conn.close()
        cursor.close()
        return result

    def busiest_hour(self):
        cur = self.conn.cursor()
        query = """select "re_startTime", "re_endTime", count("re_startTime")
                    from "Reservation" group by "re_startTime", "re_endTime"
                    order by count("re_startTime") DESC LIMIT 5"""
        cur.execute(query)
        rooms_list = [row for row in cur]
        cur.close()
        return rooms_list

    def dispose(self):
        self.conn.close()
