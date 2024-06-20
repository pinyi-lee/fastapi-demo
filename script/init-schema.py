import pymysql

db =  pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "test",
    password = "test",
    db = "taipei_day_trip"
)

cursor = db.cursor()

create_location_sql = """
CREATE TABLE IF NOT EXISTS location(
    id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    mrt VARCHAR(255),
    SERIAL_NO VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    RowNumber VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    rate BIGINT NOT NULL,
    transport TEXT NOT NULL,
    date DATETIME NOT NULL,
    lng DECIMAL(10,6) NOT NULL,
    lat DECIMAL(10,6) NOT NULL,
    MEMO_TIME VARCHAR(255),
    description TEXT NOT NULL,
    PRIMARY KEY (id)
);
"""

create_url_file_sql = """
CREATE TABLE IF NOT EXISTS URL_file(
    file_id BIGINT NOT NULL AUTO_INCREMENT,
    location_id BIGINT NOT NULL,
    images VARCHAR(255) NOT NULL,
    PRIMARY KEY (file_id),
    FOREIGN KEY (location_id) REFERENCES location(id)
);
"""

create_member_table_sql = """
        CREATE TABLE IF NOT EXISTS member (
        id char(36) primary key,
        name varchar(255) not null,
        password varchar(255) not null,
        email varchar(255) unique not null
);
"""

if __name__ == '__main__':
    try:
        cursor.execute("BEGIN;")
        cursor.execute(create_location_sql)
        cursor.execute(create_url_file_sql)
        cursor.execute(create_member_table_sql)
        db.commit()
    except Exception as e :
        print("creating tables error, error message:" , e)
        db.rollback()
    finally:
        db.close()
        cursor.close()