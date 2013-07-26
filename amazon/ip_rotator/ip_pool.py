# coding:utf8
'''
Created on 2013-7-12

@author: liujian
'''
import urllib2
import time
import thread
import threading
from ip_rotator.config import proxy_spider_config
import Queue
urllib2.socket.setdefaulttimeout(8)
class IpPool():
    MUTEX_D = threading.Semaphore()
    MUTEX_T = threading.Semaphore()
    def __init__(self):
        self.proxy_list={}
        f = open(proxy_spider_config["proxy_file_path"],"r")
        
        for line in f.readlines():
            #减一为了去掉换行符
            line =line[0:len(line)-1]
            self.proxy_list[line]=True
        f.close()
        self.proxy_queue = Queue.Queue()
        for proxy in self.proxy_list.keys():
            self.proxy_queue.put(proxy)
            
        return
    
    
    def get_proxy(self):
        return self.proxy_queue.get()
    
    def put_proxy(self,proxy):
        self.proxy_queue.put(proxy)
        
    #调用该方法需要加锁
    def del_proxy(self,proxy):
        if self.proxy_list.has_key(proxy):
            del self.proxy_list[proxy]
#        self.proxy_list.remove(proxy)
        self.proxy_queue =Queue.Queue()
        for proxy in self.proxy_list.keys():
            self.proxy_queue.put(proxy)
            
    
        
        
        
        
        
#    def update_proxy_list(self):
#        #遍历每个ip
#        threads =[]
#        for ip in self.proxy_list.keys():
#            #对每个ip启用一个检查ip的线程
#            t1 = threading.Thread(target=self.does_function,args=(self.proxy_list,ip))#指定目标函数，传入参数，这里参数也是元组  
#            threads.append(t1)
#        for thread in threads:
#            thread.start()
#            print "start!"
#        for thread in threads:
#            thread.join(8)
#        f = open(proxy_spider_config["proxy_file_path"],"w")
#        count=0
#        for ip in self.proxy_list.keys():
#            f.write(ip+"\n")
#            count = count+1
#        print count
#        f.close()
#                
#        
#            
#                 
#        
#        pass
#    
#    def ip_queue(self):
##        len = self.get_ip_num()
#        queue =Queue.Queue()
#        for ip in self.proxy_list.keys():
#            queue.put(ip)
#        return queue
#    def getip(self):
#        
#        return self.proxy_list.popitem()[0]
#    
#    def puship(self,ip):
#        self.proxy_list[ip]=True
#    
#    def get_ip_num(self):
#        print len(self.proxy_list)
#    
#    
#    
#    
#    #检查proxy是否可用    
#    def does_function(self,pool,ip):
#        url='http://www.amazon.cn'
#        proxy_url = 'http://'+ip
#        proxy_support = urllib2.ProxyHandler({'http': proxy_url})
#        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#        r=urllib2.Request(url)
#        r.add_header("Accept-Language","zh-cn")    #加入头信息，这样可以避免403错误
#        r.add_header("Content-Type","text/html; charset=gb2312")
#        r.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)")
#        trycount=1
#        Ti=10
#        while trycount<=2:
#            try:
##                IpPool.MUTEX_T.acquire()
#                T0=time.clock()
#                f=opener.open(r,timeout=2)
#                data=f.read()
#                Ti=time.clock()  
##                IpPool.MUTEX_T.release()
#                if '亚马逊' in data:
#                          
#                    break
#                else:
#                    print "bad"
#                    return []
#            except:
#                time.sleep(1)
#                trycount=trycount+1
#        if trycount>2:
#            print "bad"
#            IpPool.MUTEX_D.acquire()
#            del pool[ip]
#            IpPool.MUTEX_D.release()
#            return False
#        else:
#            return True