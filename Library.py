#!/usr/bin/python3
#coding:utf-8
#tested in win


from urllib.error import URLError
# from urllib.parse import quote
import re,os,json, time, shutil,sys,sqlite3,argparse,random
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
from prettytable import PrettyTable , from_db_cursor
import requests

# customized module
from mylog import mylogger,get_funcname
from openlink import op_simple,op_requests
from mytool import mywait

# headers = {
#     "Accept":"text/html,application/xhtml+xml,application/xml; " \
#         "q=0.9,image/webp,*/*;q=0.8",
#     "Accept-Encoding":"text/html",
#     "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
#     "Content-Type":"application/x-www-form-urlencoded",
#     "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 "\
#         "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
# }

ignorelist = ['因装修暂闭馆','闭馆修缮']
blacklist = ['徐汇华泾镇','青浦夏阳','崇明港西镇',\
            '浦东洋泾','浦东新区新川沙','浦东沪东新村','杨浦长白新村','杨浦四平',\
            '奉贤分馆','闵行分馆','闵行莘庄工业区','嘉定分馆','嘉定分馆(新馆)','松江分馆','']
whitelist = ['普陀分馆','黄浦分馆','静安区图书馆(新闸路)','普陀宜川']

plink = set() #link to different pages of version list
# num = [] #link to book version number
# version = [] #link to different book version
link = set() #link to library list of different pages
D = {}
fail = []
masterpath = 'E:\\UT\\'
= 10
logfile = masterpath+'library.log'
database = masterpath+'library.db'
wishlist = masterpath+'library.ini'
# basicquery = "http://ipac.library.sh.cn/ipac20/ipac.jsp?menu=search&aspect=basic_search&profile=sl&ri=&index=.TW&term="
queryapi = 'http://ipac.library.sh.cn/ipac20/ipac.jsp'

"""
TW = 题名
AW = 著者
SW = 主题
SE = 丛书名
PW = 出版者
"""

# class dec: # tracer
#     def __init__(self,func):
#         self.func = func
#     def __call__(self,*args, **kw):
#         # l.verbose('>>>> Call %s()' % self.func.__name__)
#         #start = datetime.datetime.now().microsecond
#         result = self.func(*args, **kw)
#         #elapsed = (datetime.datetime.now().microsecond - start)
#         # l.verbose('<<<< Exit %s()' % self.func.__name__)
#         #l.verbose('++++ Function '+self.func.__name__+' spend ' +str(elapsed)
#         return result


def modificate(text):
    ml = mylogger(logfile,get_funcname()) 
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    text = str(text)
    before = text
    text = text.replace('&amp;', u'&')
    text = text.strip()
    #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
    after = text
    if before != after :
        ml.debug("Before modify >>>> "+before)
        ml.debug("After modify >>>> "+after)
    return text

def filter_lib(lib):
    #  map(lambda x:re.search(x,lib),ignorelist) :
    if lib in blacklist:
        return False
    else:
        for s in ignorelist:
            if re.findall(s,lib) is not None:
                return False
            else:
                return True

class db():
    def create(self):
        ml = mylogger(logfile,get_funcname()) 
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cmd = 'create table inventory (SN varchar(20) primary key,\
                        book varchar(20),lib varchar(20),cat varchar(20)  )'
        ml.debug(cmd)
        cursor.execute(cmd)
        cursor.close()
        conn.close()

    def lib(self,lib):
        ml = mylogger(logfile,get_funcname())        
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        # cmd = 
        # ml.debug(cmd)
        cursor.execute('select distinct book as 图书, cat as 索书号 from inventory \
                        where lib = ? order by book' , (lib,))
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def all(self):
        ml = mylogger(logfile,get_funcname())          
        ml.info(">>>>>>>显示所有图书<<<<<<<")
        ml.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select lib as 图书馆,book as 书,SN,cat as 索书号 from inventory ')
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def sum(self):
        ml = mylogger(logfile,get_funcname())          
        ml.info(">>显示书种类最多的图书馆<<")
        ml.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select lib as 图书馆,count(distinct(book)) as 本 from inventory \
                        group by 图书馆 having 本 > 1 order by 本 desc limit 10')
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def book(self,book):
        ml = mylogger(logfile,get_funcname())          
        ml.info(">>>>显示有此书的图书馆<<<<")
        ml.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct lib as 图书馆, book as 书,cat as 索书号 from inventory \
                        where book like ?', (book,))
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def listbook(self):
        ml = mylogger(logfile,get_funcname())          
        ml.info(">>>>显示找到的图书列表<<<<")
        ml.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct book, cat from inventory')
        values = cursor.fetchall()
        for i in values: ml.info(i)
        cursor.close()
        conn.close()

# @dec  #return version,num
def find_book_ver(queryapi,book,author=''):
    ml = mylogger(logfile,get_funcname())  
    para = [('menu','search'),
        ('index','.TW'),
        ('term',book),
        ('index','.AW'),
        ('term',author)]
    ml.debug(para)    
    try:
        # global version,num
        version,num = [],[]
        html = op_requests(url=queryapi,para=para)
        ml.debug(html.url)
        bsObj = BeautifulSoup(html.content,"html.parser")
        nobook = bsObj.find_all(string=re.compile("对不起"))
        if nobook: # not find any book
            ml.err("对不起, 不能找到任何命中书目")
            return version,num  # all none
        else:
            vbook = bsObj.find_all("a",{"class":"mediumBoldAnchor"})
            if vbook: # mediumBoldAnchor >= 1 , different version find, only scan 1st page
                ml.debug('Find book version below')
                for v in vbook:
                    ml.debug(v)
                    bookname = str(v).split('<')[1].split('>')[-1].strip()
                    # ml.info(bookname)
                    if bookname == book:
                        n = v
                        for i in range(7): n = n.parent                  
                        # ml.debug(n)
                        n = n.previous_sibling.text.strip()
                        # ml.debug(n)  # sample n :  "1."
                        ml.verbose(n+bookname)
                        num.append(n)
                        ml.verbose(v["href"])
                        version.append(v["href"])
                    else:
                        ml.info(bookname+' not match')
                        #sys.exit()
                        # pass
                if version == []: #there is book, but no name match
                    ml.error("都不符合，请确认书名")
                    return version,num  # all none
                # else:
                #     for i in version : l.debug(i)
            else: # mediumBoldAnchor = 0 , search directly
                ml.debug("没其他版本，直接搜!")
                version = 1
                num = html.url
                return version, num
    except AttributeError as e:
        print(e)
    return version,num

# @dec #return other library link
def find_other_lib(v):
    ml = mylogger(logfile,get_funcname())      
    try:
        global link
        #bookname = bsObj.find("a",{"class":"largeAnchor"})
        #print(bookname)
        #for i in bookname:  print(i["title"])
        #l.info(bookname["title"])
        T = 10
        while T != 0:  #find other library
            # html = op_simple(v)[0]
            html = op_requests(v)
            ml.debug(html.url)
            bsObj = BeautifulSoup(html.content,"html.parser")
            other = bsObj.find("input",{"value":"其它馆址"})
            ml.verbose(other)
            if other :
                T = 0
            else:
                T = T - 1
                ml.error("重新加载网页...")
                mywait(10)
        ol = (str(other).split(" "))
        ml.debug(ol)
        try:
            other_lib = modificate(ol[2][30:-2])
            ml.debug("Other lib is : ")
            ml.debug(other_lib)
            link.add(other_lib)
            #go to other_lib
            html = op_requests(other_lib)
            ml.debug(html.url)
            bsObj = BeautifulSoup(html.content,"html.parser")
            # find more page of other lib
            lk = bsObj.find_all(href=re.compile("staffonly=$"))
            for i in lk :  link.add(i["href"])
            ml.debug("Other lib list : ")
            ml.debug(link)
        except IndexError as e:
            ml.error("没有其他馆址")
    except AttributeError as e:
        print(e)
    #time.sleep(3)
    #find_library(bsObj)
    #print(link)
    return link

#馆址	馆藏地	索书号	状态	应还日期 馆藏类型 馆藏条码
# @dec
def find_library(bsObj,book):
    ml = mylogger(logfile,get_funcname())  
    global D, fail
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    for i in bsObj.find_all("tr",{"height":"15"}):
        status = i.td.next_sibling.next_sibling.next_sibling.text
        ml.verbose("="*10)
        if status == "归还":
            library = i.td
            ml.verbose("馆址:"+library.text)
            lib = library.text
            if filter_lib(lib) == True:       
                room = library.next_sibling
                ml.verbose("馆藏地:"+room.text)
                catalog = room.next_sibling
                ml.verbose("索引号:"+catalog.text)
                cat = catalog.text
                if bsObj.find(title="应还日期") :
                    #print("find 应还日期")
                    #index = room.next_sibling
                    #print(index.text)
                    btype = room.next_sibling.next_sibling.next_sibling.next_sibling
                else:
                    btype = room.next_sibling.next_sibling.next_sibling
                # bt = btype.text
                ml.verbose("馆藏类型:"+btype.text)
                label = btype.next_sibling
                ml.verbose("馆藏条码:"+label.text)
                SN = label.text

                if btype.text == "普通外借资料":
                    try:
                        cursor.execute("insert into inventory values (?,?,?,?)", (SN,book,lib,cat))
                    except sqlite3.IntegrityError as e:
                        ml.verbose(e)
                        ml.error("Duplicate: "+SN+" "+book+" "+lib)

        else:
            ml.info(status)

    cursor.close()
    conn.commit()
    conn.close()

# @dec
def single(book,author=''):
    ml = mylogger(logfile,get_funcname())  
    ml.info("搜寻图书："+book)
    if author:
        ml.info("作者："+author)
    version,num = find_book_ver(queryapi,book,author)
    if version == 1:        
        link = find_other_lib(num)
        for lib in link:
            ml.debug(lib)
            bsObj = op_simple(link)[0]
            find_library(bsObj,book)
    elif version == []:
        pass
    else:
        D = {num[i]:version[i] for i in range(len(version))}
        ml.debug(D) 
        ml.info("Scan version")
        for v in D:
            ml.info(v + book)
            link = find_other_lib(D[v])
        ml.debug("all link find below")
        for lib in link:
            ml.debug(lib)
            bsObj = BeautifulSoup(op_simple(lib)[0],"html.parser")
            find_library(bsObj,book)

def main():
    ml = mylogger(logfile,get_funcname())  
    parser = argparse.ArgumentParser(description = 'Library search tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m','--multiple',help='Search multiple books',action='store_true')
    group.add_argument('-c','--clean',help='Clean database',action='store_true')
    group.add_argument('-q',help='Query all|libary|single book|best',choices=['a','l','s','b'])
    parser.add_argument('-ql',help='Query one library')
    parser.add_argument('-qs',help='Query one book')
    parser.add_argument('-qb',help='Query best library',action='store_true')
    parser.add_argument('-b','--book',help='Search book ')
    parser.add_argument('-a','--author',help='Search author')
    args = parser.parse_args()

    if args.book:
        book = args.book
        single(book,args.author if args.author else '')
      
    elif args.multiple == True:
        ml.info('Search multiple books')
        with open(wishlist, 'r') as w:
            for i in w:
                book = i.strip()
                single(book)
    
    elif args.clean == True:
        ml.info('Clean up database')
        if os.path.isfile(database): os.remove(database)
        r = db()
        r.create()

    elif args.q == 'a':
        ml.info('all find')
        r = db()
        v = r.all()
        ml.info(v.get_string(fields = ['图书馆','书','SN','索书号']))

    elif args.q == 's':
        book = input('>>')
        ml.info('Search : '+book)
        r = db()
        v = r.book(book)
        ml.info(v.get_string(fields = ['图书馆','索书号']))

    elif args.q == 'l':
        lib = input('>>')
        ml.info(lib)
        r = db()
        v = r.lib(lib)
        ml.info(v.get_string(fields = ['图书','索书号']))

    elif args.q == 'b':
        # print('best')
        r = db()
        v = r.sum()
        ml.info(v.get_string(fields = ['图书馆','本']))

    else:
        parser.print_help()


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('ctrl + c')



"""
Changelog:
2019.3.13 add filter lib function v2.6
2019.3.11 Add author search key v2.5
2019.1.22 optimize argparse v2.4
2018.12.25 add keyinterrupt v2.3
2018.12.24 use argparse,prettytable v2.2
2018.1.15 add DB class v2.1
2018.1.13 fix log bug, optimize DB query v2.0
2018.1.4 add logger, dec v1.9
2017.11.5 update usage comment v1.8
2017.7.29 optimize sql query v1.7
2017.7.28 build multiple book query v1.6
2017.7.27 isolate single book query v1.5
2017.7.26 fix timeout issue v1.4
2017.7.25 add DB query v1.3
2017.7.24 enable logging, re-org structure v1.2
2017.7.23 add link search, fix column issue v1.1
2017.7.22 basic query funtion v1.0


Flow chart:
search_link find_book_ver  find_other_lib  find_library       query
    |             |               |              |              |
q2 ---> queryapi ---------> [version] ---> link ------------> lib ---> Result
"""
