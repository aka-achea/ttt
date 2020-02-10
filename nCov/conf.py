#!/usr/bin/python3
#coding:utf-8

from configparser import ConfigParser

baiduconf = r'M:\GH\_pri\baidu.ini'
config = ConfigParser()
config.read(baiduconf)
ak_geo = config.get('BaiduMap','ak_2020_srv') 
sk_geo = config.get('BaiduMap','sk_2020_srv')
ak_web = config.get('BaiduMap','ak_nCovApi_browser')
ak_dev = config.get('BaiduMap','ak_dev_browser')

qconf = r'M:\MyProject\nCov\qcloud.ini'
bucket = '2020-1301184162'
target = r'M:\MyProject\nCov\render.html'
outfile = r'M:\MyProject\nCov\out.html'
dest = 'render.html'
logbucket = 'log-1301184162'
logdir = r'M:\MyProject\nCov\log'
geofile = r'M:\MyProject\nCov\geo.json'

#width:200px;height:50px;font-weight: bold;font-size: 20px;
#http://api.map.baidu.com/lbsapi/getpoint/index.html

sumarysample = [('浦东新区', 32), ('静安区', 8),('宝山区', 8), ('闵行区', 7), ('长宁区', 7), ('徐汇区', 7),('金山区', 1),
 ('虹口区', 5), ('黄浦区', 5), ('奉贤区', 5), ('松江区', 3),('青浦区', 2), ('杨浦区', 2), ('嘉定区', 2), ('普陀区', 2) ]

data = {#date,(death,上海累计确诊,上海现有疑似,上海治愈,上海死亡)
    '2020-1-20':(0,1,2,0,0),
    '2020-1-21':(1,9,10,0,0),
    '2020-1-22':(7,16,22,0,0),
    '2020-1-23':(18,20,34,0,0),
    '2020-1-24':(26,33,72,1,0),
    '2020-1-25':(39,40,95,1,1),
    '2020-1-26':(56,53,90,1,1),
    '2020-1-27':(82,66,129,3,1),
    '2020-1-28':(106,80,167,4,1),
    '2020-1-29':(170,101,180,5,1),
    '2020-1-30':(213,128,164,5,1),
    '2020-1-31':(259,153,167,9,1),
    '2020-2-1':(304,177,168,10,1),
    '2020-2-2':(361,193,173,10,1),
    '2020-2-3':(425,208,168,10,1),
    '2020-2-4':(490,233,194,12,1),
    '2020-2-5':(564,254,196,15,1),
    '2020-2-6':(637,269,166,25,1),
    '2020-2-7':(723,281,181,30,1),
    '2020-2-8':(812,292,205,41,1),
    '2020-2-9':(909,295,223,44,1),
}


location = [
    ["上海市长宁区虹桥街道虹桥路1024弄",1],
    ["上海市徐汇区枫林路街道东安二村",1],
    ["上海市徐汇区安吉斯铭汽车销售服务有限公司",1],
    ["上海市普陀区曹杨新村街道连亮路111弄",1],
    ["上海市杨浦区定海路街道宁武路218弄",1],
    ["上海市浦东新区阳光花城",1],
    ["上海市浦东新区芳草路欧麦克KTV",1],
    ["上海市浦东新区民乐城兰丽苑",1],
    ["上海市浦东新区金京路地铁站",1],
    ["上海市浦东新区新高苑",1],
    ["上海市浦东新区锦江之星风尚酒店(机场镇店)",1],
    ["上海市嘉定区江桥镇金园一路1118弄",1],
    ["上海市嘉定区首创旭辉城",1],
    ["上海市宝山区海尚菊苑",1],
    ["上海市宝山区采菊苑",1],
    ["上海市奉贤区南行贤苑",1],
    ["上海市松江区新桥镇华兴小区",1],
    ["上海市松江区沃天百联生活超市(新桥店)",1],
    ["上海市闵行区虹桥火车站",1],
    ["上海市徐汇区炎虹路76弄",1],
    ["上海市浦东新区汤臣豪园四期",1],
    ["上海市浦东新区陆家嘴锦绣前城",1],
    ["上海市浦东新区证大家园",1],
    ["上海市浦东新区浦东国际机场",1],
    ["上海市浦东新区上海贺普药业股份有限公司",1],
    ["上海市静安区嘉利明珠城",1],
    ["上海市松江区乐都西路1636弄",1],
    ["上海市松江区久阳文华府邸",1],
    ["上海市松江区亭中小区",1],
    ["上海市松江区地铁九号线九亭站",1],
    ["上海市松江区松江大学城站",1],
    ["上海市长宁区新华豪庭",1],
    ["上海市嘉定区华润中央公园",1],
    ["上海市宝山区南秀雅苑",1],
    ["上海市宝山区共康雅苑（二期）",1],
    ["上海市奉贤区南桥镇阳光二期",1]
]

