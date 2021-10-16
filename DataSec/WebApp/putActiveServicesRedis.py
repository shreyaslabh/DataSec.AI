from WebApp import app,con,rconn
import psycopg2
import redis
import pickle

def activeServices():
	#con = psycopg2.connect(dbname='datamasking',user='postgres',host='localhost',password='shreyas')

	"""con = psycopg2.connect(user="shreyas",
                                  password="shreyas",
                                  host="34.70.46.231",
                                  port="5432",
                                  dbname="dm")"""


	"""con = psycopg2.connect(user="datamaskuser",
									                                  password="datamaskuser123",
									                                  host="35.245.71.89",
									                                  port="5432",
									                                  dbname="datamask")"""
	
	cur = con.cursor()

	servicedetails = []


	cur.execute("SELECT * FROM services WHERE status = %s",('active',))
	services = cur.fetchall()

	for service in services:
		sid = service[0]

		cur.execute("SELECT * FROM servicedetails WHERE sid = %s",(sid,))
		s = cur.fetchall()
		urls = []
		for i in s:
			urls.append(i[2])
		#print(urls)

		cur.execute("SELECT * FROM fsets WHERE fsetid = %s",(sid,))
		fsets = cur.fetchall()
		fids = [j for i,j in fsets]
		#print(fids)

		fdetails = []

		for fid in fids:
			cur.execute("SELECT * FROM filters WHERE fid = %s",(fid,))
			f = cur.fetchall()[0]
			#print(f)
			#fdetails.append([f[4].replace("\\",""),f[5],f[6]])
			fdetails.append([f[4],f[5],f[6],f[7]])

		for filter in fdetails:
			cur.execute("SELECT mname FROM masks WHERE mid = %s",(filter[2],))
			m = cur.fetchall()[0][0]
			#print(m)
			filter[2] = m

		#print(fdetails)
		service_dict = {'sid' : sid , 'urls' : urls , 'filters' : fdetails}
		servicedetails.append(service_dict)

	#print(servicedetails)

	servicedetails_p = pickle.dumps(servicedetails)
	rconn.set("activeServices",servicedetails_p)

	#return(servicedetails)
"""
aS = activeServices()
aS_p = pickle.dumps(aS)


conn = redis.Redis('localhost')

conn.set("activeServices",aS_p)

aS_rp = conn.get("activeServices")

print(pickle.loads(aS_rp))"""




