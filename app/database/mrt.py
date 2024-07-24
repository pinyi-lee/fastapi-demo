import pymysql
from typing import List

from app.database.db import DBManager
from app.model.error import ServiceError, DBError
from app.util.logger import LoggerManager

def get_mrt_list() -> List[str] | ServiceError:
    connection = None
    cursor = None
    
    try:
        connection = DBManager.get_db()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "select mrt from location where mrt is not null group by mrt order by count(*) DESC;"
        cursor.execute(sql ,)
        results = cursor.fetchall()
    
        mrt_list = [result["mrt"] for result in results]
        return mrt_list
        
    except Exception as e:
        LoggerManager.error("get mrt list database error, error message:" , e)
        return DBError()
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()