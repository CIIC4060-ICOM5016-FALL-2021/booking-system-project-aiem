# I think we can eliminate this file - Emma

class User:
    def __init__(self, uid, name, username, password):
        self.uid = uid
        self.name = name
        self.username = username
        self.password = password


class Room:
    def __init__(self, rid, name, location):
        self.rid = rid
        self.name = name
        self.location = location


class Reservation:
    def __init__(self, resid, date, starttime, endtime):
        self.resid = resid
        self.date = date
        self.starttime = starttime
        self.endtime = endtime

