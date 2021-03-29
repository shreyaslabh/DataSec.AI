import psycopg2
import datetime
import pickle
from WebApp import putActiveServicesRedis as red


con = psycopg2.connect(user="postgres",
                                  password="shreyas",
                                  host="localhost",
                                  port="5432",
                                  dbname="dm2")



cur = con.cursor()

cur.execute("SELECT * FROM fsets WHERE fsetid = %s",(2,))
fsets = cur.fetchall()

print(fsets)

# fids = [j for i,j,_ in fsets]

red.activeServices()


