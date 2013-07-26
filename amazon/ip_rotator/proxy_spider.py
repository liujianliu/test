# coding:utf8

import urllib2,re,thread,time,threading

import socket
socket.setdefaulttimeout(10)
from spider import Spider
from check_proxy_thread import CheckProxyThread
from string_search_tree import StringST
from config import proxy_spider_config




class IPSpider(Spider):
    def __init__(self, name, host, user_agents='', cookie=''):
        super(IPSpider, self).__init__(name,host,user_agents,cookie)
        self.proxy_list=[]
        self._fetch_proxies()
        self._check_proxy_list()

    def _fetch_proxies(self):
        pagenum=0       
        trycount=0
        while pagenum<=9 and trycount<=2:
            pagenum=pagenum+1
            url='http://www.cnproxy.com/proxy'+str(pagenum)+'.html'
            try:
                #html=urllib2.urlopen(url)
                html = self.fetch_obj(url, nb_retries=1, retry_delay=1)
                print html
                for line in html:
                    if "HTTP" in line:
                        proxy=line[line.find('<td>')+4:line.find('<SCRIPT')]                     
                        self.proxy_list.append(proxy)
            except:
                trycount=trycount+1
                pagenum=pagenum-1      
        return None
    
    
    
    def _check_proxy_list(self,step=100):         
        #每次3个线程来检查proxy  
        proxy_length = len(self.proxy_list)
        temp_list=[]
        for proxy in self.proxy_list:
            temp_list.append(proxy) 
        
        
        print "共有"+str(proxy_length)+"个待查proxy" 
        start =0        
        while start<=proxy_length:
            end=-1
            if start+step <= proxy_length:
                end = start+step
            end = start+step
            threads=[]            
            print "进行到"+str(start)
            #每次启用三个线程，对proxy进行检查
            for proxy in temp_list[start:end]:
                #创建 opener与request
               
                proxy_url = 'http://'+proxy
                proxy_support = urllib2.ProxyHandler({'http': proxy_url})
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
                url='http://www.amazon.cn'
                r=urllib2.Request(url)
                r.add_header("Accept-Language","zh-cn")    #加入头信息，这样可以避免403错误
                r.add_header("Content-Type","text/html; charset=gb2312")
                r.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)")  
                #启动线程
                thread = CheckProxyThread(proxy,r,opener)
                threads.append(thread)
                thread.start()
                time.sleep(0.3)
            for thread in threads:
                thread.join(5)
            for thread in threads:
                if not thread.does_func:
                    self.proxy_list.remove(thread.proxy)
            print "剩余proxy数量为"+str(len(self.proxy_list))
            start = start+step
        return None
    
    def persist_proxylist(self):
        filepath= proxy_spider_config["proxy_file_path"]
        f = open(filepath,'w')
        for proxy in self.proxy_list:
            f.write(proxy+"\n")
        f.close()

            
                    
        
        
        
    def get_proxylist(self):
        return self.proxy_list
    
    def print_proxylist(self):
        print self.proxy_list


if __name__ == '__main__':
    
    pl = IPSpider(name="duokan",host="localhost")
    
#    pl.print_proxylist()
#    
#    pl.proxy_list.remove("199.115.231.51")
#    
#    pl.print_proxylist()
    
    pl.persist_proxylist()
    
    pl.print_proxylist()
    
    
   
    #先读出文本中的proxy至trie中，验证每个proxy正确性，将不符合的proxy删除
    #然后再爬取新的链接更新trie
    #再将遍历新trie树写回到文件中
   
    
   
#    f = open(proxy_spider_config["proxy_file_path"],"r")
#    st = StringST(fil=f)
#    f.close()
#    #以下代码检查查找树中各proxy是否还可用，不可用则从树中删除该proxy,删除操作在updateTrie中执行
#    
#    print "检查之前，文本中的proxy数量为" + str(st.size())
#    #遍历trie中所有的ip
#    ips = st.values()
#    threads=[]
#    for ip in ips:
#        spider = CheckProxyThread(ip,trie=st)
#        t = threading.Thread(target=spider.updateTrie)
#        threads.append(t)
#    for thread in threads:
#        thread.start()
#    for thread in threads:
#        thread.join(10)
#        
#    print "检查后，文本中的proxy数量为" + str(st.size())
#    
#    
#        
#    #以下代码将新抓来的proxy中可用的加入到st中，insert操作在run()方法中执行
#    sp = IPSpider('duokan','localhost')
#    proxyList= sp.get_proxies()
#    print "长度是"+str(len(proxyList))
#    threads=[]
#    for proxy in proxyList:
#        threads.append(CheckProxyThread(proxy,trie=st))
#    for thread in threads:
#        thread.start()
#    for thread in threads:
#        thread.join(10)
#    print "更新后，文本中的proxy数量为" + str(st.size())
#    
#    
#    
#    #以下代码将更新后的ip写入文本中,有点问题
#    newips = st.values()
#    w =open(proxy_spider_config["proxy_file_path"],"w")
#    for ip in newips:
#        w.write(ip+"\n")
#    w.close()
    
  

    
            
            
    
        
        
        