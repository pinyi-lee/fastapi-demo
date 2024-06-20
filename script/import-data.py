import json
import pymysql
import re

db =  pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "test",
    password = "test",
    db = "taipei_day_trip"
)

cursor = db.cursor()

insert_location_sql = """
insert ignore into location(id,name,mrt,SERIAL_NO,address,RowNumber,rate,transport,date,lng,lat,category,MEMO_TIME,description) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

insert_URL_file_sql = """
insert ignore into URL_file( location_id , images) values(%s,%s)
"""

if __name__ == '__main__':
    try:
        with open('taipei-attractions.json') as data_details:
            data = json.load(data_details)
        data_results = data["result"]["results"]

        cursor.execute("BEGIN;")
        for item in data_results:
            cursor.execute(insert_location_sql , (
                item["_id"] , item["name"], item["MRT"], item["SERIAL_NO"] , item["address"],
                item["RowNumber"] , item["rate"] , item["direction"] , item["date"],
                item["longitude"] , item["latitude"] , item["CAT"] , item["MEMO_TIME"] ,
                item["description"]
            ))
            if "file" in item:
                data_files = item["file"]
                urls_seperate = re.findall(r'https?://[^\s]+?\.(?:jpg|JPG|png|PNG)' , data_files)
            for url in urls_seperate:
                cursor.execute(insert_URL_file_sql , (
                    item["_id"] , url
                ))
        db.commit()
    except Exception as e:
        print("creating tables error, error message:" , e)
        db.rollback()
    finally:
        db.close()
        cursor.close()