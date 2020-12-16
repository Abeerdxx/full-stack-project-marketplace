from config import connection


class OwnerAlreadyExists(Exception):
    pass


class OwnerDoesntExist(Exception):
    pass


def insert_owner(name, email, phone, info):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM owners where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            raise OwnerAlreadyExists()
        else:
            query = f"INSERT INTO owners (name, phone, email, info) VALUES ('{name}', '{phone}', '{email}', '{info}')"
            cursor.execute(query)
            connection.commit()
        query = f"SELECT * FROM owners where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["id"]


def get_owners():
    with connection.cursor() as cursor:
        query = f"SELECT * FROM owners"
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def insert_image(owner_id, img_url):
    with connection.cursor() as cursor:
        query = f"INSERT INTO images (owner_id, img_url) VALUES ({owner_id}, '{img_url}')"
        cursor.execute(query)
        connection.commit()
        query = f"SELECT id FROM images where owner_id = '{owner_id}' and img_url = '{img_url}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["id"]

'''
for item in items:
    insert_item(item)
on inserting the owner, should also get an item (class or dict), 
'''


def insert_item(owner_id, price, info, img_id):
    with connection.cursor() as cursor:
        query = f"INSERT INTO items (owner_id, price, info, img_id) VALUES ({owner_id}, {price}, '{info}', {img_id})"
        cursor.execute(query)
    connection.commit()

'''
owner_id = insert_owner("aa2", "b", 1, "h")
img_id = insert_image(owner_id, "https://images.fairtrade.net/product/infosite_flowers_18043_1440.jpg")
insert_item(owner_id, 2, "jj", img_id)
#print(get_owners())
'''