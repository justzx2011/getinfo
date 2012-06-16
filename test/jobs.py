#!/usr/bin/env python
# -*- coding: utf-8 -*-
import popen2
import urllib2 
from BeautifulSoup import BeautifulSoup
import os
import requests
from lxml import html
from datetime import datetime, timedelta
# get news in last X days
DAY = 3
# url of the news page
BASE_URL = "http://job.xidian.edu.cn/"

#  get the page content
r = requests.get(BASE_URL)

# override the encoding
r.encoding = 'GBK'

doc = html.document_fromstring(r.content)
today = datetime.today()


def get_today_news():
    homedir = os.getcwd()
    os.system("/bin/echo "" > /srv/http/jobs/index.html") 
    fin,fout = popen2.popen2("tee -a /srv/http/jobs/index.html")
    fout.write("<html>")
    fout.write("<head>")
    fout.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=gb2312\">")
    fout.write("<link rel=\"Stylesheet\" type=\"text/css\" href=\"css/style.css\">")
    #fout.write("<script src=\"goto.js\"/>")
    #fout.write("<script src=\"script/jquery-1.7.1.min.js\"></script>")
    #fout.write("<script src=\"script/jquery.mobile-1.1.0.min.js\"></script>")
    #fout.write("<script>function GetContent(i){var content=$('#news_'+i).attr('rel');localStorage.content=content;}</script>")
    
    fout.write("</head>")
    fout.write("<body>")
    tds = doc.cssselect('table[width="723px"] td')
    newsnum = 0
    titlepre = ""
    for td in tds:
        content_tag = td.cssselect('span[class="titlePic"]')
        date_tag = td.cssselect('span[class="titleTime"]')
        if  date_tag and content_tag:
            td_date = date_tag[0].text_content().strip('[]')
            content_pre = content_tag
            td_timedelta = today - datetime.strptime('2012.'+td_date, "%Y.%m.%d")
            if td_timedelta < timedelta(DAY):
                link = td.cssselect('a')[0].get('href')
                title = td.cssselect('a')[0].get('title')
                if (title != titlepre):
                    titlepre=title
                    web=urllib2.urlopen(str(BASE_URL + link))
                    soup = BeautifulSoup(web)
                    #print web
                    content = soup.body.div.extract()
                    file=open('/srv/http/jobs/news_'+str(newsnum) + '.html','w+') 
                    head = BeautifulSoup(open(homedir +  "/cache/construction/head.html"))
                    bodyend = BeautifulSoup(open(homedir +  "/cache/construction/bodyend.html"))
                    print >> file,head
                    print >> file,content
                    file.close()  
                    fout.write("<div id=\"news_")                
                    fout.write(str(newsnum))                
                    fout.write("\">")                
                    fout.write("<a href=")                
                    fout.write("\"news_")
                    fout.write(str(newsnum))
                    fout.write(".html\">")                
                    fout.write(title.encode('gb2312'))
                    fout.write("</a>")
                    fout.write("<span>")
                    fout.write(str(datetime.strptime('2012.'+td_date, "%Y.%m.%d").strftime('%Y-%m-%d'))) 
                    fout.write("</span>")
                    fout.write("</div>")                
                    newsnum  = newsnum + 1
                 
    
                #fout.write("<a onclick=\"goto(str(BASE_URL + link))\"")
		#fout.write("<a href="ddd.html?#id_1">");
                #fout.write(str(BASE_URL + link))
                #fout.write("\">")
                





                #print title.encode('gb2312')
                #fout.write(title.decode('GBK').encode('gb2312'))
                #fout.write(title.encode('gb2312'))
                #fout.write("</a>")
                #fout.write("</h3></p>")
    fout.write("</body>")
    fout.write("</html>")
    fout.close()      
if __name__ == '__main__':
    get_today_news()
