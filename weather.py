#!/usr/bin/env python
# coding: utf-8

import sys
import os
import HTMLParser
import urllib2
import json
import time
import re


class Htmlparser(HTMLParser.HTMLParser):
    def __init__(self, th=[], td=[]):
        HTMLParser.HTMLParser.__init__(self)
        self.th = th
        self.td = td
        self.i = 0
        self.t = 0
        self.br = 0
        self.pos = 0
        self.data = ''
        
    def handle_starttag(self, tag, attrs):
        if tag == 'th':
            self.t = 1
        if tag == 'br':
            self.br = 1

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.t == 1:
            self.th.append(data)  #监测项
            self.t = 0
        if self.br == 1:
            self.th[-1] = self.th[-1] + " " + data
            self.br = 0
        if self.pos == 1:
            self.td.append(data)  #监测值
            self.i += 1
        if self.i == 9:
            self.pos = 0
        if data == '海淀区万柳':  #监测点
            self.td.append(data)
            self.pos = 1
        if re.search('数据更新时间', data):
            self.th.append(data.split('：')[0])
            self.td.append(data.split('：')[1])

class Weather:
    def aqi(self):
        text = ''.join([ line.strip() for line in urllib2.urlopen(url='http://www.pm25.in/beijing', timeout=5).readlines() if re.search('<th.*>|<td.*>|<p>', line) ])
        #print text
        #text = "<html><body><td>text</td></body></html>"
        th = []
        td = []
        parser = Htmlparser(th=th, td=td)
        parser.feed(text)
        return '\n'.join([ "%s:  %s" % (h, td[th.index(h)]) for h in th ])

    def forecast(self):
        data = json.loads(urllib2.urlopen(url='http://platform.sina.com.cn/weather/forecast?app_key=2872801998&city=%E5%8C%97%E4%BA%AC&lenday=2', timeout=5).read())['data']['city'][0]
        city = data['info']['name']
        wday = {
            0: u"\u661f\u671f\u4e00", 
            1: u"\u661f\u671f\u4e8c", 
            2: u"\u661f\u671f\u4e09", 
            3: u"\u661f\u671f\u56db", 
            4: u"\u661f\u671f\u4e94", 
            5: u"\u661f\u671f\u4e6d", 
            6: u"\u661f\u671f\u65e5"
        }
        w = []
        for day in data['days']['day']:
            t = []
            print day
            if day['s1'] == day['s2']:
            #if False:
                t.append(day['s1'])
            else:
                t.append("%s%s%s" % (day['s1'], unicode('转', 'utf-8'), day['s2']))
            t.append("%s ~%s " % (day['t1'], day['t2']))
            t.append("%s %s" % (day['d1'], day['p1']))
            w.append(t)
        return city + " " + time.strftime("%Y-%m-%d") + " " + wday[time.localtime().tm_wday] +  unicode("\n今日 ", "utf-8") + ' '.join(w[0]) + unicode("\n明日 ", "utf-8") + ' '.join(w[1]) + "\n"


if __name__ == "__main__":
    print Weather().aqi()
    print Weather().forecast()
