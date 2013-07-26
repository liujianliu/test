# coding:utf8
'''
Created on 2013-7-15

@author: liujian
'''
import gzip
import StringIO
import urllib2
import random
import time
from ip_rotator.spider import Spider
from ip_rotator.const import user_agents



class ProxySpider(Spider):
    
#    MUTEX_WRITE = threading.Semaphore()
    
    def __init__(self, name, host, user_agents='', cookie=''):
        super(ProxySpider, self).__init__(name,host,user_agents,cookie)
       
        
        
        
        
    def fetch(self, url,proxy, nb_retries = 0, retry_delay = 0):
        return self._fetch_url(url,proxy, nb_retries = nb_retries)
    
    
    
    def _fetch_url(self, url,proxy, nb_retries = 0, retry_delay = 0):
        proxy_url = "http://"+proxy
        proxy_support = urllib2.ProxyHandler({'http':proxy_url})
        #建立一个支持proxy的opener 用它来打开一个request
        opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
        
        self.log("fetching %s" % url)
        nb_tried = 0
        while nb_tried <= nb_retries:
            if nb_tried > 0:
                self.log("retried for %d time(s)" % nb_tried)
                
            try:
                if self.user_agents:
                    self.headers['User-Agent'] = self.user_agents
                else:
                    self.headers['User-Agent'] = user_agents[random.randint(0, len(user_agents)-1)]
                
                if self.cookie:
                    self.headers['Cookie'] = self.cookie
                request = urllib2.Request(url = url,
                                          headers = self.headers)                
                g = opener.open(request)
                html=""
                if g.headers.get('content-encoding', '') == 'gzip':
                    data = StringIO.StringIO(g.read())
                    gzipper = gzip.GzipFile(fileobj=data)
                    html = gzipper.read()
                else:
                    html = g.read()
                return html
            except Exception, e:
                self.log("exception caught while fetch %s: %s" % (url, str(e)))
            nb_tried += 1
            time.sleep(random.uniform(retry_delay*0.5, retry_delay*1.5))
            retry_delay *= 0.2
        self.log("return None from %s" % url)
        return None
    
    
    

    