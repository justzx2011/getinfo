#!/usr/bin/env python
# -*- coding: utf-8 -*-
import popen2
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
    fin,fout = popen2.popen2("tee -a index.html")
    fout.write("<html>")
    fout.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=gb2312\">")
    tds = doc.cssselect('table[width="723px"] td')
    for td in tds:
        content_tag = td.cssselect('span[class="listTitle"]')
        date_tag = td.cssselect('span[class="titleTime"]')
        if  date_tag and content_tag:
            td_date = date_tag[0].text_content().strip('[]')
            td_timedelta = today - datetime.strptime('2012.'+td_date, "%Y.%m.%d")
            if td_timedelta < timedelta(DAY):
                link = td.cssselect('a')[0].get('href')
                title = td.cssselect('a')[0].get('title')
                #print datetime.strptime('2012.'+td_date, "%Y.%m.%d").strftime('%Y-%m-%d') , title, BASE_URL + link
                fout.write("<p>")                
                fout.write(str(datetime.strptime('2012.'+td_date, "%Y.%m.%d").strftime('%Y-%m-%d')))     
                fout.write("<a href=\"")
                fout.write(str(BASE_URL + link))
                fout.write("\">")
                #print title.encode('gb2312')
                #fout.write(title.decode('GBK').encode('gb2312'))
                fout.write(title.encode('gb2312'))
                fout.write("</a>")
                fout.write("</p>")
    fout.write("</html>")
    fout.close()      
if __name__ == '__main__':
    get_today_news()
