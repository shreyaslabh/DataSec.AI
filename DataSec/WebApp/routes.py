from WebApp import app,con
from flask import render_template,request,redirect,url_for,flash,session,jsonify
from flask_mail import Mail,Message
from WebApp import putActiveServicesRedis as red
from itsdangerous import URLSafeSerializer
import datetime
import pickle


mail = Mail(app)
s = URLSafeSerializer(app.config["SECRET_KEY"])


def putUserLogs(sid,uid,logdata):
	
		cur = con.cursor()
		timstamp = datetime.datetime.now().date()
		cur.execute("INSERT INTO userlogs(logid,logdate,uid,logdata) VALUES(%s,%s,%s,%s)",(sid,timstamp,uid,logdata))
		con.commit()


# Default Route
@app.route('/')
def index():
	return render_template('login.html')




#User Logs In
@app.route('/login',methods = ["GET","POST"])
def login():
	try:
		if request.method=="POST":
			
			email = request.form['email'].lower()
			passw = request.form['pass']

			cur = con.cursor()

			cur.execute("SELECT * FROM users WHERE email = %s",(email,))
			try:
				udata = cur.fetchall()[0]
			except:
				flash("No User Found!","info")
				return redirect('/')
			
			if udata[6] == 1:

				if passw == udata[5]:
					session['uid'] = udata[0]
					session['utype'] = udata[1]
					fname = udata[2]
					lname = udata[3]
					session['name'] = fname + " " + lname

					return redirect('/manageservices')
				else:
					flash("Incorrect Password!","error")
					return redirect('/')
			elif udata[6] == -1:
				flash("User Account Rejected! Please Contact the Administrator.","error")
				return redirect('/')

			else:
				flash("User Not Yet Approved! Please Contact the Administrator.","info")
				return redirect('/')


	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')

#User Logs Out
@app.route('/logout',methods = ["GET","POST"])
def logout():
	session.clear()
	return redirect('/')




# New User Registers
@app.route('/register',methods = ["GET","POST"])
def register():
	try:
		if request.method=="POST":
			
			utype = request.form['utype']
			fname = request.form['fname']
			lname = request.form['lname']
			email = request.form['email'].lower()
			passw = request.form['pass']
			cnfpass = request.form['cnfpass']
			timstamp = datetime.datetime.now().date()

			if utype == '1':
				usertype = 'Administrator'
			elif utype == '2':
				usertype = 'Client'

			if passw == cnfpass:
				cur = con.cursor()
				cur.execute("INSERT INTO users(utype,fname,lname,email,passval,approve,timstamp) VALUES(%s,%s,%s,%s,%s,%s,%s)",(utype,fname,lname,email,passw,0,timstamp))
				con.commit()
				cur.execute("SELECT uid FROM users WHERE utype = %s AND fname = %s AND lname = %s AND email = %s AND passval = %s AND approve = %s",(utype,fname,lname,email,passw,0))
				uid = cur.fetchone()[0]

				uid = s.dumps(uid)

				url1 = url_for('approve', token = uid, _external = True)

				url2 = url_for('reject', token = uid, _external = True)

				with app.app_context():
					msg = Message(subject="New Administrator/Client Approval",
								sender=app.config.get("MAIL_USERNAME"),
								recipients=[app.config.get("MAIL_USERNAME")], # replace with your email for testing
								body=f" New Administrator/Client Approval \n User Type : {usertype} \n First Name : {fname} \n Last Name : {lname} \n Email Address : {email} \n Click To Accept : {url1} \n Click To Reject : {url2}")
					mail.send(msg)
					flash("New User Registered , Wait For Approval!","success")
					return redirect('/')


				flash("New User Registered!","success")
				return redirect('/')

			else:
				flash("Passwords Not Matching!","error")
				return redirect('/')
		else:
			return render_template('register.html')

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')


#Approve New User Account
@app.route('/approve/<token>',methods = ["GET","POST"])
def approve(token):

	try:
		uid = s.loads(token)
		cur = con.cursor()
		cur.execute("UPDATE users SET approve = %s WHERE uid = %s",(1,uid))
		con.commit()

		cur.execute("SELECT * FROM users WHERE uid = %s",(uid,))

		udata = cur.fetchall()[0]
		email = udata[4]

		flash(f"User With UniqueID : {uid} Approved!","success")

		with app.app_context():
					msg = Message(subject="Data Masking Microservice",
								sender=app.config.get("MAIL_USERNAME"),
								recipients=[email], # replace with your email for testing
								body=f"Congratulations, Your Account Has Been Approved!")
					mail.send(msg)

		return redirect('/') 

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')


@app.route('/approve_web/<uid>',methods = ["GET","POST"])
def approve_web(uid):

	try:
		#uid = s.loads(token)
		cur = con.cursor()
		cur.execute("UPDATE users SET approve = %s WHERE uid = %s",(1,uid))
		con.commit()

		cur.execute("SELECT * FROM users WHERE uid = %s",(uid,))

		udata = cur.fetchall()[0]
		email = udata[4]

		flash(f"User With UniqueID : {uid} Approved!","success")

		with app.app_context():
					msg = Message(subject="Data Masking Microservice",
								sender=app.config.get("MAIL_USERNAME"),
								recipients=[email], # replace with your email for testing
								body=f"Congratulations, Your Account Has Been Approved!")
					mail.send(msg)

		return redirect('/settings') 

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')


#Reject New User Account
@app.route('/reject/<token>',methods = ["GET","POST"])
def reject(token):

	try:
		uid = s.loads(token)
		cur = con.cursor()
		cur.execute("UPDATE users SET approve = %s WHERE uid = %s",(-1,uid))
		con.commit()

		cur.execute("SELECT * FROM users WHERE uid = %s",(uid,))

		udata = cur.fetchall()[0]
		email = udata[4]

		flash(f"User With UniqueID : {uid} Rejected","error")

		with app.app_context():
					msg = Message(subject="Data Masking Microservice",
								sender=app.config.get("MAIL_USERNAME"),
								recipients=[email], # replace with your email for testing
								body=f"Sorry, Your Account Has Been Rejected!")
					mail.send(msg)

		return redirect('/') 

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/reject_web/<uid>',methods = ["GET","POST"])
def reject_web(uid):

	try:
	
		cur = con.cursor()
		cur.execute("UPDATE users SET approve = %s WHERE uid = %s",(-1,uid))
		con.commit()

		cur.execute("SELECT * FROM users WHERE uid = %s",(uid,))

		udata = cur.fetchall()[0]
		email = udata[4]

		flash(f"User With UniqueID : {uid} Rejected","error")

		with app.app_context():
					msg = Message(subject="Data Masking Microservice",
								sender=app.config.get("MAIL_USERNAME"),
								recipients=[email], # replace with your email for testing
								body=f"Sorry, Your Account Has Been Rejected!")
					mail.send(msg)

		return redirect('/settings') 

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/waiting_web/<uid>',methods = ["GET","POST"])
def waiting_web(uid):

	try:
	
		cur = con.cursor()
		cur.execute("UPDATE users SET approve = %s WHERE uid = %s",(0,uid))
		con.commit()

		cur.execute("SELECT * FROM users WHERE uid = %s",(uid,))

		udata = cur.fetchall()[0]
		email = udata[4]

		flash(f"User With UniqueID : {uid} Waiting","info")

		with app.app_context():
					msg = Message(subject="Data Masking Microservice",
								sender=app.config.get("MAIL_USERNAME"),
								recipients=[email], # replace with your email for testing
								body=f"Hello, Your Account Has Been Shifted to Wait State!")
					mail.send(msg)

		return redirect('/settings') 

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/delete_user/<uid>',methods = ["GET","POST"])
def delete_user(uid):

	try:
	
		cur = con.cursor()

		cur.execute("SELECT * FROM users WHERE uid = %s",(uid,))

		udata = cur.fetchall()[0]
		email = udata[4]

		flash(f"User With UniqueID : {uid} Deleted!","info")

		with app.app_context():
					msg = Message(subject="Data Masking Microservice",
								sender=app.config.get("MAIL_USERNAME"),
								recipients=[email], # replace with your email for testing
								body=f"Sorry, Your Account Has Been Deleted!")
					mail.send(msg)

		cur.execute("SELECT sid FROM userservices WHERE uid = %s",(uid,))
		services = cur.fetchall()
		for service in services:
			sid = service[0]
			cur.execute("DELETE FROM userservices WHERE sid = %s",(sid,))
			con.commit()
			cur.execute("DELETE FROM services WHERE serviceid = %s",(sid,))
			con.commit()
			cur.execute("DELETE FROM servicedetails WHERE sid = %s",(sid,))
			con.commit()
			cur.execute("SELECT filterid FROM fsets WHERE fsetid = %s",(sid,))
			fs = cur.fetchall()
			for fid in fs:
				cur.execute("DELETE FROM filters WHERE fid = %s",(fid[0],))
				con.commit()
			cur.execute("DELETE FROM fsets WHERE fsetid = %s",(sid,))
			con.commit()
			cur.execute("DELETE FROM logs WHERE logid = %s",(sid,))
			con.commit()


		cur.execute("DELETE FROM users WHERE uid = %s",(0,uid))
		con.commit()

		return redirect('/settings') 

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



#Reset Password
@app.route('/resetpassword',methods = ["GET","POST"])
def resetpassword():
		
	try:
		if request.method=="POST":
			
			email = request.form['email']
			passw = request.form['pass']
			newpass = request.form['newpass']
			cnfnewpass = request.form['cnfnewpass']

			cur = con.cursor()

			cur.execute("SELECT * FROM users WHERE email = %s",(email,))
			try:
				udata = cur.fetchall()[0]
			except:
				flash("No User Found!","info")
				return redirect('/')
			
			if passw == udata[5]:
				if newpass == cnfnewpass:
					cur.execute("UPDATE users SET passval = %s WHERE email = %s",(newpass,email))
					con.commit()
					flash("Password Changed!","success")
					return redirect('/')
				else:
					flash("New Passwords Not Matching!","error")
					return redirect('/')
			else:
				flash("Incorrect Old Password!","error")
				return redirect('/')

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



#Forgot Password
@app.route('/forgotpassword',methods = ["GET","POST"])
def forgotpassword():
		
	try:
		if request.method=="POST":
			
			email = request.form['forgotemail']

			cur = con.cursor()

			cur.execute("SELECT * FROM users WHERE email = %s",(email,))
			try:
				udata = cur.fetchall()[0]
			except:
				flash("No User Found!","info")
				return redirect('/')

			try:
				password = udata[5]
				with app.app_context():
					msg = Message(subject="Data Masking Microservice",
								sender=app.config.get("MAIL_USERNAME"),
								recipients=[email], # replace with your email for testing
								body=f"Your password is : {password}, Don't share it to anyone")
					mail.send(msg)
					flash("Your Password has been Mailed!","success")
					return redirect('/')
			except:
				flash("Could Not Mail. Try Contacting Administrator.","error")
				return redirect('/')

		else:
			return redirect('/')

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')




# Manage Services WebPage
@app.route('/manageservices')
def manageservices():
		
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()

		uid = session['uid']
		utype = session['utype']
		name = session['name']

		if utype == 1:
			cur.execute("SELECT * FROM services ORDER BY dateofcreation DESC LIMIT 10")

		else:
			cur.execute("SELECT sid FROM userservices WHERE uid = %s ",(uid,))
			try:
				sids = cur.fetchall()[0]
			except:
				sids = (1,) # Service ID 1 is Reserved
			cur.execute("SELECT * FROM services WHERE serviceid IN %s ORDER BY status ASC",(sids,))

		allData = cur.fetchall()
		l = []
		for data in allData:
			if data[2] == 'active':
				d = 'Stop'
				isedit = 'disabled'
			else:
				d = 'Start'
				isedit = ' '
			l.append([data[0],data[1],data[2],d,isedit])
		
		stype = 'Recent Services'
		l.sort()
		return render_template('manageservices.html',services = l,name = name,stype=stype,utype=utype)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/viewservices')
def viewservices():
		
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()

		uid = session['uid']
		utype = session['utype']
		name = session['name']

		if utype == 1:
			cur.execute("SELECT * FROM services ORDER BY servicename ASC")

		else:
			cur.execute("SELECT sid FROM userservices WHERE uid = %s ",(uid,))
			try:
				sids = cur.fetchall()[0]
			except:
				sids = (1,) # Service ID 1 is Reserved
			cur.execute("SELECT * FROM services WHERE serviceid IN %s ORDER BY status ASC",(sids,))

		allData = cur.fetchall()
		l = []
		for data in allData:
			if data[2] == 'active':
				d = 'Stop'
				isedit = 'disabled'
			else:
				d = 'Start'
				isedit = ' '
			l.append([data[0],data[1],data[2],d,isedit])
		
		stype = 'All Services'
		l.sort()
		return render_template('manageservices.html',services = l,name = name,stype=stype, utype = utype)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')




@app.route('/search1',methods=["GET","POST"])
def search1():
	try:	
		if not 'uid' in session:
				return redirect('/')

		if request.method=="POST":

			cur = con.cursor()

			sname = request.form['sname']

			cur.execute("SELECT * FROM services WHERE servicename = %s",(sname,))

			allData = cur.fetchall()
			l = []
			for data in allData:
				if data[2] == 'active':
					d = 'Stop'
					isedit = 'disabled'
				else:
					d = 'Start'
					isedit = ' '
				l.append([data[0],data[1],data[2],d,isedit])
			
			stype="Selected Service"

			name = session['name']
			return render_template('manageservices.html',services = l,name = name,stype=stype)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



#Edit a given Service SID
@app.route('/sess/<seid>')
def sess(seid):
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		name = session['name']

		try:
			session['sid'] = str(seid)
		except:
			seid = session['sid']

		cur.execute("SELECT * FROM services WHERE serviceid = %s",(seid,))
		data = cur.fetchall()[0]

		sname = data[1]
		session['sname'] = sname
		return render_template('addnew.html',sname=sname,name=name)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



#Delete a given Service
@app.route('/delservice/<seid>')
def delservice(seid):
		
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		cur.execute("DELETE FROM userservices WHERE sid = %s",(seid,))
		con.commit()
		cur.execute("DELETE FROM services WHERE serviceid = %s",(seid,))
		con.commit()
		cur.execute("DELETE FROM servicedetails WHERE sid = %s",(seid,))
		con.commit()
		cur.execute("SELECT filterid FROM fsets WHERE fsetid = %s",(seid,))
		fs = cur.fetchall()
		for fid in fs:
			cur.execute("DELETE FROM filters WHERE fid = %s",(fid[0],))
			con.commit()
		cur.execute("DELETE FROM fsets WHERE fsetid = %s",(seid,))
		con.commit()
		cur.execute("DELETE FROM logs WHERE logid = %s",(seid,))
		con.commit()
		cur.close()

		red.activeServices()

		return redirect(url_for('manageservices'))

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')




#Create a New Service : Initialisation of Services Table with status = 'inactive'
@app.route('/sinsert',methods = ['GET','POST'])
def sinsert():
	
	try:

		if not 'uid' in session:
			return redirect('/')

		if request.method=="POST":
			
			uid = session['uid']
			sname = request.form['sname']
			
			cur = con.cursor()
			timstamp = datetime.datetime.now().date()
			cur.execute("INSERT INTO services(servicename,status,dateofcreation) VALUES(%s,%s,%s)",(sname,'inactive',timstamp))
			con.commit()
			cur.execute("SELECT serviceid FROM services WHERE servicename = %s AND status = %s AND dateofcreation = %s",(sname,'inactive',timstamp))
			sid = cur.fetchone()[0]
			cur.execute("INSERT INTO userservices(uid,sid) VALUES(%s,%s)",(uid,sid))
			con.commit()
			session['sid'] = str(sid)
			session['sname'] = sname
			cur.close()
			return render_template('addnew.html',sname=sname)
		else:
			#session['sid'] = str(sid)
			sname = session['sname']
			return render_template('addnew.html',sname=sname)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/updatesname',methods = ["GET","POST"])
def updatesname():
	try:
		if not 'uid' in session:
				return redirect('/')

		if request.method=="POST":
				
			uid = session['uid']
			sid = session['sid']

			sname = request.form['sname']
			name = session['name']
				
			cur = con.cursor()
			cur.execute("UPDATE services SET servicename = %s WHERE serviceid = %s",(sname,sid))
			con.commit()
			cur.close()

			session['sname'] = sname
			return render_template('addnew.html',sname=sname)
		else:
			return render_template('addnew.html',sname=session['sname'],name=name)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



# Step 1 WebPage
@app.route('/step1',methods=['GET','POST'])
def step1():
		
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		sid = session['sid']
		cur.execute("SELECT * FROM servicedetails WHERE sid = %s",(sid,))
		try:
			urlp = cur.fetchall()
		except TypeError:
			urlp = False

		cur.close()
		name = session['name']
		return render_template('step1.html',urls=urlp,sname=session['sname'],name = name)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')





# Add New URL Prefix Stage 1 
@app.route('/addurl',methods=['GET','POST'])
def addurl():
		
	try:
		if not 'uid' in session:
			return redirect('/')

		if request.method=="POST":
			
			sid = session['sid']
			cur = con.cursor()
			url  = request.form['urlprefix']
			cur.execute("INSERT INTO servicedetails(sid,urlp) VALUES(%s,%s)",(sid,url))
			con.commit()
			cur.close()
			return redirect(url_for('step1'))

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')





#Edit added URL Prefix Stage 1
@app.route('/urledit',methods = ['GET','POST'])
def urledit():
		
	try:
		if not 'uid' in session:
			return redirect('/')

		if request.method == 'POST':
			urlid = request.form['urlid']
			urlp = request.form['urlpre']
			sid = session['sid']
			cur = con.cursor()
			cur.execute("UPDATE servicedetails SET urlp = %s WHERE sid = %s AND urlid = %s",(urlp,sid,urlid))
			con.commit()
			cur.close()
			return redirect(url_for('step1'))

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')





#Delete added URL Stage 1
@app.route('/deleterow/<row>')
def deleterow(row):
		
	try:
		if not 'uid' in session:
			return redirect('/')

		#print("DELETE FUNCTION INVOKED!")
		sid = session['sid']
		cur = con.cursor()
		cur.execute("DELETE FROM servicedetails WHERE sid = %s AND urlp = %s ",(sid,row))
		con.commit()
		cur.close()
		return redirect(url_for('step1'))

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')





# Step 2 WebPage
@app.route('/step2',methods=['GET','POST'])
def step2():
		
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		sid = session['sid']

		#Fetching Default Filters
		cur.execute("SELECT * FROM filters WHERE ftype = %s ORDER BY fid ASC ",(0,))
		filters = list(cur.fetchall())
		flist = []
		for filter in filters:
			filter = list(filter)
			mid = filter[6]
			cur.execute("SELECT * FROM masks WHERE mid = %s",(mid,))
			filter[6] = cur.fetchall()[0][1]
			flist.append(filter)

		#Fetching Selected Filters
		cur.execute("SELECT * FROM fsets WHERE fsetid = %s ",(sid,))
		fids = cur.fetchall()
		selfils = []
		for fid in fids:
			cur.execute("SELECT * FROM filters WHERE fid = %s",(fid[1],))
			selfils.append(list(cur.fetchall()[0]))

		for selfil in selfils:
			mid = selfil[6]
			cur.execute("SELECT * FROM masks WHERE mid = %s",(mid,))
			selfil[6] = cur.fetchall()[0][1]

		cur.execute("SELECT * FROM prefixes ORDER BY pid")
		prefixes = cur.fetchall()

		pnames = []
		for prefix in prefixes:
			pnames.append(prefix[1])

		cur.execute("SELECT * FROM suffixes ORDER BY sufid")
		suffixes = cur.fetchall()

		snames = []
		for suffix in suffixes:
			snames.append(suffix[1])

		name = session['name']
		cur.close()
		status = 2
		return render_template('step2.html',filters=flist,selfils = selfils,status = status,prefixes=pnames,suffixes=snames,sname=session['sname'],name = name)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')






# Selecting from Default Filters Stage 2 
@app.route('/selfilter/<fid>',methods = ['GET','POST'])
def selfilter(fid):
		
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		sid = session['sid']

		cur.execute("SELECT * FROM filters WHERE fid = %s",(fid,))
		f = cur.fetchall()[0]

		fname = f[2]
		farea = f[3]
		fprefix = f[4]
		fsuffix = f[5]
		maskid = f[6]

		cur.execute("INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(%s,%s,%s,%s,%s,%s,%s)",(1,fname,farea,fprefix,fsuffix,maskid,0))
		con.commit()
		cur.execute("SELECT fid FROM filters WHERE ftype = %s AND fname = %s AND farea = %s AND fprefix = %s AND fsuffix = %s AND maskid = %s AND unmask = %s ORDER BY fid DESC",(1,fname,farea,fprefix,fsuffix,maskid,0))
		fid = cur.fetchone()[0]
		cur.execute("INSERT INTO fsets(fsetid,filterid) VALUES(%s,%s)",(sid,fid))
		con.commit()
		cur.close()
		return redirect(url_for('step2'))

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')






# Edit a Selected Filter : Add a new filter into Filters Table, link to Fsets Table
@app.route('/updatefil',methods = ["GET","POST"])
def updatefil():
		
	try:
		if not 'uid' in session:
			return redirect('/')

		if request.method == 'POST':
			fid = request.form['fid']
			fname = request.form['name']
			farea = request.form['area']
			fprefix = request.form['prefix']
			fsuffix = request.form['suffix']
			maskid = request.form['mask']
			cur = con.cursor()
			sid = session['sid']
			cur.execute("SELECT mid FROM masks WHERE mname = %s",(maskid,))
			mid = cur.fetchall()[0]
			#Check corresponding to fid is there a row with type = 0
			cur.execute("SELECT * FROM filters WHERE fid = %s",(fid,))
			f = cur.fetchall()[0]
			if f[1] == 1:
				cur.execute("UPDATE filters SET fname = %s , farea = %s , fprefix = %s , fsuffix = %s , maskid = %s , unmask = %s WHERE fid = %s",(fname,farea,fprefix,fsuffix,mid,0,fid))
				con.commit()
			cur.close()
			return redirect(url_for('step2'))

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')




# Delete Selected Filter FID
@app.route('/deleteselfil/<fid>')
def deleteselfil(fid):
		
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		sid = session['sid']
		cur.execute("DELETE FROM filters WHERE fid = %s",(fid,))
		con.commit()
		cur.execute("DELETE FROM fsets WHERE fsetid = %s AND filterid = %s ",(sid,fid))
		con.commit()
		cur.close()
		return redirect(url_for('step2'))

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')






# Step 3 WebPage
@app.route('/step3',methods = ['GET','POST'])
def step3():
	
	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		sid = session['sid']
		cur.execute("SELECT * FROM fsets WHERE fsetid = %s ",(sid,))
		fids = cur.fetchall()
		selfils = []
		for fid in fids:
			cur.execute("SELECT * FROM filters WHERE fid = %s",(fid[1],))
			selfils.append(list(cur.fetchall()[0]))

		for selfil in selfils:
			mid = selfil[6]
			cur.execute("SELECT * FROM masks WHERE mid = %s",(mid,))
			selfil[6] = cur.fetchall()[0][1]
		cur.close()
		name = session['name']
		return render_template('step3.html',selfils = selfils,sname=session['sname'],name = name)

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



# Save a New Service, make Status = Active
@app.route('/saveservice',methods = ['GET','POST'])
def saveservice():

	try:
		if not 'uid' in session:
			return redirect('/')

		else:
			cur = con.cursor()
			sid = session['sid']

			cur.execute("SELECT * FROM fsets WHERE fsetid = %s ",(sid,))
			fids = cur.fetchall()
			for fid in fids:
				cur.execute("UPDATE filters SET unmask = %s WHERE fid = %s",(0,fid[1]))
				con.commit()

			try:
				unmask = request.form.getlist('unmask')
				unmask = tuple(int(x) for x in unmask)
				cur.execute("UPDATE filters SET unmask = %s WHERE fid IN %s",(1,unmask))
				con.commit()
			except Exception as e:
				con.rollback()
				cur.close()


			cur = con.cursor()
			cur.execute("UPDATE services SET status = %s WHERE serviceid = %s",('active',sid))
			con.commit()
			cur.close()

			red.activeServices()

			return redirect(url_for('manageservices'))


	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')




# Stop Service
@app.route('/Stop/<sid>',methods = ['GET','POST'])
def stop(sid):

	# try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		#sid = session['sid']
		cur.execute("UPDATE services SET status = %s WHERE serviceid = %s",('inactive',sid))
		con.commit()
		cur.close()

		red.activeServices()

		return redirect(url_for('manageservices'))

	# except:
	# 	con.rollback()
	# 	cur.close()

	# 	return redirect('/')



#Start Service
@app.route('/Start/<sid>',methods = ['GET','POST'])
def start(sid):

	try:
		if not 'uid' in session:
			return redirect('/')

		cur = con.cursor()
		#sid = session['sid']
		cur.execute("UPDATE services SET status = %s WHERE serviceid = %s",('active',sid))
		con.commit()
		cur.close()

		red.activeServices()

		return redirect(url_for('manageservices'))

	except:
		con.rollback()
		cur.close()

		return redirect('/')





@app.route('/logs',methods=["GET","POST"])
def logs():
	try:
		if not 'uid' in session:
			return redirect('/')

		utype = session['utype']

		if request.method=="POST":
			cur = con.cursor()
			startdate = request.form['startdate']
			enddate = request.form['enddate']
			#date = request.form['date']
			wholedata = []
			cur.execute("SELECT * FROM services WHERE dateofcreation BETWEEN %s AND %s",(startdate,enddate))
			data = cur.fetchall()
			for s in data:
				sid = str(s[0])
				#print(sid)
				cur.execute("SELECT * FROM userservices WHERE sid = %s",(sid,))
				user = cur.fetchall()[0]
				uid = str(user[0])
				cur.execute("SELECT * FROM users WHERE uid = %s",(uid,))
				userdata = cur.fetchall()[0]
				username = str(userdata[2]) + " " + str(userdata[3])
				print(username)
				wholedata.append([s[0],s[1],s[2],s[3],username])
			name = session['name']


			return render_template('dashboard.html',data = wholedata,name=name,utype=utype,startdate=startdate,enddate=enddate)
		else:
			'''cur = con.cursor()
												cur.execute("SELECT * FROM services ORDER BY status")
												data = cur.fetchall()'''
			name = session['name']
			return render_template('dashboard.html',name=name,utype=utype)
			
	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/view_report',methods=["GET","POST"])
def view_report():
	try:
		if not 'uid' in session:
			return redirect('/')

		if request.method=="POST":
			cur = con.cursor()
			sid = request.form['logid']
			date = request.form['date']
			uname = request.form['name']
			sname = request.form['sname']
			status = request.form['status']

			startdate = request.form['startdate']
			enddate = request.form['enddate']

			data = [[sid,sname,status,date,uname,]]
			#date = request.form['date']

			utype = session['utype']

			cur.execute("SELECT * FROM logs WHERE logid = %s",(sid,))
			logdata = cur.fetchall()
			try:
				print(logdata[0])
				name = session['name']
				alldata = []
				for row in logdata:
					masks = pickle.loads(row[3])
					#print(masks)
					alldata.append([row[0],row[1],row[2],masks])

				return render_template('dashboard.html',name=name,data=data,logdata=alldata,utype=utype,startdate=startdate,enddate=enddate)
			except:
				flash("No Logs Found!","info")
				name = session['name']
				return render_template('dashboard.html',name=name,data=data,logdata=logdata,utype=utype,startdate=startdate,enddate=enddate)
		else:
			return redirect('/logs')

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')




@app.route('/settings',methods=["GET","POST"])
def settings():
	try:
		if not 'uid' in session:
			return redirect('/')
		elif session['utype'] != 1:
			return redirect('/')

		if request.method=="POST":
			cur = con.cursor()
			email = request.form['email']
			cur.execute("SELECT * FROM users WHERE email = %s",(email,))
			
		else:
			cur = con.cursor()
			cur.execute("SELECT * FROM users ORDER BY timstamp DESC")

		users = cur.fetchall()
		alldata = []
		for user in users:
			ustatus = user[6]
			if ustatus == 0:
				ustatus = "Waiting"
			elif ustatus == 1:
				ustatus = "Approved"
			elif ustatus == -1:
				ustatus = "Rejected"
			alldata.append([user[0],user[1],user[2],user[3],user[4],user[5],ustatus,user[7]])

		name = session['name']
		return render_template('settings.html',name=name,users=alldata, pagename="")


	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/user_approval')
def user_approval():
	try:
		if not 'uid' in session:
				return redirect('/')

		cur = con.cursor()
		name = session['name']

		cur.execute("SELECT * FROM users WHERE approve = 1")
		users = cur.fetchall()
		alldata = []
		for user in users:
			ustatus = user[6]
			if ustatus == 0:
				ustatus = "Waiting"
			elif ustatus == 1:
				ustatus = "Approved"
			elif ustatus == -1:
				ustatus = "Rejected"
			alldata.append([user[0],user[1],user[2],user[3],user[4],user[5],ustatus,user[7]])

		pagename = "Approved"
		return render_template('settings.html',name=name,users=alldata,pagename=pagename)
	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')




@app.route('/user_waiting')
def user_waiting():
	try:
		if not 'uid' in session:
				return redirect('/')

		cur = con.cursor()
		name = session['name']

		cur.execute("SELECT * FROM users WHERE approve = 0")
		users = cur.fetchall()
		alldata = []
		for user in users:
			ustatus = user[6]
			if ustatus == 0:
				ustatus = "Waiting"
			elif ustatus == 1:
				ustatus = "Approved"
			elif ustatus == -1:
				ustatus = "Rejected"
			alldata.append([user[0],user[1],user[2],user[3],user[4],user[5],ustatus,user[7]])

		pagename = "Waiting For Approval"
		return render_template('settings.html',name=name,users=alldata,pagename=pagename)
	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/user_rejection')
def user_rejection():
	try:
		if not 'uid' in session:
				return redirect('/')

		cur = con.cursor()
		name = session['name']

		cur.execute("SELECT * FROM users WHERE approve = -1")
		users = cur.fetchall()
		alldata = []
		for user in users:
			ustatus = user[6]
			if ustatus == 0:
				ustatus = "Waiting"
			elif ustatus == 1:
				ustatus = "Approved"
			elif ustatus == -1:
				ustatus = "Rejected"
			alldata.append([user[0],user[1],user[2],user[3],user[4],user[5],ustatus,user[7]])
		pagename = "Unapproved"
		return render_template('settings.html',name=name,users=alldata,pagename=pagename)
	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/help')
def help():
	try:
		name = session['name']
		utype = session['utype']
		return render_template('help.html',name=name,utype=utype)
	except Exception as e:
		con.rollback()
		cur.close()
		return redirect('/')

@app.route('/filtertypes')
def filtertypes():
	try:
		name = session['name']
		utype = session['utype']
		return render_template('filtertypes.html',name=name,utype=utype)
	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')





@app.route('/userlogs',methods=["GET","POST"])
def userlogs():
	try:
		if not 'uid' in session:
			return redirect('/')

		utype = session['utype']

		if request.method=="POST":
			cur = con.cursor()
			startdate = request.form['startdate']
			enddate = request.form['enddate']
			#date = request.form['date']
			wholedata = []
			cur.execute("SELECT * FROM userlogs WHERE logdate BETWEEN %s AND %s",(startdate,enddate))
			data = cur.fetchall()
			name = session['name']
			return render_template('userDashboard.html',data = data,name=name,utype=utype)
		else:
			'''cur = con.cursor()
												cur.execute("SELECT * FROM services ORDER BY status")
												data = cur.fetchall()'''
			name = session['name']
			return render_template('userDashboard.html',name=name,utype=utype)
			
	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')



@app.route('/view_user_report',methods=["GET","POST"])
def view_user_report():
	try:
		if not 'uid' in session:
			return redirect('/')

		if request.method=="POST":
			cur = con.cursor()
			sid = request.form['logid']
			date = request.form['date']
			uname = request.form['name']
			sname = request.form['sname']
			status = request.form['status']
			data = [[sid,sname,status,date,uname,]]
			#date = request.form['date']

			utype = session['utype']

			cur.execute("SELECT * FROM userlogs WHERE logid = %s",(sid,))
			logdata = cur.fetchall()
			try:
				print(logdata[0])
				name = session['name']
				# alldata = []
				# for row in logdata:
				# 	masks = pickle.loads(row[3])
				# 	#print(masks)
				# 	alldata.append([row[0],row[1],row[2],masks])

				return render_template('dashboard.html',name=name,data=data,logdata=alldata,utype=utype)
			except:
				flash("No Logs Found!","info")
				name = session['name']
				return render_template('dashboard.html',name=name,data=data,logdata=logdata,utype=utype)
		else:
			return redirect('/logs')

	except Exception as e:
		con.rollback()
		cur.close()

		return redirect('/')


