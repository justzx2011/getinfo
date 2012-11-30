#!/usr/bin/env python
# -*- coding: utf-8 -*-
import popen2
import time
import sys
import os
import requests
from lxml import html

USERNAME = ""
PASSOWORD = ""

BASE_URL = "http://pay.xidian.edu.cn"

FORM_URL = "/servlet/login"
PAY_INFO_URL = "/swyh/dyll.jsp"

TMP_DIR = os.path.expanduser("~/.xidian/")
IMG_PATH = os.path.join(TMP_DIR, "img.jpg")
TEXT_PATH = os.path.join(TMP_DIR, "result.txt")


def make_data_and_cookies():
    """make the post data(including vcode) and get cookies"""

    vcode = ''
    while len(vcode) is not 4:
        r = requests.get(BASE_URL)
        doc = html.document_fromstring(r.content)
        vcode_link = doc.cssselect('form img')[0].get('src')
        vcv = doc.cssselect('input[name="vcv"]')[0].get('value')
        img_url = BASE_URL + vcode_link
        img = requests.get(img_url)

        # write to the image file
        with open(IMG_PATH, 'w') as f:
            f.write(img.content)

        # using tesseract to get the vcode img value
        os.popen('tesseract %s %s' % (IMG_PATH, TEXT_PATH[:-4]))
        with open(TEXT_PATH) as f:
            vcode = f.read().strip('\n')

    data = {
            "account": USERNAME,
            "password": PASSOWORD,
            "vcode": vcode,
            "vcv": vcv
            }
    return data, r.cookies


def submit_form(data, cookies):
    """submit the login form so you're logined in"""
    form_action_url = BASE_URL + FORM_URL
    requests.post(form_action_url, data=data, cookies=cookies)


def get_info(cookies):
    """retrieve the data using the cookies"""
    info_url = BASE_URL + PAY_INFO_URL
    r = requests.get(info_url, cookies=cookies)
    doc = html.document_fromstring(r.content)
    used, rest = doc.cssselect('tr')
    used_gb = float(used.findall('td')[1].text) / 1024
    rest_gb = float(rest.findall('td')[1].text) / 1024
    return used_gb, rest_gb

if __name__ == '__main__':
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
    while True:
        data, cookies = make_data_and_cookies()
        submit_form(data, cookies)
        time.sleep(1)
        try:
            result = get_info(cookies)
            break
        except:
            time.sleep(1)
    #oldStdout = sys.stdout
    #sys.stdout = open("script.log", "w+")
    #print time.ctime()
    #print "%.2fGB" % (result[0])
    #print "%.2fGB" % (result[1])
    os.system("/bin/echo "" > pay.html")
    fin,fout = popen2.popen2("tee -a pay.html")
    fout.write("<html>")
    fout.write("<head>")
    fout.write("<link rel=\"Stylesheet\" type=\"text/css\" href=\"style.css\">") 
    fout.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">")
    fout.write("</head>")
    fout.write("<h3>")
    fout.write(time.ctime())	 
    fout.write("</h3>")
    #fout.write("\n")
    #fout.write("<h3>")
    fout.write("<h3>此月已使用流量  ")
    fout.write("%.2fGB" % (result[0]))
    fout.write("</h3>")
    fout.write("<h3>此月剩余流量  ")
    fout.write("%.2fGB" % (result[1]))
    fout.write("</h3>")
    fout.write("</html>")
    #print "此月已使用流量 %.2fGB, 剩余 %.2f GB" % (result)
    #sys.stdout = oldStdout
