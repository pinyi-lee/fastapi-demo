import pymysql

from database.db import get_db_connection_pool
from model.attraction import Attraction, AttractionListRes
from model.error import ServiceError, AttractionNotFoundError, DBError

def get_attraction_list(page , keyword = None) -> AttractionListRes | ServiceError:
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection_pool()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
    
        if keyword:
            count_sql = "SELECT COUNT(*) as total from location where name LIKE %s OR MRT = %s"
            cursor.execute(count_sql , ('%' + keyword + '%' , keyword ))
        else:
            count_sql = "SELECT COUNT(*) as total from location"
            cursor.execute(count_sql)

        total_records = cursor.fetchone()["total"]
        offset = page * 12

        if keyword:
            sql = "select id, name, category, description, address, transport,  mrt, CAST(lat AS DOUBLE) AS lat, CAST(lng AS DOUBLE) AS lng from location where name LIKE %s OR MRT = %s LIMIT 12 OFFSET %s"
            cursor.execute(sql , ('%' + keyword + '%' , keyword  , offset))
        else:
            sql = "select id, name, category, description, address, transport, mrt, CAST(lat AS DOUBLE) AS lat, CAST(lng AS DOUBLE) AS lng from location LIMIT 12 OFFSET %s"
            cursor.execute(sql , (offset))
        
        locations = cursor.fetchall()

        location_ids =[]
        for location in locations:
            location_ids.append(location['id'])

        image_sql = "select location_id, images FROM URL_file where location_id IN ({format_string})"
        cursor.execute(image_sql , tuple(location_ids))
        image_results = cursor.fetchall()

        image_map ={}
        for image_result in image_results:
            location_id = image_result["location_id"]
            image = image_result["images"]
            if location_id not in image_map:
                image_map[location_id] = []
            image_map[location_id].append(image)

        attraction_list =[]
        for location in locations:
            attraction = Attraction(
                id = location["id"],
                name = location["name"],
                category = location["category"],
                description = location["description"],
                address = location["address"],
                transport = location["transport"],
                mrt = location["mrt"] if location["mrt"] is not None else "",
                lat = location["lat"],
                lng = location["lng"],
                images = image_map[location["id"]],
            )
            attraction_list.append(attraction)

        nextPage = None
        if offset + 12 < total_records:
            nextPage = page + 1 

        return AttractionListRes(
            nextPage = nextPage,
            data = attraction_list,
        )
            
    except Exception as e:
        print("get attraction list database error, error message:" , e)
        return DBError()
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def get_attraction(id: int) -> Attraction | ServiceError:
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection_pool()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "select id, name, category, description, address, transport, mrt, CAST(lat AS DOUBLE) AS lat, CAST(lng AS DOUBLE) AS lng from location where id = %s"
        cursor.execute(sql ,(id, ))
        result = cursor.fetchone()

        if result == None | len(result) == 0:
            return AttractionNotFoundError()
        
        image_urls = []
        if result:
            image_sql = "select images from URL_file where location_id = %s"
            cursor.execute(image_sql , (id, ))
            results = cursor.fetchall()
            image_urls = [result["images"] for result in results]
        
        return Attraction(
            id = result["id"],
            name = result["name"],
            category = result["category"],
            description = result["description"],
            address = result["address"],
            transport = result["transport"],
            mrt = result["mrt"] if result["mrt"] is not None else "",
            lat = result["lat"],
            lng = result["lng"],
            images = image_urls,
        )
    
    except Exception as e:
        print("get attraction database error, error message:" , e)
        return DBError()
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()