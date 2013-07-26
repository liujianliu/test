#coding=utf-8
'''
Created on 2013-7-3

@author: liujian
'''
class StringST():
    class Node():
        def __init__(self,value=None,size=0,R=256):
            self.pArray=[None for i in range(0,R)] #数组初始化,假设字符以ascII码编码        
            self.value=value
            self.R = R
            self.size=size
            
    def __init__(self,fil=None):
       
        if fil:
            
            self.root= self.Node()#调用自己的方法必须加self
            content = fil.readlines()
            for line in content:
#               print line
                line = line[0:len(line)-1]#为了把那个恶心的\n给去掉
                print line
                self.put(line,line)
        else:
            self.root= self.Node()#调用自己的方法必须加self
#将key-value插入到单词查找树中
    def put(self,key,val):
        length = len(key)
        temp = self.root
        for i in range(0,length):#不包括length
            c = key[i]
            
            index =ord(c)
            if temp.pArray[index]:  #如果不为空
                temp = temp.pArray[index]
            else:
                temp.pArray[index] = self.Node()
                temp = temp.pArray[index]
        temp.value=val
     
     
     
        
    def get(self,key):
        return self.__get(self.root, key)
    
    def __get(self,node,key):
        length = len(key)
        temp = node
        for i in range(0,length):
            c = key[i]
            index = ord(c)
            if temp.pArray[index]:
                temp = temp.pArray[index]
            else:
                return ''
        if temp.value:
            return temp.value #返回该节点
        else :
            return ''
    
    
    
        
    def size(self):
        return self.__size(self.root)
        
    def __size(self,node):#键的数量描述 如果value值不为零则count++，否则遍历他的所有指针节点
        if not node:
            return 0
        else:
            count =0
            if node.value:
                count+=1
            for cNode in node.pArray:
                count= count+self.__size(cNode)#调用本身的方法要加self.
            return count  
        
        
        
    def delete(self,key):
        self.__delete(self.root, key, 0)
        
    def __delete(self,node,key,index):
        if not node :
            return None
        if index==len(key):
            node.value = None
        else:
            c = key[index]
            node.pArray[ord(c)]=self.__delete(node.pArray[ord(c)], key, index+1)
        #判断是否其value非空，若是则返回该节点
        if node.value:
            return node
        #判断其是否有非空链接，若有则返回
        for i in range(0,node.R):
            if node.pArray[i]:
                return node
        #若以上两种情况均不存在则删除该节点
        return None
    
    


    
    def values(self):
        ret=[]
        self.__values(self.root,ret)
        return ret
    
    def __values(self,node,ret):
        if not node:
            return None
        if node.value:
            ret.append(node.value)
        for n in node.pArray:
            self.__values(n,ret)
        
        
        
        
    
    

                
        
        
if __name__ == '__main__':
#    st = StringST()
#    st.put("liu", "smart")
#    st.put("lj","google")
#    print st.get("lj")
#    print st.size()
#    print st.keysWithPrefix("li")
    
    f = open(r"D:\book_scraper\book_scraper\spider\com\duokan\proxies.txt","r")
    st1 = StringST(fil=f)
    print "删除前"+str(st1.size())
    st1.delete("8")
    print "删除后"+str(st1.size())#要加个换行符才能找到...
    
    values = st1.values()
    print "共有"+str(len(values))
                
        
                
            
