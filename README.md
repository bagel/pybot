pybot
=====

python gtalk bot

##Getting Started
* **send message api** - configure wsgi with apache, add to apache httpd-vhost.conf

        WSGIScriptAlias /pybot /pathtopybot/application

examples

        curl http://127.0.0.1/pybot/send -d '{"to": ["user@gmail.com"], "msg": "text"}' -v

