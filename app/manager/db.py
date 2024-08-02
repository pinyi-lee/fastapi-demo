from dbutils.pooled_db import PooledDB
import pymysql

from app.manager.config import ConfigManager
from app.manager.logger import LoggerManager

class DBManager:
    _db_instance = None

    @classmethod
    def init_db(cls) -> None:
        try:
            if cls._db_instance is None:
                cls._db_instance = PooledDB(
                                        creator = pymysql,
                                        maxconnections = 3,
                                        database = ConfigManager.get_config().database_name,
                                        user = ConfigManager.get_config().database_user,
                                        password = ConfigManager.get_config().database_password,
                                        host = ConfigManager.get_config().database_host,
                                        port = ConfigManager.get_config().database_port
                                    )
            connetion = cls._db_instance.connection()
            connetion.close()
        except Exception as e:
                raise RuntimeError(f"Init DB Fail, Error: {e}")
    
    @classmethod
    def get_db(cls) -> pymysql.Connection:
        try:
            connetion = cls._db_instance.connection()
            LoggerManager.debug("Database connect successful")
            return connetion
        except Exception as e:
            LoggerManager.error(f"Database connect failed :{e}")
        
    @classmethod
    def close_db(cls) -> None:
        if cls._db_instance is not None:
            cls._db_instance.close()
            cls._db_instance = None