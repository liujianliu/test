# coding:utf8
'''
Created on 2013-7-17

@author: liujian
'''
import threading
import time

from spider_by_proxy import ProxySpider
class HtmlFetchThread(threading.Thread):
    def __init__(self, proxy,url):  
        threading.Thread.__init__(self)  
        self.html=''
        self.spider = ProxySpider(name='duokan',host='localhost')
        self.proxy =proxy
        self.url =url
        
    def run(self):
        self.html=self.spider.fetch(url=self.url, proxy=self.proxy, nb_retries=0, retry_delay=0.5)
    
    
    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    
    def does_function(self):
        trycount=1
        data=""
        while trycount<=3:
            try:
                f=self.opener.open(self.request)
                data=f.read()
                break
            except:
                time.sleep(0.5)
                trycount=trycount+1
        if trycount>3:
            print "bad"
            return None
        else:
            return data
    
        

