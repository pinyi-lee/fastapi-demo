from dbutils.pooled_db import PooledDB
import pymysql

from config.config import get_config as config

pool = PooledDB(
    creator = pymysql,
    maxconnections = 3,
    database = "taipei_day_trip",
    user = config().database_user,
    password = config().database_password,
    host = config().database_host,
    port = config().database_port
)

def get_db_connection_pool():
    try:
        connetion = pool.connection()
        print("Database connect successful")
    except Exception as e:
        print("Database connect failed :", e)

    return connetion