import psycopg2
import redis
import pickle
import logging
import datetime
#from presidio_analyzer import AnalyzerEngine

# rconn = redis.Redis(host = '10.149.17.4', port = 6379) # Sutherland Redis
#rconn = redis.Redis(host = '10.179.117.59', port = 6379)
rconn = redis.Redis('localhost')

#con = psycopg2.connect(dbname='datamasking',user='postgres',host='localhost',password='shreyas')

"""con = psycopg2.connect(user="shreyas",
                                  password="shreyas",
                                  host="34.70.46.231",
                                  port="5432",
                                  dbname="dm")"""

con = psycopg2.connect(user="postgres",
                                  password="shreyas",
                                  host="localhost",
                                  port="5432",
                                  dbname="data-masking-microservice")


logging.basicConfig(filename="Logs/logs.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')

logger=logging.getLogger()

logger.setLevel(logging.INFO)

#analyzer = AnalyzerEngine()

def activeServices():
	#con = psycopg2.connect(dbname='datamasking',user='postgres',host='localhost',password='shreyas')

	activeServices_p = rconn.get("activeServices")

	try:
		return(pickle.loads(activeServices_p))
	except TypeError:
		putActiveServicesIntoRedis()
		activeServices()



def putIntoSessionMasks(sid,pairs):

	session_mask = getSessionMasks()
	session_mask[sid] = pairs
	session_mask = pickle.dumps(session_mask)
	#rconn.delete('session_mask',session_mask)
	rconn.set('session_mask',session_mask)


def putIntoHitServices(sid):

	hit_service_id = getHitServices()
	hit_service_id.append(sid)
	hit_service_id = pickle.dumps(hit_service_id)
	#rconn.delete('hit_service_id',hit_service_id)
	rconn.set('hit_service_id',hit_service_id)


def getSessionMasks():

	session_mask = rconn.get("session_mask")
	try:
		return(pickle.loads(session_mask))
	except TypeError:
		return({0:[['0','0']]})


def getHitServices():

	hit_service_id = rconn.get("hit_service_id")
	try:
		return(pickle.loads(hit_service_id))
	except TypeError:
		return([0])


def putLogs(sid,lognature,log):
	
	
		cur = con.cursor()
		timstamp = datetime.datetime.now().date()
		log = pickle.dumps(log)
		cur.execute("INSERT INTO logs(logid,logdate,lognature,logdata) VALUES(%s,%s,%s,%s)",(sid,timstamp,lognature,log))
		con.commit()



def putActiveServicesIntoRedis():
	
	cur = con.cursor()

	servicedetails = []

	cur.execute("SELECT * FROM services WHERE status = %s",('active',))
	services = cur.fetchall()

	try:
		print(services[0])

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
			fids = [j for i,j,_ in fsets]
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

		servicedetails_p = pickle.dumps(servicedetails)
		rconn.set("activeServices",servicedetails_p)

	except IndexError:
		service_dict = {'sid' : 0 , 'urls' : ['abc'] , 'filters' : [['a','a','maskWithAsterix',1]]}
		servicedetails.append(service_dict)
		servicedetails_p = pickle.dumps(servicedetails)
		rconn.set("activeServices",servicedetails_p)

