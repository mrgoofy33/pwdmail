#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
import os
import cgi
import datetime
import logging

from google.appengine.api import mail
from google.appengine.api import users
import string
import datetime
import locale

class Mail(db.Model):
    email = db.StringProperty(required=True)
    status = db.BooleanProperty(default=False)
    comment = db.TextProperty()
    modified = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now_add=True)


class SendMail(object):

    def __init__(self, pwd, sub='', from_ad='hogehoge@exsample.com'):
        self.password = pwd
        self.add_sub = sub
        self.from_addr = from_ad

    def send(self):
        date = datetime.datetime.today() + datetime.timedelta(hours=9)
        password = self.password
        to_addr = []
        mails = Mail.all().filter('status =', True).order('email')
        for mailmodel in mails:
            to_addr.append(mailmodel.email)
        sub = "%s【Password】%s/%02d" % ( self.add_sub, date.year, date.month )
        message = mail.EmailMessage(sender=self.from_addr,
                                    subject=sub)
        message.to = ';'.join(to_addr)
        message.body = u"""
TO:メンバー各位

%s年%s月のパスワードです。

%s

以上です。
        """ % (date.year, date.month, password)
        message.send()

