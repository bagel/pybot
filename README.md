pybot
=====

python gtalk bot

##Getting Started
* **send message api**

test

        python application

example

        curl http://127.0.0.1:8080/pybot/send -d '{"to": ["user@gmail.com"], "msg": "text"}'

configure wsgi with apache, add to apache httpd-vhost.conf

        WSGIScriptAlias /pybot /pathtopybot/application

