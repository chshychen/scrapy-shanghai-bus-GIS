# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 14:13:24 2016

@author: chensheng.cheney
"""
import urllib2
from urllib2 import URLError
import re
from bs4 import BeautifulSoup
import sys
import MySQLdb
import time
import json
import string
import datetime


#########

 #MYSQL IP ***.***.**.***   3306
 #用户密码是username  password 修改自己的用户名与密码，ip地址，db=数据库名称
def storeData(table):
    conn = MySQLdb.connect(host='***.***.**.***', user='username', passwd='password', db='****', charset='utf8')
    c = conn.cursor()
    sql = ' CREATE TABLE IF NOT EXISTS zhandian(scrapydate varchar(255),label varchar(255), URL varchar(255), name varchar(255),URL2 varchar(255),  Content text(65535))'
    c.execute(sql)
    today = str(datetime.date.today())
    for each in table:
        if each:
            if len(each)==5:
                sql = "INSERT INTO zhandian(scrapydate,label, URL, name,URL2, Content) values (%s,%s,%s,%s,%s,%s)"
                param = (today,each[0], each[1], each[2],each[3] ,each[4])
                c.execute(sql, param)
    conn.commit()
    c.close()
    conn.close()
  

##每个站点的经纬度函数  
def  scrape_jingweidu(page):
    #page="http://shanghai.8684.cn/z_cc3d3dc2"
    #page="http://shanghai.8684.cn/z_41ab01d9"
    html=urllib2.urlopen(page).read()
    Soup=BeautifulSoup(html)
    List=[]
    try:
        str1=Soup.findAll('div',{'class':'site_map_content'})
        str2=BeautifulSoup(str(str1)).find('img')['src']
        jw=re.findall(r'.*(\d\d\d\.\d+\,\d\d.\d+).*',str2)
        if len(jw)==0:
            jw=['*']
    except:jw=['*']
    return jw
    
    
    
##########抓取每个站点名函数 
def scrape_zhandian(page):
    #page="http://shanghai.8684.cn/x_424ca83a"
    #page="http://shanghai.8684.cn/x_d657401b"
    html=urllib2.urlopen(page).read()
    Soup=BeautifulSoup(html)
    #List=[]
    try:
        str1=Soup.findAll('div',{'class':'bus_site_layer'})
        datall=''
        for i in str1:
            lin2=BeautifulSoup(str(i)).findAll('a')
            na_jw=''
            for j in lin2:
                name=BeautifulSoup(str(j)).get_text()
                url='http://shanghai.8684.cn'+BeautifulSoup(str(j)).find('a')['href']
                jw=scrape_jingweidu(url)
                name_jw=name+':'+jw[0]
                na_jw=na_jw+'=>'+name_jw
            datall=datall+'||'+na_jw
    except:datall=''
    return datall            
                 
        
def scrape_linename(page):
    #ID = re.findall(r'[0-9]+', page)[0]
    page="http://shanghai.8684.cn/line2"
    html = urllib2.urlopen(page).read()
    Soup = BeautifulSoup(html)   
    #try:
    List = []
    str1=Soup.findAll('div',{'class':'stie_list','id':'con_site_1'})
    chat=BeautifulSoup(str(str1)).findAll('a')
    for i in chat:
        name=BeautifulSoup(str(i)).get_text()
        url='http://shanghai.8684.cn'+BeautifulSoup(str(i)).find('a')['href']
        datall=scrape_zhandian(url)
        List.append([name,url,datall])
    #except:List.append(['','',''])
    return List


def scrapy_page():   
    URL="http://shanghai.8684.cn"
    try:
        #data=[]
        baseHtml = urllib2.urlopen(URL).read()
        soup = BeautifulSoup(baseHtml)
        line=soup.find('div',{'class':'bus_layer_r'})            
        url=BeautifulSoup(str(line)).findAll('a')
        data=[]
        for b in url:
            name=BeautifulSoup(str(b)).text
            lineurl=URL+BeautifulSoup(str(b)).find('a')['href']            
            data.append([name,lineurl])
    except:data.append(['',''])
    return data                
            #print 'Storage completed.'

#http://shanghai.8684.cn/line2
def main():   
    #URL="http://shanghai.8684.cn"
    try:
        data=scrapy_page()
        lena=len(data)
        for i  in range(2):#range(lena):
            name=data[i][0]
            url=data[i][1]
            if url!='':
                List=scrape_linename(url)
                leng=len(List)
                da=[]
                for i in range(leng):                
                    da.append([name,url,List[i][0],List[i][1],List[i][2]])
                storeData(da)
            sleep(10)
    except:print 'no completed'                
            #print 'Storage completed.'


if __name__ == '__main__':
    main()

