from pymongo import MongoClient


def storage_data(data):
    DBNAME = 'mydb'
    DBUSERNAME = 'tass'
    DBPASSWORD = 'liehu'
    DB = '192.168.0.15'
    PORT = 65521
    db_conn = MongoClient(DB, PORT)
    na_db = getattr(db_conn, DBNAME)
    na_db.authenticate(DBUSERNAME, DBPASSWORD)
    c = na_db.cvedatas
    c.update({"description": data['description']}, {'$set': data}, True)
	
	