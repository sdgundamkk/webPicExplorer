#!/usr/bin/python
# -*- coding:UTF-8 -*-

from flask import Flask
from flask_mail import Mail,Message
from threading import Thread
import re

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.qiye.163.com',
    MAIL_PROT = 994,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = '',
    MAIL_PASSWORD = '',
    MAIL_DEBUG = True
)

mail = Mail(app)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def checkAddress(address):
    result = []
    if not isinstance(address,list):
        return False
    for a in address:
        if re.match(r'^[0-9a-zA-Z\.]{0,19}@[0-9a-zA-Z]{1,13}\.com$',a):
            result.append(result)
    return result


def sendMail(recipients, ccUser, title, body):
    msg = Message()
    if not checkAddress(recipients) or not checkAddress(ccUser):
        raise 'error'
    msg.recipients = recipients
    msg.cc = ccUser
    msg.subject = title
    msg.body = body
    thread = Thread(target=send_async_email,args=[app,msg])
    thread.start()

