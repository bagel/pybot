pybot
=====

python gtalk bot

##Getting Started
* **send interface** - configure wsgi with apache, add to apache httpd-vhost.conf
'''apache
    WSGIScriptAlias /pybot /pathtopybot/application
    WSGIProcessGroup nobody
    WSGIDaemonProcess nobody user=nobody group=nobody processes=2 threads=25 python-path="/pathtopybot/:/usr/lib/python2.6/"
'''
