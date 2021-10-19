import psycopg2


class Database:
    def create_db_connection(self):
        db = psycopg2.connect(dbname='d5gkt64aa114el', user='seqmujfcvmcqhh', host='ec2-18-206-20-102.compute-1.amazonaws.com', password='91bad46d3e7e5df3ff53d48a41e27fd9ac827acae2b75d2eb12b9722f939e860')
        return db

    def close_db_connection(db):
        db.close()