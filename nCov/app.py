#!/usr/bin/python3
#coding:utf-8


from pprint import pprint

from conf import geofile,outfile,bucket,dest
from shnCov2 import makechart
from cos import upload_to_cos
from get_geo import update_geo

# source https://lab.isaaclin.cn/nCoV/zh

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
    '2020-2-10':(1017,302,180,48,1),
    '2020-2-11':(1114,306,177,53,1),
    '2020-2-12':(1364,313,183,57,1),
    '2020-2-13':(1489,318,156,62,1),
    '2020-2-14':(1524,326,143,90,1),
    '2020-2-15':(1666,328,142,124,1),
    '2020-2-16':(1772,331,117,140,1),
    '2020-2-17':(1870,333,97,161,1),
    '2020-2-18':(2006,333,127,177,1),
    '2020-2-19':(2121,333,115,186,1),
    '2020-2-20':(2239,334,107,199,2),
    '2020-2-21':(2348,334,100,211,3),
    '2020-2-22':(2445,335,99,227,3),
    '2020-2-23':(2595,335,90,249,3),
    '2020-2-24':(2666,335,64,261,3),
    '2020-2-25':(2718,336,78,268,3),
    '2020-2-26':(2747,337,74,272,3),
    '2020-2-27':(2791,337,64,276,3),
    '2020-2-28':(2838,337,57,279,3),
    '2020-2-29':(2873,337,32,287,3),
    '2020-3-1':(2915,337,17,290,3),
    '2020-3-2':(2947,338,19,292,3),
    '2020-3-3':(2984,338,26,294,3),
    '2020-3-4':(3015,338,32,298,3),
    '2020-3-5':(3045,338,40,303,3),
    '2020-3-6':(3073,338,37,306,3),
    '2020-3-7':(3100,338,40,313,3),
    '2020-3-8':(3123,338,30,314,3),
    '2020-3-9':(3140,338,30,315,3),
    '2020-3-10':(3162,338,23,319,3),
    '2020-3-11':(3173,338,34,320,3),
    '2020-3-12':(3180,338,36,321,3),
    '2020-3-13':(3194,338,26,324,3),
    '2020-3-14':(3204,338,30,324,3),
    '2020-3-15':(3218,338,46,324,3),
    '2020-3-16':(3231,338,14,325,3), #统计不再包括境外输入
    '2020-3-17':(3241,338,6,325,3),
    '2020-3-18':(3250,338,3,326,3),
    '2020-3-19':(3253,338,0,326,3),
    '2020-3-20':(3261,338,0,326,3),
    '2020-3-21':(3267,338,0,327,3),
}


def main(geo=False):
    if geo:
        wx = input('>>>>')
        update_geo(wx)
    makechart(data)
    result = upload_to_cos(outfile,bucket,dest)
    print(result)


if __name__ == "__main__":
    main()
