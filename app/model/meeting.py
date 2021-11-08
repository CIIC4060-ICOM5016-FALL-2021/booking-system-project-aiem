from app.model.db import Database

#Handles Meeting/meeting attending DAO Operations
class MeetingDAO:

#-Reusable SQL Snippets------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    GET_MEETING = """select mt_id, mt_name, mt_desc, re_id, re_date, "re_startTime", "re_endTime", us_id, us_name, ro_id, ro_name 
                     from "Meeting" natural inner join "Reservation" natural inner join "User" natural inner join "Room"
                  """
    ORDER_DATE_DESCENDING = """ order by re_date desc, "re_startTime" desc;"""
    
    #order by snippets which may or may not be used later (in fact they could be used elsewhere :thinking:)
    ORDER_BY_X = " order by %s" #these snippets are only usable for ordering by one column pero oops
    ASC = ";" # Since asc is default we can just add a semicolon because yes
    DESC = " desc;" # Specify desc then continue 

    def __init__(self):
        self.conn = Database().connection #this is so I don't have to radically alter the code


#-Gets------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #Gets all meetings (along with some additional linked information including linked Reservation details, Who reserved it (User ID/Name), and where it is reserved (Room ID/Name))
    def getAllMeeting(self):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + self.ORDER_DATE_DESCENDING
        cursor.execute(query) 
        result = []
        for row in cursor:
            result.append(row)
        return result

        #Gets a specified meeting
    def getMeetingById(self, mt_id):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + " where mt_id = %s;" #since we only get one we don't need to order
        cursor.execute(query, (mt_id,))
        result = cursor.fetchone()
        return result
        
        #Gets a list of every user that is attending a given meeting
    def getMeetingAttending(self, mt_id):
        cursor = self.conn.cursor()
        query = """select us_id, us_name, us_username 
                   from "User" natural inner join "Attending" 
                   where mt_id=%s;"""
        cursor.execute(query, (mt_id,))
        result = cursor.fetchone()
        return result

        #Gets meetings reserved by given reserver ordered by date descending
    def getMeetingsByReserver(self, us_id):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + " where us_id = %s" + self.ORDER_DATE_DESCENDING
        cursor.execute(query, (us_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

        #Gets meeting reserved by given room and date
    def getMeetingsForRoomOn(self, ro_id, re_date):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + " where ro_id = %s and re_date = %s" + self.ORDER_DATE_DESCENDING
        cursor.execute(query, (ro_id,re_date,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMeetingsForUserOn(self, us_id, re_date):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + """ where re_date  = %s and mt_id IN
                                    (select mt_id from "Meeting" natural inner join "Attending" 
                                    where us_id = %s)""" + self.ORDER_DATE_DESCENDING
        cursor.execute(query, (re_date,us_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

        #Gets meeting that is occurring at a given time in a given room
    def getMeetingInRoomAtTime(self, ro_id, date, time):
        cursor = self.conn.cursor()
        query = self.GET_MEETING + """ where ro_id = %s and re_date = %s and "re_startTime" < %s and "re_endTime" > %s;"""
        cursor.execute(query, (ro_id,date,time,time,))
        result = cursor.fetchone()
        return result

    #def getAvailableRoomAtTimeRange(self, date, start, end):
        #get the rooms that are unavailable #this belongs on the room DAO I think
     #   return null

    #Check if a user is busy during a certain time range (IE If the user is busy or unavailable). Used to check if we can add them as attending
    def checkUserBusy(self, us_id, date, start, end):
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
                        (startp < %s and endp > %s) or --Checks if the given start is between the start and endtime of an unavailability period
                        (startp < %s and endp > %s) or --Checks if the given end is between the start and endtime of an unavailability period
                        (startp > %s and endp < %s) --Checks if an existing unavailability period exists between the given start and end times
                    )
                ; 
        """
        cursor.execute(query, (us_id,us_id,date,start,start,end,end,start,end,))
        result = cursor.fetchone()
        return result[0] >= 1 # if there's 1 or more in these things, the user is busy 

    #Check if a meeting is possible (IE The reserver is not busy/unavailable and the room is not busy/unavailable). Used to check if we should create a meeting or not
    def checkMeetingBusy(self, us_id, ro_id, date, start, end):
        cursor = self.conn.cursor()
        query = """select count(*) from (
                     select "re_startTime" as startp, "re_endTime" as endp, re_date as datep --Times that are unavailable because either the user is in a meeting or the room is busy
                     from "Meeting" natural inner join "Reservation"
                     where mt_id in (select mt_id from "Attending" where us_id=%s) or ro_id = %s
                     union ( --User unavailable times just because they said so
                         select "uu_startTime" as startp, "uu_endTime" as endp, uu_date as datep
                         from "UserUnavailability"
                         where us_id = %s )
                     union ( --Room is unavailable because the department said so
                        select "ru_startTime" as startp, "ru_endTime" as endp, ru_date as datep
                        from "RoomUnavailability"
                        where ro_id=%s )
                     ) as UnavailableTimes
                    where datep = %s and (
                        (startp < %s and endp > %s) or --Checks if the given start is between the start and endtime of an unavailability period
                        (startp < %s and endp > %s) or --Checks if the given end is between the start and endtime of an unavailability period
                        (startp > %s and endp < %s) --Checks if an existing unavailability period exists between the given start and end times
                    )
                ;"""
        cursor.execute(query, (us_id,ro_id,us_id,ro_id,date,start,start,end,end,start,end,))
        result = cursor.fetchone()
        return result[0] >= 1 # if there's 1 or more in these things, the user or the room is busy or unavailable
        

#-Insert------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def insertMeeting(self, mt_name, mt_desc, re_id):
        cursor = self.conn.cursor()
        query = """insert into "Meeting" (mt_name, mt_desc, re_id) values (%s,%s,%s) returning mt_id;"""
        cursor.execute(query, (mt_name, mt_desc, re_id,))
        mt_id = cursor.fetchone()[0]
        self.conn.commit()
        return mt_id

    #This should be done BEFORE insert meeting
    def insertReservaiton(self, re_date, re_startTime, re_endTime, us_id, ro_id):
        cursor = self.conn.cursor()
        query = """insert into "Reservation" (re_date, "re_startTime","re_endTime",us_id,ro_id) values (%s,%s,%s,%s,%s) returning mt_id;"""
        cursor.execute(query, (re_date, re_startTime, re_endTime, us_id, ro_id,))
        re_id = cursor.fetchone()[0]
        self.conn.commit()
        return re_id

    #Does both in order
    def insertEverythingForMeeting(self, mt_name, mt_desc, re_date, re_startTime, re_endTime, us_id, ro_id):
        re_id = self.insertReservaiton(re_date, re_startTime, re_endTime, us_id, ro_id) #Create the reservation
        mt_id = self.insertMeeting(mt_name, mt_desc, re_id) #Create the meeting
        self.insertAttending(mt_id, us_id) # Register the host as attending as well
        return mt_id #finally we're done after three requests que lindo

    #Adds an attending user
    def insertAttending(self, mt_id, us_id):
        cursor = self.conn.cursor()
        query = """insert into "Attending" (mt_id,us_id) values (%s,%s);"""
        cursor.execute(query, (mt_id,us_id,))
        # re_id = cursor.fetchone()[0] #Here we don't actually need to fetch anything
        self.conn.commit()
        return True



#-Update------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def updateMeeting(self, mt_id, mt_name, mt_description):
        cursor = self.conn.cursor()
        query= """update "Meeting" set mt_name=%s, 
                                       mt_desc=%s 
                  where mt_id=%s;"""
        cursor.execute(query, (mt_name,mt_description,mt_id,))
        self.conn.commit()
        return True

    def updateMeetingReservation(self, mt_id, re_date, re_startTime, re_endTime, ro_id):
        cursor = self.conn.cursor()
        query= """update "Reservation" set re_date = %s, 
                                           "re_startTime" = %s, 
                                           "re_endTime" = %s, 
                                           ro_id = %s 
                  where re_id = (
                        select re_id 
                        from "Meeting" 
                        where mt_id=%s
                );"""
        cursor.execute(query, (re_date,re_startTime,re_endTime,ro_id,mt_id,))
        self.conn.commit()
        return True

    def updateReservation(self, re_id, re_date, re_startTime, re_endTime, ro_id):
        cursor = self.conn.cursor()
        query= """update "Reservation" set re_date = %s, 
                                           "re_startTime" = %s, 
                                           "re_endTime" = %s, 
                                           ro_id = %s 
                  where re_id = %s;"""
        cursor.execute(query, (re_date,re_startTime,re_endTime,ro_id,re_id,))
        self.conn.commit()
        return True

    #There is no update for attending. You either create it or delete it. That's it

#-delete------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #Delete just the meeting
    def deleteMeetingOnly(self, mt_id):
        cursor = self.conn.cursor()
        query = """delete from "Meeting" where mt_id=%s;"""
        cursor.execute(query,(mt_id,))
        
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0

    #Delete's a meeting's tied reservation
    def deleteReservationOnly(self, re_id):
        cursor = self.conn.cursor()
        query = """delete from "Reservation" where re_id = %s"""
        cursor.execute(query,(re_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows !=0


    #Delete a specific attender
    def deleteAttending(self, mt_id, us_id):
        cursor = self.conn.cursor()
        query = """delete from "Attending" where mt_id=%s and us_id=%s;"""
        cursor.execute(query,(mt_id,us_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows !=0
    
    #Delete all those attending a certain meeting
    def deleteAllAttending(self, mt_id):
        cursor = self.conn.cursor()
        query = """delete from "Attending" where mt_id=%s;"""
        cursor.execute(query,(mt_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows !=0

    def deleteMeeting(self, mt_id): #We should've REALLY Just made meeting and reservation as the same thing pero oops!!!!
        if not self.deleteAllAttending(mt_id): return False #delete all the attending
        re_id = self.getMeetingById(mt_id)[3] #get the reservation ID god what a dumb idea this was oopsie dasy! :)
        if not self.deleteMeetingOnly(mt_id): return False #delete the meeting holder
        return self.deleteReservationOnly(re_id) #delete the reservation
       

