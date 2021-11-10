import psycopg2
from app.model.db import Database

class GlobalStatistic:

    def __init__(self):
        self.db = Database()

    def busiest_hours(self):
        cur = self.db.connection.cursor()
        query= """SELECT * FROM "Room";"""
        return 5
