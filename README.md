pybot
=====

python gtalk bot

##Getting Started
* **send message post interface** - configure wsgi with apache, add to apache httpd-vhost.conf

    WSGIScriptAlias /pybot /pathtopybot/application
    WSGIProcessGroup nobody
    WSGIDaemonProcess nobody user=nobody group=nobody processes=2 threads=25 python-path="/pathtopybot/:/usr/lib/python2.6/"
