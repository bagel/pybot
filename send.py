#!/usr/bin/env python

import sys
import os
import json
import talk

def Send(environ):
    ctype = 'text/plain; charset=utf-8'
    data = json.loads(environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])))
    msg = str(data['msg'])
    conn = talk.Gtalk().connect()
    conn.sendInitPresence()
    [ talk.Gtalk().send(conn, str(t), msg) for t in data['to'] ]
    response_body = ''
    return (ctype, response_body)


if __name__ == "__main__":
    Send('test')
