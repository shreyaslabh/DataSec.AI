from flask import Flask
from flask_mail import Mail,Message
import psycopg2
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'


mail_settings = {
	  "SECRET_KEY": 'super-secret',
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'dms.suth@gmail.com',
    "MAIL_PASSWORD": 'lockdown123'
}

app.config.update(mail_settings)


#con = psycopg2.connect(database="datamask", user = "postgres", password = "Admin123", host = "127.0.0.1")


con = psycopg2.connect(user="postgres",
                                  password="shreyas",
                                  host="localhost",
                                  port="5432",
                                  dbname="data-masking-microservice")



# con = psycopg2.connect(user="datamaskuser",
#                                   password="datamaskuser123",
#                                   host="35.245.71.89",
#                                   port="5432",
#                                   dbname="datamask")

#rconn = redis.Redis(host = '10.175.91.227', port = 6379)

try:
	#rconn = redis.Redis(host = '10.149.17.4', port = 6379)  # Sutherland Redis
  #rconn = redis.Redis(host = '10.179.117.59', port = 6379)
	rconn = redis.Redis(host = 'localhost', port = 6379)
except Exception as e:
	print("Redis Connection Error : ",e)

#rconn = redis.Redis('localhost')

from WebApp import routes

