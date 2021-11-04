from app.model.db import Database


# Contains all the methods necessary for operations in the Room table
class RoomsDAO:
    def __init__(self):
        self.db = Database()

    def get_all_rooms(self):
        cur = self.db.connection.cursor()
        query = """SELECT ro_id, ro_name, ro_location, rt_id FROM "Room";"""
        cur.execute(query)
        rooms_list = [row for row in cur]
        return rooms_list

    def create_room(self):
        return

    def get_room(self):
        return

    def update_room(self):
        return

    def delete_room(self):
        return
