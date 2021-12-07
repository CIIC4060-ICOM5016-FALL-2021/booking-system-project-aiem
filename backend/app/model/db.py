import psycopg2

from backend.app.config.dbconfig import aiem_config


# Creates connection to database for easier legibility in DAO classes
class Database:
    def __init__(self):
        self.connection = psycopg2.connect("dbname=%s user=%s host=%s password=%s port=%s"
                                           % (aiem_config['dbname'], aiem_config['user'],
                                              aiem_config['host'], aiem_config['password'],
                                              aiem_config['port']))

    def close(self):
        self.connection.close()
