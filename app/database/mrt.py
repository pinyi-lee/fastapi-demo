import pymysql
from typing import List

from database.db import get_db_connection_pool
from model.error import ServiceError, DBError

def get_mrt_list() -> List[str] | ServiceError:
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection_pool()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "select mrt from location where mrt is not null group by mrt order by count(*) DESC;"
        cursor.execute(sql ,)
        results = cursor.fetchall()
    
        mrt_list = [result["mrt"] for result in results]
        return mrt_list
        
    except Exception as e:
        print("get mrt list database error, error message:" , e)
        return DBError()
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()