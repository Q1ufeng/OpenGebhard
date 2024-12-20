#import psycopg2
from SQL_generator import SQL_generator

def SQL_conductor ():

#    conn = psycopg2.connect(database="postgres", user="postgres", password="PGshujing40", host="localhost", port="5432")

#    cursor = conn.cursor()

    SQLs = SQL_generator(10,30,5000)

#    for sql in SQLs:
#        cursor.execute(sql)

#    conn.commit()

#    conn.close()
