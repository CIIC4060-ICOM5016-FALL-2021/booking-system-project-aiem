from app import app
from app.db import *


@app.route('/')
def home():
    return 'Welcome to team AIEMs Database Semester Project'


@app.route('/test')
def create():

    db = Database
    con = db.create_db_connection()
    cur = con.cursor()
    cur.execute("CREATE TABLE accounts(user_id serial PRIMARY KEY,username VARCHAR ( 50 ), email VARCHAR ( 255 ))")
    con.commit()

    return "Table created"