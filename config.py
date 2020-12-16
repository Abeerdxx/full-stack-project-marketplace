import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    db="business_db",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
