#!/usr/bin/env python
# coding: utf-8

import sys
import os
import xmpp


class Gtalk:
    def __init__(self, account='xxxxxxxx@gmail.com', password='xxxxxxxx'):
        self.account = account
        self.password = password
        self.host = 'talk.google.com'
        self.port = 5223

    def connect(self):
        jid = xmpp.JID(self.account)
        user = jid.getNode()
        server = jid.getDomain()
        print user,server
        conn = xmpp.Client(server, debug=[])
        if not conn.connect():
            print "Unable to connect to %s" % server
            sys.exit(1)
        if not conn.auth(user, self.password):
            print "Unable to authorize on %s, Please check account or password" % server
        return conn

    def send(self, conn, sendto, msg):
        conn.send(xmpp.Message(sendto, msg))

if __name__ == "__main__":
    print Gtalk().connect()
