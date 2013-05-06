pybot
=====

python gtalk bot

##Getting Started
* **send message api**

test

        python application

example

        curl http://127.0.0.1:8080/send -d '{"to": ["user@gmail.com"], "msg": "text"}'

configure wsgi with apache, add to apache httpd-vhost.conf

        WSGIScriptAlias /pybot /pathtopybot/application


* **bot**

run

        python bot.py

examples

1. run commands on server

        #ip cmd opts

2. run scripts on admin

        $user script

3. get weather and pm2.5

        weather

4. default run commands on vm where bot run
