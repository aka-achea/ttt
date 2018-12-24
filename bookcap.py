﻿#!/usr/bin/python
#coding:utf-8
"""
SCAN eBOOK
"""

import time , os
import pyautogui as auto

path = 'E:\\SIR\\book'
name = input('Book Name: ')
pages = input('Total page: ')
bp = os.path.join(path,name)
if os.path.isdir(bp) == True:
    print('Book folder exist')
else:
    os.mkdir(bp)
# print(bp)
os.chdir(bp)

auto.size()
width, height = auto.size()
print(width,height)
auto.PAUSE = 1
auto.click(150,150,button='left')


def scan(name,p):
    png = name+"_"+p+".png"
    auto.screenshot(png,region=(125,90, 620, 815))

for p in range(1,int(pages)):
    scan(name,str(p))
    time.sleep(1)
    auto.typewrite(['right'])


print('finish book capture')

"""
change log:
2018.12.7 resize with new screen v1.1
2017.6.21 build basic screenshot funciton v1.0
"""