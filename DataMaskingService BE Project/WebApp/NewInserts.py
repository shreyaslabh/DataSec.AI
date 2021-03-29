def putUserLogs(sid,uid,logdata):
	
		cur = con.cursor()
		timstamp = datetime.datetime.now().date()
		cur.execute("INSERT INTO userlogs(logid,logdate,uid,logdata) VALUES(%s,%s,%s,%s)",(sid,timstamp,uid,logdata))
		con.commit()

#REGISTER

putUserLogs(sid=0,uid,'New Registration!')

#LOGIN

putUserLogs(sid=0,uid,'Logged In!')

#LOGOUT

putUserLogs(sid=0,uid,'Logged Out!')

#APPROVE

putUserLogs(sid=0,uid,'Approved!')

#REJECT

putUserLogs(sid=0,uid,'Rejected!')

#ADD NEW SERVICE

putUserLogs(sid,uid,'Added New Service!')

#START

putUserLogs(sid,uid,'Started Service!')

#EDIT

putUserLogs(sid,uid,'Edited Service!')

#DELETE

putUserLogs(sid,uid,'Deleted Service!')
