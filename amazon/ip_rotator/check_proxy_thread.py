#coding=utf-8
'''
Created on 2013-7-3

@author: liujian
'''
import threading
import urllib2,time
COUNT = 0
MUTEX_COUNT = threading.Semaphore()
MUTEX_WRITE = threading.Semaphore()
MUTEX_TIME = threading.RLock()
urllib2.socket.setdefaulttimeout(10)
class CheckProxyThread(threading.Thread):
    def __init__(self,proxy,request,opener,f=None,trie=None):
        threading.Thread.__init__(self)
        self.proxy = proxy
        self.does_func =False
        self.request = request
        self.opener = opener
#        if f:
#            self.wfile = f
#        if trie:
#            self.trie = trie
            
            
            
    def run(self):
        self.does_func =self.does_function()
        
    def is_useful(self):
        return self.does_func
    
    #检查proxy是否可用    
    def does_function(self):
#        url='http://www.amazon.cn'
#        proxy_url = 'http://'+self.proxy
#        proxy_support = urllib2.ProxyHandler({'http': proxy_url})
#        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#        r=urllib2.Request(url)
#        r.add_header("Accept-Language","zh-cn")    #加入头信息，这样可以避免403错误
#        r.add_header("Content-Type","text/html; charset=gb2312")
#        r.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)")
        trycount=1
        while trycount<=2:
            try:
                T0=time.time()
                f=self.opener.open(self.request)
                data=f.read()
                if '亚马逊' in data:
                    T=time.time()-T0        
                    break
                else:
                    print "bad"
                    return []
            except:
                time.sleep(0.5)
                trycount=trycount+1
        if trycount>2:
            print "bad"
            return False
        else:
            return True
    
    
    
    
    
            
## 多线程状态下，检查proxy是否在树中 
#    def does_exist(self):#相当于读操作
#        global COUNT
#        global MUTEX_COUNT
#        global MUTEX_WRITE
#        MUTEX_COUNT.acquire()#互斥访问count
#        if COUNT == 0:
#            MUTEX_WRITE.acquire()#第一个读者要抢占读写权限
#        COUNT+=1
#        MUTEX_COUNT.release()#释放对count的加法操作
#        flag = True
#        if not self.trie.get(self.proxy):
#            flag=False
#            
#        MUTEX_COUNT.acquire()
#        COUNT-=1
#        if COUNT==0:
#            MUTEX_WRITE.release()
#        MUTEX_COUNT.release()
#        return flag
    
    

        
    
             

    
    
            
        
    
    #对Trie进行删除操作    
#    def updateTrie(self):
#        if not self.does_function():            
#            global MUTEX_WRITE
#            MUTEX_WRITE.acquire()
#            self.trie.delete(self.proxy)
#            MUTEX_WRITE.release()
    
    
    
#    def run(self):
#        if self.does_function():
#            global MUTEX_WRITE
#            MUTEX_WRITE.acquire()
#            self.trie.put(self.proxy,self.proxy)
#            MUTEX_WRITE.release()
            
        
        
           

            
        