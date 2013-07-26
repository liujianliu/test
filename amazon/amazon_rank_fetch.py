# coding: utf8
'''
Created on 2013-7-11

@author: liujian
'''
import sys
import json
import Queue
import csv
import threading
import time
import re
from ip_rotator.spider import Spider
from threading import Thread
#import pickle
reload(sys)
sys.setdefaultencoding("utf-8")
class ExtractBook():
    def __init__(self,bookurl_queue,count):
        self.json_config=  f = open("config","r")
        #载入json对象
        self.json_config = json.load(f)
        f.close()
        self.spider = Spider("duokan","localhost")
        self.bookurl_queue=bookurl_queue
        self.csvfile = open(self.json_config["csv_path"], 'wb')
        self.csv_writer = csv.writer(self.csvfile,dialect="excel")
        self.count = count#用于计数
        self.book_cache=self.gen_books_from_csv()
    #从配置中Load一本书的pattern，解析后生成json对象的book
    def __extract_book(self,html):
        try:
            book_pattern = self.json_config["book"]        
            ret={}
            for field in book_pattern.keys():
                pattern_pair =book_pattern[field]
                start_partten =pattern_pair[0]
                end_partten =pattern_pair[1]
                start_partten =start_partten.encode("utf-8")
                end_partten = end_partten.encode("utf-8")
                content = ExtractRank.fetch_content_string_match(start_partten, end_partten, html)
                ret[field]=content            
            return ret
        except:
            print "extract book failed"
        return None
    #从已抓取的csv中生成book对象
    def gen_books_from_csv(self):
        csv_path=self.json_config["csv_bak_path"]
        with open(csv_path, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, dialect='excel')
            books_dic={}
            co=0
            for row in spamreader:
                try:
                    bookid=row[2]
                    bookid = bookid.lstrip()
                    bookurl ="http://www.amazon.cn/dp/"+bookid
                    if not books_dic.has_key(bookurl):
                        book={}
                        book["versions"]=unicode(row[5],"utf-8")                        
                        book['kindleprice']=unicode(row[6],"utf-8")
                        book["title"] =unicode(row[3],"utf-8")
                        book["code"]=bookid
                        book["publisher"]=unicode(row[1],"utf-8")
                        book["brand"]=unicode(row[4],"utf-8")
                        books_dic[bookurl]=book
                        co+=1
                except:
                    print"it`s empty"
            print "\n"
            print str(co)
            return books_dic
    
    #逻辑主体    
    def extract_book_action(self):
        while True:
            try:      
                book_url_rank_category=self.bookurl_queue.get()#queue为空的时候将被阻塞
                url_rank_category = book_url_rank_category.popitem()#将list? 的 第一个元素pop出来bookurl:(count,bookcategory)
                book={}            
                if not self.book_cache.has_key(url_rank_category[0]):
                    bookpage = self.spider.fetch(url_rank_category[0], nb_retries=2, retry_delay=0.5)
                    book =self.__extract_book(bookpage)
                else:
                    book.update(self.book_cache[url_rank_category[0]])
                book["rank"]=url_rank_category[1][0]
                book["category"] =url_rank_category[1][1]
                book["datetime"]=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
                self.csv_writer.writerow(book.values())
                self.count+=1
                print str(self.count)
            except:
	    	print sys.exc_info()[0]
		print sys.exc_info()[1]
#            print book


class ExtractSeed():
    lock = threading.Lock() 
    def __init__(self,seed_queue,root_url,seed_bak_set=None):
        self.json_config=  f = open("config","r")
        #载入json对象
        self.__json_config = json.load(f)
        f.close()
        self.seed_queue = seed_queue
        self.spider = Spider("duokan","localhost")
        self.seed_pattern = self.__json_config["child_link_pattern"]
        self.has_visited =set()      
        self.root_url = root_url
        self.seed_bak_set = seed_bak_set
        
#    #将一个页面中的seeds抽出来    
#    def extract_seeds_in_one_page(self,html_page):
#        urlset=
#        return urlset
    
    def extract_seeds_action(self):
        self.__bfs(self.root_url)

    def __bfs(self,root):
        tem =Queue.Queue(maxsize = 0)
        tem.put(root)
        while not tem.empty():
            seed = tem.get();
            if not seed in self.has_visited:
                html_page = self.spider.fetch(seed, nb_retries=5, retry_delay=0)
                url_set = ExtractSeed.fetch_set(html_page,self.seed_pattern)
                ExtractSeed.lock.acquire()
                self.has_visited.add(seed)
                ExtractSeed.lock.release()
                for url in url_set:
                    if not url in self.has_visited:
                        tem.put(url)
                        self.seed_queue.put(url)
#                        print url 

#    def backup(self):
#        #备份has_visited
#        with open ( 'entry.pickle' , 'wb' ) as f :           
#            ExtractSeed.lock.acquire()
#            pickle.dump ( self.has_visited , f )
#            ExtractSeed.lock.release()
#            
#    def load_from_backup(self):
#        with open ( 'entry.pickle' , 'rb' ) as f :
#            entry = pickle . load ( f )
#            self.has_visited=self.has_visited|entry
    
    #抽取一个页面中符合url_pattern的url并返回url_set               
    @staticmethod
    def fetch_set(page,url_pattern):
        try:       
            tem=[]
            p = re.compile(url_pattern)
            matches = p.finditer(page)
            for match in matches:
                tem.append(page[match.start():match.end()])
            return set(tem)
        except:
            print "fetch set failed" 
        return None
  
class ExtractRank():
    def __init__(self,bookurl_queue,seeds_queue):
        self.json_config=  f = open("config","r")
        #载入json对象
        self.json_config = json.load(f)
        f.close()
        self.spider = Spider("duokan","localhost")
        self.bookurl_queue=bookurl_queue
        self.seeds_queue = seeds_queue
        
    #抽取出一个seed中的按rank顺序排列的booklist
    def fetch_book_list(self,rootpage):
        page_pattern = self.json_config["page_pattern"]        
        url_pattern = self.json_config["book_link_pattern"]       
        #获取当前页面的page链接,先用set存放去重，再存成list，排序，保证输出有序
        pageset =ExtractSeed.fetch_set(rootpage,page_pattern)
        pageset = list(pageset)
        pageset.sort()
        #获取当前页面的booklisturl链接
        book_list=[]
        for pageurl in pageset:
            page = self.spider.fetch(pageurl,nb_retries=5,retry_delay=1.5)
            book_list.extend(ExtractRank.fetch_list(page,url_pattern))#注意 此处抓取的链接有重复
        #由于抓取的bookurl相邻的两个重复，所有去一下重复，为了保证排名有序，不能用set,可能可以在正则表达式上改进一下
        count =0
        ret=[]
        for bookurl in book_list:
            if count%2==0:
                ret.append(bookurl)
            count=count+1
        return self.__pre_process_booklist(ret)    
    
    #将http://www.amazon.cn/%E5%A5%BD%E5%A6%88%E5%A6%88%E8%83%9C%E8%BF%87%E5%A5%BD%E8%80%81%E5%B8%88/dp/B008CM3SUW/ref=zg_bs_143291071_1
    #转换为http://www.amazon.cn/dp/B008CM3SUW/
    def __pre_process_booklist(self,booklist):
        newbooklist=[]
        for bookurl in booklist:
            start = "dp/"
            end = "/ref="
            bookid= ExtractRank.fetch_content_string_match(start,end,bookurl)
            tem = "http://www.amazon.cn/dp/"+bookid
            newbooklist.append(tem)
        return newbooklist

    #解析排名页bookurl与rank值，并放入队列中
    #队列中每个节点是一个dic。dic中只有一对key-value。key是一个url，value是一个元组（rank值，类别）
    def __extract_rank_action(self,html):
        sorted_booklist = self.fetch_book_list(html)
        p=self.json_config["book_category_pattern"]
        #这里不encode会出问题，我也没搞清楚为啥要encode,在linux中这里encode会报错    
        book_category=ExtractRank.fetch_content_string_match(p[0].encode("utf-8"), p[1].encode("utf-8"), html)
        #count用来记录排名     
        count=1        
        for book in sorted_booklist:
            book_rank_dic ={} 
            book_rank_dic[book]=(count,book_category)#首位是count，第二位是category
            count+=1
            self.bookurl_queue.put(book_rank_dic)#栈中存放键值对
            
    def extract_rank_action(self):
        while True:
            seed=self.seeds_queue.get()
            htmlpage = self.spider.fetch(seed, nb_retries=2, retry_delay=0)
            self.__extract_rank_action(htmlpage)
            
    #将一张html中start_str与end_str中间的内容抽取出来         
    @staticmethod        
    def fetch_content_string_match(start_str,end_str,html):
        try:            
            start_len = len(start_str)
            tem = html.find(start_str)
            start_pos = tem+start_len
            end_pos = html.find(end_str,start_pos)
            content = html[start_pos:end_pos]
            return content
        except:
            print "extract by str error"
        return "  "
    #将page中匹配url_pattern的链接装到list
    @staticmethod
    def fetch_list(page,url_pattern):
        try:
            tem=[]
            p = re.compile(url_pattern)
            matches = p.finditer(page)
            for match in matches:
                tem.append(page[match.start():match.end()])
            return tem
        except:
            print"list extract failed"
        return None
    
if __name__=="__main__":
    seed_queue = Queue.Queue(maxsize = 0)    
    bookurl_queue =Queue.Queue(maxsize=0)
    
    root_url ="http://www.amazon.cn/gp/bestsellers/digital-text/116169071/ref=sv_kinc_3"
    
    extract_seed =ExtractSeed(seed_queue=seed_queue,root_url=root_url)
    t1 = Thread(target=extract_seed.extract_seeds_action)
    t1.start()
    
    
    
    
    extract_rank = ExtractRank(bookurl_queue=bookurl_queue,seeds_queue=seed_queue)    
    t2 = Thread(target=extract_rank.extract_rank_action)
    t2.start()

    
    count =0
    extract_book =ExtractBook(bookurl_queue=bookurl_queue,count=count)
    t3 =Thread(target=extract_book.extract_book_action)
    t3.start()





        
