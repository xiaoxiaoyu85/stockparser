#!/usr/bin/python
from binascii import b2a_base64
import json
import re
import urllib
#import urllib2
import cookielib
import socket
import time
import requests as requests
import os
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(filename= os.environ["APPDATA"] + "\\" + "stock.log", mode="a", maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
handler.setFormatter(formatter)
g_logger = logging.getLogger("stock")
g_logger.setLevel(logging.DEBUG)
g_logger.addHandler(handler)




dictHeaders = {'Accept' : 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language' : 'zh-CN',
                        #'Content-Type' : 'application/x-www-form-urlencoded',
                        'X-Requested-With' : 'XMLHttpRequest',
                        #'Accept-Encoding' : 'deflate',
                        'Connection' : 'Keep-Alive',
                        'User-Agent' : 'Mozilla/5.0 compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0',
                        'Referer' : 'https://caipiao.baidu.com/lottery/draw/view/200?qq-pf-to=pcqq.c2c',
                        'DNT' : '1',
                        'Cookie' : 'BAIDUID=81C36ADA26E5E63B0DAC30874D51D511:FG=1'
                        }


def HttplibGet(strUrl):
    urlParse = urlparse.urlparse(strUrl)
    strPath = urlParse.path
    strHost = urlParse.hostname
    iPort = urlParse.port
    strPath = strPath + "?" + urlParse.query
    #strQueryString = urllib.urlencode(listPara)        
    httpconn = httplib.HTTPConnection(strHost, iPort)
    httpconn.request('GET', strPath, None, dictHeaders)
    response = httpconn.getresponse()
    strRspData = response.read()
    return int(response.status), strRspData

class HttpBase():
    def PostMsg(self, dictMsg):
        result = {}                      
        kwargs = {'url' : config.PUBSUB_CFG['POST_URL'], 
             'method' : 'POST',         
             'headers':  config.PUBSUB_CFG['PostHeader'],
             'json' : dictMsg} 
        try:  
            resp = requests.request(**kwargs)
            result = {
                'status': resp.status_code,
                'data': resp.content
                }
        except Exception, e:            
            result = {'status': 'error',
                'data': "Couldn't resolve host: " + kwargs['url']               
            }   
        return result
      
    def GetMsg(self, strUrl, dictParams):   
        result = {}        
        kwargs = {'url' : strUrl, 
             'method' : 'GET',  
             'params' : dictParams,           
             'headers':  dictHeaders}
        try:  
            resp = requests.request(**kwargs)
            result['status'] = resp.status_code       
            if 200 == resp.status_code:
                result['data'] = resp.content
        except Exception, e:            
            result = {'status': 'error',
                'data': "Couldn't resolve host: " + kwargs['url']               
            }
        return result
