import random
import tempfile
import time
import socket
import collections
import gzip
import imghdr
import chardet
import re
from re import search
import string
import pandas as pd
import psycopg2
import gzip
import threading
import logging
import urllib.parse as up
from presidio_analyzer import AnalyzerEngine

from masks.type2Masks import *

import getServices as gs
from getServices import rconn,logger


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    import socketserver
except ImportError:
    import SocketServer
    socketserver = SocketServer

import sys
sys.path.append('.')

from pyicapNew import *



import psycopg2


#rconn.set('session_mask',)

class ThreadingSimpleServer(socketserver.ThreadingMixIn, ICAPServer):
     def finish_request(self, request, client_address):
        request.settimeout(30)
        # "super" can not be used because BaseServer is not created from object
        ICAPServer.finish_request(self, request, client_address)

class ICAPHandler(BaseICAPRequestHandler):

    '''session_mask = {}
                hit_service_id = []'''


    def checkURL(self,checkurl):

        activeServices = gs.activeServices()
        
        for service in activeServices:
            
            urls = service['urls']

            for url in urls:
                if search(url,checkurl):
                    print("URL HIT!!!! FOR SERVICE ID : ",service['sid'])
                    logger.info("URL HIT!!!! FOR SERVICE ID : " + str(service['sid']))
                    gs.putLogs(service['sid'],'URL Hit for Service ID',str(service['sid']))

                    print(url,checkurl)
                    return(service['sid'])
        return('0')


    def maskTheData(self,content,flag,sid,sessionid):
        
        activeServices = gs.activeServices()

        print("Hit Services : ",gs.getHitServices())

        for service in activeServices:
            #IF URL FILTERING
            if service['sid'] == sid:

                gs.putLogs(service['sid'],'Masking For Session ID',str(sessionid))
                
                if flag == 1:
                    content = gzip.decompress(content)
                elif flag == 2:
                    content = up.unquote(content)
                else:
                    pass

                encoding = chardet.detect(content)['encoding']
                    #print("Uncompressed Content: ",content)

                fdetails = service['filters']

                all_mask_pairs = []

                for row in fdetails:
                    pref = row[0]
                    suf = row[1]
                    mask = row[2]
                    unmask = row[3]

                    if mask == 'numbersOnlyData':
                        content,mask_pairs = numbersOnlyData(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'charsOnlyData':
                        content,mask_pairs = charsOnlyData(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'numbersAndChars':
                        content,mask_pairs = numbersAndChars(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'emailData':
                        content,mask_pairs = emailData(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'maskWithAsterix':
                        content,mask_pairs = maskWithAsterix(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'maskWithHash':
                        content,mask_pairs = maskWithHash(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'reduceMaskWithAsterix':
                        content,mask_pairs = reduceMaskWithAsterix(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'reduceMaskWithHash':
                        content,mask_pairs = reduceMaskWithHash(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'partialMaskWithAsterix':
                        content,mask_pairs = partialMaskWithAsterix(encoding,content,pref,suf,unmask,sessionid)

                    elif mask == 'partialMaskWithHash':
                        content,mask_pairs = partialMaskWithHash(encoding,content,pref,suf,unmask,sessionid)

                    #print("Mask Pairs : ", mask_pairs)
                    if mask_pairs == ['0']:
                        pass
                    else:
                        all_mask_pairs.append(mask_pairs)

                #print("All_Mask_Pairs : ", all_mask_pairs)
                gs.putIntoSessionMasks(service['sid'],all_mask_pairs)
                print("Putting Into Session Masks : " + str(service['sid']) + "Mask Pairs" + str(all_mask_pairs))
                logger.info("Putting Into Session Masks : " + str(service['sid']) + "Mask Pairs" + str(all_mask_pairs))
                gs.putLogs(service['sid'],'Masks Applied to the Response',all_mask_pairs)

                '''Session_mask :  [{63: [[['080-22932392', '******'], ['080-23601227', '******'], ['022-25767068', '******'], 
                    ['011-26591750', '******'], ['011-26596137', '******'], ['011-26591749', '******'], ['044-22578200', '******']], 
                    [['0361-2582751', '############'], ['0361-2582755', '############'], ['0512-2597412', '############']]]}]'''

                #print("Session_mask : ", self.session_mask)

                if flag == 1:
                        content = gzip.compress(content)
                elif flag == 2:
                        content = up.quote(content)

            else:
                pass

        return(content)

    def unMaskTheData(self,data,sid,flag,sessionid):
        #originaldata = data
        encoding = 0
        gs.putLogs(sid,'Unmasking For Session ID',str(sessionid))
        #print("Raw Request Received : ",data)
        
        encoding = chardet.detect(data)['encoding']
        #print("ENCODING : ",encoding)
                                                            
        if encoding:
            data = data.decode(encoding)

            #print("DATA : ", data)

            if flag == 1:
                    data = gzip.decompress(data)
            else:
                pass


            #print("DECODED DATA : ",data)
                #print("Req Received Decoded : ",data)
                #print(self.session_mask)

            keys = list(gs.getSessionMasks().keys())
            print("Session_Mask Keys : ",keys)
            for key in keys:
                if sid == key:
                    servicedetails = gs.getSessionMasks()[key]

                    print("Hit Service Details",servicedetails)
                    logger.info("Hit Service Details For Unmasking : "+str(servicedetails))

                    unmaskpairs = []
                    for mask in servicedetails:
                        for pair in mask:
                            pidata = str(pair[0])
                            mdata = str(pair[1])


                            if pidata == 'cookie':
                                if mdata != sessionid:
                                    print(" SESSION ID MISS, WONT BE UNMASKING!")
                                    goto : dontunmask
                            else:

                                if flag == 2:
                                    pidata = up.quote_plus(pidata,encoding=encoding)
                                    mdata = up.quote_plus(mdata,encoding=encoding)
                                #print("UNMASKING  " + mdata + " WITH " + pidata)

                                if mdata in data:
                                    data = data.replace(mdata,pidata,1)
                                    print("Replacing : "+mdata+" With : "+pidata)
                                    logger.info("Replacing : "+mdata+" With : "+pidata)
                                    unmaskpairs.append("Replacing : "+mdata+" With : "+pidata)
                                    

                                else:
                                    print("Else Condition instead of  Replacing")
                                    logger.info("Else Condition instead of  Replacing")

                    gs.putLogs(sid,'Unmasks Applied to the Request',unmaskpairs)


            if flag == 1:
                data = gzip.compress(data)
            else:
                pass

            label: dontunmask
            data = bytes(data,encoding)

        else:
            pass

        return(data)


    def read_into(self, f):
        while True:
            try:
                chunk = self.read_chunk()
                if chunk == b'':
                    return

                print(len(chunk))
                f.write(chunk)
            except:
                return


    def reqmod_OPTIONS(self):
         self.set_icap_response(200)
         self.set_icap_header(b'Methods', b'REQMOD')
         self.set_icap_header(b'Max-Connections', b'10')
         self.set_icap_header(b'Service', b'PyICAP Server 1.0')
         self.send_headers(False)


    def reqmod_REQMOD(self):
        self.set_icap_response(200)

        self.set_enc_request(b' '.join(self.enc_req))

        #print("REQMOD Enc Req Status : ",self.enc_req) # self.enc_req[1] has the Server URL (TARGET SCOPE).
        #logger.info(print("REQMOD Enc Req Status : " + str(self.enc_req)))

        flag = 0
        unmaskflag = 0
        sid = 0
        sessionid = '0'

        urlServer = self.enc_req[1]
        print("URLServer : ",urlServer)

        the_encoding = chardet.detect(urlServer)['encoding']
        checkurl = urlServer.decode(the_encoding)

        sid = self.checkURL(checkurl)

        if sid == '0':
            pass

        else:
            unmaskflag = 1
            gs.putLogs(sid,'Request Received From',checkurl)

            if sid not in gs.getHitServices():
                gs.putIntoHitServices(sid)
            else:
                pass

        
        print("Request Header:")
        for h in self.enc_req_headers:
            for v in self.enc_req_headers[h]:
                if h == b'content-type' and v == b'application/x-www-form-urlencoded':
                        flag=2 # Flag 2 for URl Encoding
                elif h == b'cookie':
                        the_encoding = chardet.detect(v)['encoding']
                        sessionid = v.decode(the_encoding)

                print(h,v)
                self.set_enc_header(h, v)
        
        # Copy the request body (in case of a POST for example)
        if not self.has_body:
            self.send_headers(False)
            return
        if self.preview:
            prevbuf = b''
            while True:
                chunk = self.read_chunk()
                if chunk == b'':
                    break
                prevbuf += chunk
            if self.ieof:
                self.send_headers(True)
                if len(prevbuf) > 0:
                    self.write_chunk(prevbuf)
                self.write_chunk(b'')
                return
            self.cont()
            self.send_headers(True)
            if len(prevbuf) > 0:
                self.write_chunk(prevbuf)
            while True:
                chunk = self.read_chunk()
                self.write_chunk(chunk)
                if chunk == b'':
                    break
        
        else:

            #self.send_headers(True)

            while True:

                chunk = self.read_chunk()
                print("REQ Received : ",chunk)
                if chunk == b'':
                    self.write_chunk(chunk)
                    break
                    
                elif unmaskflag:
                    chunk = self.unMaskTheData(chunk,sid,flag,sessionid)
                else:
                    pass
                print("REQ Sent : ",chunk)
                logger.info("REQ Sent : " + str(chunk))
                print("Sending Header : ")
                #logger.info("Sending Header : ")
                for h in self.enc_req_headers:
                    for v in self.enc_req_headers[h]:
                        if h == b'content-length':
                            the_encoding = chardet.detect(v)['encoding']
                            v = bytes(str(len(chunk)),the_encoding)
                        print(h,v)
                        #logger.info(str(h) + " " + str(v))
                        self.set_enc_header(h, v)
                self.send_headers(True)
                self.write_chunk(chunk)



    
    def respmod_OPTIONS(self):
        self.set_icap_response(200)
        self.set_icap_header(b'Methods', b'RESPMOD')
        self.set_icap_header(b'Service', b'PyICAP Server 1.0')
        self.set_icap_header(b'Preview', b'1024')
        self.set_icap_header(b'Transfer-Preview', b'*')
        self.set_icap_header(b'Transfer-Ignore', b'jpg,jpeg,gif,png,swf,flv')
        self.set_icap_header(b'Transfer-Complete', b'')
        self.set_icap_header(b'Max-Connections', b'10')
        self.set_icap_header(b'Options-TTL', b'3600')
        self.send_headers(False)


    def respmod_RESPMOD(self):
        self.set_icap_response(204)

        #print("RESPMOD Enc Req Status : ",self.enc_res_status)
        #print("RESPMOD Servicename : ",self.servicename)

        self.set_enc_status(b' '.join(self.enc_res_status))

        if not self.has_body:
            self.send_headers(False)
            return
        with tempfile.NamedTemporaryFile(prefix='pyicap.', suffix='.txt') as upstream:
            self.set_icap_response(200)
            self.read_into(upstream)
            if self.preview and not self.ieof:
                self.cont()
                self.read_into(upstream)
            upstream.seek(0)
            try:
                with open(upstream, "r") as f:
                    data = f.read()
                    print(type(data))
                    #print("Content Received : ",data)
            except:
                pass
            # And write it to downstream
            upstream.seek(0)
            content = upstream.read()
            
            #the_encoding = chardet.detect(content)['encoding']
            flag = 0
            
            urlServer = self.enc_req[1]
            print("RESPMOD REQUEST URLServer : ",urlServer)

            the_encoding = chardet.detect(urlServer)['encoding']
            checkurl = urlServer.decode(the_encoding)

            sid = self.checkURL(checkurl)

            maskflag = 0

            if sid == '0':
                pass

            else:
                maskflag = 1
                gs.putLogs(sid,'Response Received From',checkurl)

                if sid not in gs.getHitServices():
                    gs.putIntoHitServices(sid)
                else:
                    pass


            if maskflag:

                print("Masking Response From : "+checkurl)

                for h in self.enc_res_headers:
                    for v in self.enc_res_headers[h]:

                        if h == b'content-encoding' and v == b'gzip':
                            flag = 1 # 1 for gzip encoding
                            print('GZIP ENCODED!')
                        elif h == b'content-type' and v == b'application/x-www-form-urlencoded':
                            flag = 2 # 2 for url encoding
                            print('URL ENCODED!')

                #SESSION ID MANAGEMENT

                sessionid = '0'
                for h in self.enc_req_headers:
                    for v in self.enc_req_headers[h]:
                        if h == b'cookie':
                            the_encoding = chardet.detect(v)['encoding']
                            sessionid = v.decode(the_encoding)

                content = self.maskTheData(content,flag,sid,sessionid)
            
                print("RESPMOD RESPONSE Masked Header:")
                for h in self.enc_res_headers:
                    for v in self.enc_res_headers[h]:
                        the_encoding = chardet.detect(v)['encoding']
                        if h == b'content-length':
                            v = bytes(str(len(content)),the_encoding)

                        print(h,v)
                        #logger.info(str(h) + " " + str(v))
                        self.set_enc_header(h, v)

            else:

                for h in self.enc_res_headers:
                    for v in self.enc_res_headers[h]:
                        #print(h,v)
                        self.set_enc_header(h, v)

            try:
                self.send_headers(True)
                #print("Sending Final Content : ",content)
                self.write_chunk(content)
                self.write_chunk(b'')
            except:
                pass







    def handle_one_request(self):
        def call_method():
            mname = (self.servicename + b'_' + self.command).decode("utf-8")
            if not hasattr(self, mname):
                self.log_error("%s not found" % mname)
                raise ICAPError(404)

            method = getattr(self, mname)
            if not isinstance(method, collections.Callable):
                raise ICAPError(404)
            method()
            self.close_connection = True
        """Handle a single HTTP request.
        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.
        """

        # Initialize handler state
        self.enc_req = None
        self.enc_req_headers = {}
        self.enc_res_status = None
        self.enc_res_headers = {}
        self.has_body = False
        self.servicename = None
        self.encapsulated = {}
        self.ieof = False
        self.eob = False
        self.methos = None
        self.preview = None
        self.allow = set()
        self.client_ip = None

        self.icap_headers = {}
        self.enc_headers = {}
        self.enc_status = None  # Seriously, need better names
        self.enc_request = None

        self.icap_response_code = None

        try:
            self.raw_requestline = self.rfile.readline(65537)
            self.log_error(self.raw_requestline)
            if not self.raw_requestline:
                self.close_connection = True
                return
            self.parse_request()
            call_method()
            self.wfile.flush()
            self.log_request(self.icap_response_code)
        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
        except ConnectionResetError as e:
            self.log_error("Connection reset error: %r", e)
            self.close_connection = 1
        except ICAPError as e:
            msg = e.message[0] if isinstance(e.message, tuple) else e.message
            self.send_error(e.code, msg)



port = 13446

server = ThreadingSimpleServer((b'', port), ICAPHandler)
try:
   
    #gs.putActiveServicesIntoRedis()

    t1 = threading.Thread(target=server.serve_forever)
    t1.setDaemon(True)
    t1.start()
    t1.join()

except KeyboardInterrupt:
    print("Finished")