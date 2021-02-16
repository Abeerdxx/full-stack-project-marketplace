from config import connection
from database.password_hasher import check_password


class OwnerAlreadyExists(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class OwnerDoesntExist(Exception):
    pass


def get_user(email):
    result = None
    with connection.cursor() as cursor:
        query = f"SELECT * FROM users where email = '{email}'"
        cursor.execute(query)
        result = cursor.fetchone()
    return result


def insert_user(name, email, city, zip_code, phone, img_url, password):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM users where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            raise UserAlreadyExists()
        else:
            query = f"INSERT INTO users (name, email, city, zip_code, phone, img_url, pass_hash) VALUES " \
                    f"('{name}', '{email}', '{city}', '{zip_code}', '{phone}', '{img_url}', '{password}')"
            cursor.execute(query)
            connection.commit()
        query = f"SELECT * FROM users where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["id"]


def insert_owner(name, email, city, zip_code, phone, img_url, cat, info, password):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM owners where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            raise OwnerAlreadyExists()
        else:
            password = '"' + password + '"'
            query = f"INSERT INTO owners (name, email, city, zip_code, phone, categories, info, img_url, pass_hash) VALUES " \
                    f"('{name}', '{email}', '{city}', '{zip_code}', '{phone}', '{cat}', '{info}', '{img_url}', {password})"
            cursor.execute(query)
            connection.commit()
        query = f"SELECT * FROM owners where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["id"]


def insert_new(obj, type_):  # type_ is binary: 0 -> business owner, 1 -> client
    return_em = obj.email
    with connection.cursor() as cursor:
        result = get_user(obj.email)
        if result is not None:
            raise UserAlreadyExists()
        else:
            password = '"' + obj.hashed_pass + '"'
            if type_ == 0:
                query = f"INSERT INTO owners (email, categories, info) VALUES " \
                        f"('{obj.email}', '{obj.cat}', '{obj.info}')"
                cursor.execute(query)
                query = f"INSERT INTO users (owner, name, email, city, zip_code, phone, type, img_url, pass_hash) VALUES " \
                        f"('{return_em}', '{obj.name}', '{obj.email}', '{obj.city}', '{obj.zip_code}', '{obj.phone}', " \
                        f"{type_}, '{obj.img_url}'," \
                        f" {password})"
            else:
                query = f"INSERT INTO users (name, email, city, zip_code, phone, type, img_url, pass_hash) VALUES " \
                        f"('{obj.name}', '{obj.email}', '{obj.city}', '{obj.zip_code}', '{obj.phone}', " \
                        f"{type_}, '{obj.img_url}'," \
                        f" {password})"
            cursor.execute(query)
    connection.commit()
    return return_em


def get_owners(cat=None):
    with connection.cursor() as cursor:
        if cat is None:
            query = f"select * from users join owners on owners.email=users.email"
        else:
            query = f"select * from users join owners on owners.email=users.email where owners.categories = '{cat}'"
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_owner(email):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM users where email = '{email}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result["type"] == '0':
            query = f"SELECT * FROM owners join users on owners.email=users.owner where users.owner = '{email}'"
            cursor.execute(query)
            result = cursor.fetchone()
        return result


def get_items(owner_em):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM items where owner = '{owner_em}'"
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_categories():
    with connection.cursor() as cursor:
        query = f"SELECT categories FROM owners"
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def insert_image(owner_em, img_url):
    with connection.cursor() as cursor:
        query = f"INSERT INTO images (owner, img_url) VALUES ('{owner_em}', '{img_url}')"
        cursor.execute(query)
        connection.commit()


def insert_item(owner_em, price, info, name, img_url):
    with connection.cursor() as cursor:
        query = f"INSERT INTO items (owner, price, info, img_url, name) VALUES ('{owner_em}', {price}, '{info}'" \
                f", '{img_url}', '{name}')"
        cursor.execute(query)
    connection.commit()


def insert(person, type_, items=None):
    try:
        if type_ == 0:
            # owner_id = insert_owner(owner.name, owner.email, owner.city, owner.zip_code, owner.phone, owner.img_url,
            #                         owner.cat,
            #                         owner.info, owner.hashed_pass)
            owner_em = insert_new(person, 0)
            for item in items:
                insert_image(owner_em, item.img_url)
                insert_item(owner_em, item.price, item.info, item.name, item.img_url)
        else:
            insert_new(person, 1)
    except UserAlreadyExists:
        raise


def is_owner(email, password):
    result = get_user(email)
    if result is not None:
        return check_password(password, result["pass_hash"])
    return OwnerDoesntExist
