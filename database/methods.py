from config import connection
from objects.owner import Owner


class OwnerAlreadyExists(Exception):
    pass


class OwnerDoesntExist(Exception):
    pass


def insert_owner(name, email, city, zip_code, phone, cat, info, img_url):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM owners where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            raise OwnerAlreadyExists()
        else:
            query = f"INSERT INTO owners (name, email, city, zip_code, phone, categories, info, img_url) VALUES ('{name}', '{email}', '{city}', '{zip_code}', '{phone}', '{cat}', '{info}', '{img_url}')"
            cursor.execute(query)
            connection.commit()
        query = f"SELECT * FROM owners where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["id"]


def get_owners(cat=None):
    with connection.cursor() as cursor:
        if cat is None:
            query = f"SELECT * FROM owners"
        else:
            query = f"SELECT * FROM owners where categories = '{cat}'"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
        
def get_items(owner_id):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM items  where owner_id = '{owner_id}'"
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


def insert_item(owner_id, price, info, name, img_url):
    with connection.cursor() as cursor:
        query = f"INSERT INTO items (owner_id, price, info, img_url, name) VALUES ({owner_id}, {price}, '{info}'" \
                f", {img_url}, '{name}')"
        cursor.execute(query)
    connection.commit()


def insert(owner, items):
    try:
        owner_id = insert_owner(owner.name, owner.email, owner.city, owner.zip_code, owner.phone, owner.cat, owner.info, owner.img_url)
        for item in items:
            img_url = insert_image(owner_id, item.img_url)
            insert_item(owner_id, item.price, item.info, item.name, img_url)
    except OwnerAlreadyExists as e:
        raise

'''
owner_id = insert_owner("aa2", "b", 1, "h")
img_url = insert_image(owner_id, "https://images.fairtrade.net/product/infosite_flowers_18043_1440.jpg")
insert_item(owner_id, 2, "jj", img_url)
#print(get_owners())
'''
