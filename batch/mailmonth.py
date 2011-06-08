# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required

import string
import random
import datetime
import locale

from mylibs import *

alphabets = '%$+_-<>&#;:[]}{' + string.digits + string.letters

def getRandomString(n, sets = alphabets):
    random.seed()
    return ''.join(random.choice(sets) for i in xrange(n))

class MainHandler(webapp.RequestHandler):
    def get(self):
        date = datetime.datetime.today() + datetime.timedelta(hours=9)
        if date.day == 1:
            password = getRandomString(12)
            #mail = SendMail(password)
            mail = SendMail(password)
            mail.send()

def main():
    application = webapp.WSGIApplication([('/batch/mailmonth', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
