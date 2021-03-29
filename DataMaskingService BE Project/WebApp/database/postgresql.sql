
CREATE TABLE users(

uid SERIAL PRIMARY KEY,
utype INT,
fname VARCHAR(100),
lname VARCHAR(100),
email VARCHAR(100),
passval VARCHAR(100),
approve INT,
timstamp VARCHAR(100));


CREATE TABLE userservices(
uid INT,
sid INT);


CREATE TABLE prefixes(
pid SERIAL,
	pname VARCHAR(200)
);


CREATE TABLE suffixes(
sufid SERIAL,
	sufname VARCHAR(200)
);


CREATE TABLE services(

serviceid SERIAL PRIMARY KEY,
servicename VARCHAR(50),
status VARCHAR(20),
dateofcreation DATE
);



CREATE TABLE fsets(

fsetid INT,
filterid INT
);



CREATE TABLE filters(

fid SERIAL PRIMARY KEY,
ftype INT,
fname VARCHAR(100),
farea VARCHAR(100),
	fprefix VARCHAR(500),
	fsuffix VARCHAR(500),
	maskid INT,
	unmask INT
);

CREATE TABLE servicedetails(

sid INT ,
urlid SERIAL,
urlp TEXT
);

CREATE TABLE masks(

mid SERIAL PRIMARY KEY,
mname VARCHAR(100)
);

CREATE TABLE logs(

logid INT,
logdate DATE,
lognature VARCHAR(500),
logdata BYTEA
);

CREATE TABLE userlogs(

logid INT,
logdate DATE,
uid INT,
logdata VARCHAR(500)
);


INSERT INTO users(utype,fname,lname,email,passval,approve) VALUES(1,'admin','admin','admin@sutherland.com','lockdown',1);

INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Numbers Only','body','abc/','def/',1,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Characters Only','head','/abc/','/def/',2,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Numbers & Characters','body','/abc','/def',3,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Email Address','Body','\w*[@]\w*\.','ASM',4,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Asterix Mask','Body','\d{2,5}[-]\d{6,10}','ASM',5,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Hash Mask','Body','\d{3}[-]\d{2}[-]\d{4}','ASM',6,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Asterix Reduced Mask','Body','\d{4}\s\d{4}\s\d{4}\s\d{4}','ASM',7,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Hash Reduced Mask','Body','/ccb','ASM',8,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Asterix Partial Mask','Body','\d{3}\s\d{3}','ASM',9,0);
INSERT INTO filters(ftype,fname,farea,fprefix,fsuffix,maskid,unmask) VALUES(0,'Hash Partial Mask','Body','/ccd','ASM',10,0);


INSERT INTO masks(mname) VALUES('numbersOnlyData');
INSERT INTO masks(mname) VALUES('charsOnlyData');
INSERT INTO masks(mname) VALUES('numbersAndChars');
INSERT INTO masks(mname) VALUES('emailData');
INSERT INTO masks(mname) VALUES('maskWithAsterix');
INSERT INTO masks(mname) VALUES('maskWithHash');
INSERT INTO masks(mname) VALUES('reduceMaskWithAsterix');
INSERT INTO masks(mname) VALUES('reduceMaskWithHash');
INSERT INTO masks(mname) VALUES('partialMaskWithAsterix');
INSERT INTO masks(mname) VALUES('partialMaskWithHash');

INSERT INTO prefixes(pname) VALUES('EMAIL_ADDRESS');
INSERT INTO prefixes(pname) VALUES('\w*[@]\w*\.');
INSERT INTO prefixes(pname) VALUES('PHONE_NUMBER');
INSERT INTO prefixes(pname) VALUES('\d\d\d(|-| |\d|\d\d|\d )(|-)\d{3}(|-| )\d(| )\d{2,4}');
INSERT INTO prefixes(pname) VALUES('US_SSN');
INSERT INTO prefixes(pname) VALUES('\d{4}\s\d{4}\s\d{4}');
INSERT INTO prefixes(pname) VALUES('CREDIT_CARD');


INSERT INTO suffixes(sufname) VALUES('ASM');
INSERT INTO suffixes(sufname) VALUES('ASMRED');
INSERT INTO suffixes(sufname) VALUES('NLP');
INSERT INTO suffixes(sufname) VALUES('NLPRED');

INSERT INTO services(servicename,status) VALUES('test1','active');

INSERT INTO servicedetails(sid,urlp) VALUES(1,'https://www.google.com');
INSERT INTO servicedetails(sid,urlp) VALUES(1,'https://www.apple.com');

INSERT INTO fsets(fsetid,filterid) VALUES(1,1);
INSERT INTO fsets(fsetid,filterid) VALUES(1,2);


INSERT INTO logs(logid,logfile) VALUES(1,'testlogs1');