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
import json
import subprocess
import HTMLParser
import weather



#white_user = ["freetgm@gmail.com", "yjw1028@gmail.com", "blueswxs@gmail.com"]
#white_user = ["freetgm@gmail.com", "caoyu1099@gmail.com"]
white_user = json.load(open("user.json"))


def ssh(data):
    url = 'http://dpadmin.grid.sina.com.cn/cgi-bin/ssh.py?' + urllib.urlencode(data)
    return urllib2.urlopen(url=url).read()

def message_handle(conn, mess):
    #print mess
    user = mess.getFrom()
    print user
    #print "resource:", type(user.getResource())
    print mess.getBody()
    if not user.getResource() or not mess.getBody() or user.getStripped() not in white_user:
        return 0
    name = user.getNode()
    #print name
    text = str(mess.getBody().encode("utf-8"))
    #print "text: ", text
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
    elif re.match('[wW]eather', text):
        msg = '\n'.join(wth())
    elif re.match("user", text):
        msg = '\n'.join(white_user)
    elif re.match("add", text):
        white_user.append(text.strip("add").strip())
        fa = open("user.json", "w")
        fa.write(json.JSONEncoder().encode(white_user))
        fa.close()
    elif re.match("remove", text):
        white_user.remove(text.strip("remove").strip())
        fr = open("user.json", "w")
        fr.write(json.JSONEncoder().encode(white_user))
        fr.close()
    else:
        #p = subprocess.Popen(text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #p.wait()
        #msg = p.stdout.read()
        msg = text
    if msg:
        mesg = msg
        if msg == text:
            msg = "%s: " % name.encode("utf-8") + msg
            for u in white_user:
                if u.split("@")[0] == name:
                    continue
                talk.Gtalk().send(conn, u, msg)
        else:
            talk.Gtalk().send(conn, user, msg)
    else:
        talk.Gtalk().send(conn, user, "")

def presence_handle(conn, pres):
    user = pres.getFrom()
    conn.send(xmpp.Presence(to=user, typ='subscribe'))
    #talk.Gtalk().send(conn, user, "Hi, %s!" % user.getNode().title())

def restart():
    p = subprocess.Popen('python26 bot.py', shell=True)
    p.wait()
    sys.exit(0)

def bot():
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
        if t.tm_min % 5 == 0 and t.tm_sec == 0:
            restart()
        if t.tm_hour % 3 == 0 and t.tm_min == 18 and t.tm_sec == 0:
            w = '\n'.join(wth())
            [ talk.Gtalk().send(conn, user, w) for user in white_user ]

def wth():
    w = aqi = ''
    try:
        w = weather.Weather().forecast().encode('utf-8')
        aqi = weather.Weather().aqi()
    except:
        pass
    return (w, aqi)
    

def daemon():
    pid = os.fork()
    if pid > 0:
        print pid
        sys.exit(0)
    os.setsid()
    os.chdir("/data0/www/pybot")
    os.umask(0)

if __name__ == "__main__":
    daemon()
    bot()
