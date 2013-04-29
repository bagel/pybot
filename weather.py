#!/usr/bin/env python
# coding: utf-8

import sys
import os
import HTMLParser


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
    
