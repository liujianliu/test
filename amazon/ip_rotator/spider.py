# coding: utf8
import gzip
import StringIO
import urllib2
import random
import time
from const import user_agents
from datetime import datetime

class Spider(object):

    def __init__(self, name, host, user_agents='', cookie=''):
        self.name = name
        self.headers = {
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'zh-CN',
            'Connection': 'Keep-Alive',
            }
        self.user_agents = user_agents
        self.cookie = cookie

    def log(self, info):
        print "%s [%s] INFO: %s" % (str(datetime.now()), self.name, info)

    def extract(self, url, pattern, encoding=None, nb_retries = 0, retry_delay = 0):
        s = self._fetch_url(url, nb_retries = nb_retries, retry_delay = retry_delay)
        ret = {}
        if s == None:
            return ret

        try:
            if encoding not in [None, 'utf8', 'utf-8']:
                s = s.decode(encoding).encode('utf8')
        except:
            pass

        # FIXME(Dong Wang): multi-pattern match algorithm is needed here
        for nm, pat in pattern.items():
            ret[nm] = pat.findall(s)
        return ret
    
    
    
    def fetch_obj(self, url, nb_retries = 0, retry_delay = 0):
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
                g = urllib2.urlopen(request, None,20)
                if g.headers.get('content-encoding', '') == 'gzip':
                    data = StringIO.StringIO(g.read())
                    gzipper = gzip.GzipFile(fileobj=data)
                    html = gzipper
                    return html
                else:
                    return g
            except Exception, e:
                self.log("exception caught while fetch %s: %s" % (url, str(e)))

            nb_tried += 1
            time.sleep(random.uniform(retry_delay*0.5, retry_delay*1.5))
            retry_delay *= 0.2

        self.log("return None from %s" % url)
        return None

    def fetch(self, url, nb_retries = 0, retry_delay = 0):
        return self._fetch_url(url, nb_retries = nb_retries)
    
    def _fetch_url(self, url, nb_retries = 0, retry_delay = 0):
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
                g = urllib2.urlopen(request, None,20)
                if g.headers.get('content-encoding', '') == 'gzip':
                    data = StringIO.StringIO(g.read())
                    gzipper = gzip.GzipFile(fileobj=data)
                    html = gzipper
                    return html.read()
                else:
                    return g.read()
            except Exception, e:
                self.log("exception caught while fetch %s: %s" % (url, str(e)))

            nb_tried += 1
            time.sleep(random.uniform(retry_delay*0.5, retry_delay*1.5))
            retry_delay *= 0.2

        self.log("return None from %s" % url)
        return None

