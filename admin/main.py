#!/usr/bin/env python
#!-*- coding:utf-8 -*-
# CRUDサンプル
# http://www.jinlingren.com/

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

from mylibs import *

class Root(webapp.RequestHandler):
    def get(self):
        self.redirect('/admin/list')

class List(webapp.RequestHandler):
    def get(self):
        mails = Mail.all().order('email')
        html = template.render(
            os.path.join(os.path.dirname(__file__), 'view', 'list.html'),
            {
                'mails': mails
            }
        )
        self.response.out.write(html)

class View(webapp.RequestHandler):
    def get(self, key):
        mail = Mail.get(key)
        mail.comment = mail.comment.replace("\n","<br>\n")
        html = template.render(
            os.path.join(os.path.dirname(__file__), 'view', 'view.html'),
            {
                'mail': mail
            }
        )
        self.response.out.write(html)

class Add(webapp.RequestHandler):
    def get(self):
        forms = {}
        html = template.render(
            os.path.join(os.path.dirname(__file__), 'view', 'add.html'),
            {
                'forms': forms
            }
        )
        self.response.out.write(html)

    def post(self):
        try:
            email = cgi.escape(self.request.get('email'))
            if self.request.get('status') == 'True':
                status = True
            else:
                status = False
            mail = Mail(email=email, status=status)
            mail.comment = db.Text(cgi.escape(self.request.get('comment')))
            mail.put()
            self.redirect('/admin/list')
        except:
            self.redirect('/admin/add')


class Edit(webapp.RequestHandler):
    def get(self, key):
        forms = {}
        mail = Mail.get(key)
        html = template.render(
            os.path.join(os.path.dirname(__file__), 'view', 'edit.html'),
            {
                'forms': forms,
                'mail': mail
            }
        )
        self.response.out.write(html)

    def post(self, key):
        try:
            mail = Mail.get(key)
            mail.email = cgi.escape(self.request.get('email'))
            if self.request.get('status') == 'True':
                mail.status = True
            else:
                mail.status = False
            mail.comment = db.Text(cgi.escape(self.request.get('comment')))
            mail.put()
            self.redirect('/admin/list')
        except:
            self.redirect('/admin/edit/'+key)

class Delete(webapp.RequestHandler):
    def get(self, key):
        try:
            mail = Mail.get(key)
            if mail:
                mail.delete()
                self.redirect('/admin/list')
        except:
            self.redirect('/admin/list')

class Send(webapp.RequestHandler):
    def get(self):
        mail = SendMail('TEST PASSWORD', u'テスト')
        mail.send()
        self.redirect('/admin/list')

def main():
    application = webapp.WSGIApplication(
            [
            ('/admin', Root),
            ('/admin/list', List),
            ('/admin/view/(\w+)', View),
            ('/admin/add', Add),
            ('/admin/edit/(\w+)', Edit),
            ('/admin/delete/(\w+)', Delete),
            ('/admin/send', Send)
            ],
            debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

