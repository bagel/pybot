#!/usr/bin/env python
# coding: utf-8

import sys
import os
import talk
import re
import commands
import time
import xmpp
import urllib2
import urllib
import subprocess
import HTMLParser
import weather


def ssh(data):
    url = 'http://dpadmin.grid.sina.com.cn/cgi-bin/ssh.py?' + urllib.urlencode(data)
    return urllib2.urlopen(url=url).read()

def message_handle(conn, mess):
    #print mess
    user = mess.getFrom()
    print "resource:", user.getResource()
    if not user.getResource() or not mess.getBody():
        return 0
    name = user.getNode()
    text = str(mess.getBody())
    print "text: ", text
    msg = ''
    if re.match('#', text):
        host = text.strip('#').split(' ')[0]
        cmd = ' '.join(text.split(' ')[1:])
        msg = ssh({'ip': host, 'cmd': cmd})
    elif re.match('\$', text):
        user_home, script = text.strip('$').split(' ')
        msg = ssh({'user': user_home, 'script': script})
    elif re.match('restart', text):
        p = subprocess.Popen('python26 bot.py', shell=True)
        p.wait()
        sys.exit(0)
    else:
        p = subprocess.Popen(text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        msg = p.stdout.read()
    if msg:
        mesg = msg
        talk.Gtalk().send(conn, user, msg)

def presence_handle(conn, pres):
    user = pres.getFrom()
    conn.send(xmpp.Presence(to=user, typ='subscribe'))
    #talk.Gtalk().send(conn, user, "Hi, %s!" % user.getNode().title())

def restart():
    p = subprocess.Popen('python26 bot.py', shell=True)
    p.wait()
    sys.exit(0)

def bot():
    white_user = ["freetgm@gmail.com", "yjw1028@gmail.com", "blueswxs@gmail.com"]
    #white_user = ["freetgm@gmail.com", "caoyu1099@gmail.com"]
    conn = talk.Gtalk().connect()
    conn.RegisterHandler('message', message_handle)
    conn.RegisterHandler('presence', presence_handle)
    pres = xmpp.Presence(priority=5, show="chat", status="DPool Bot")
    conn.sendInitPresence()
    conn.send(pres)
    while True:
        conn.Process(1)
        time.sleep(0.1)
        t = time.localtime()
        #if t.tm_min % 30 == 0 and t.tm_sec == 0:
        #    restart()
        if t.tm_min == 18 and t.tm_sec == 0:
            [ talk.Gtalk().send(conn, user, weather.Weather().aqi()) for user in white_user ]
        if t.tm_min == 38 and t.tm_sec == 0:
            [ talk.Gtalk().send(conn, user, weather.Weather().forecast()) for user in white_user ]

def daemon():
    pid = os.fork()
    if pid > 0:
        print pid
        sys.exit(0)
    os.setsid()
    os.chdir("/data0/www/gtalk")
    os.umask(0)

if __name__ == "__main__":
    daemon()
    bot()
