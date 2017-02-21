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
import webapp2
import re

form = """
<h1>User Signup</h1>
         <form method='post'>
               <label>Username:
               <input type='text' name='username' value=''>
               <span style='color: red'>%(username_error)s</span>
               </label>
<br></br>
               <label>Password:
               <input type='password' name='password' value=''>
               <span style='color: red'>%(password_error)s</span>
               </label>
<br></br>
              <label>Verify:
              <input type='text' name='verify' value=''>
              <span style='color: red'>%(verify_error)s</span>
              </label>
<br></br>
              <label>Email:
              <input type='text' name='email' value=''>
              <span style='color: red'>%(email_error)s</span>
              </label>
<br></br>
               <input type='submit'>
        </form>"""
#username_error=""
#password_error=""
#verify_error=""
#email_error=""
#values = {'username':'username_error': username_error, 'password_error': password_error, 'verify_error': verify_error, 'email_error': email_error}
#parameters = dict{"username": username, "passcode": passcode, 'verify': verify, 'email': email, 'username_error': username error, 'passcode_error': passcode_error, 'verify_error': verify_error, 'email_error': email_error}

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username='', email='',username_error='', password_error='', verify_error='', email_error=''):
        values = {'username': username, 'email': email, 'username_error': username_error, 'password_error': password_error, 'verify_error': verify_error, 'email_error': email_error}
        self.response.out.write(form % values)
        #{"username_error": username_error, "password_error": password_error, "verify_error": verify_error, "email_error": email_error}

    def get(self):
        self.write_form()

    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if USER_RE.match(username):
            return True
        else:
            return False
    def valid_password(self, password):
        PASS_RE = re.compile(r"^.{3,20}$")
        if PASS_RE.match(password):
            return True
        else:
            return False
    def valid_verify(self, verify, password):
        if password != verify:
            return False
        else:
            return True
    def valid_email(self, email):
        if email = '':
            return True
        EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        if EMAIL_RE.match(email):
            return True
        else:
            return False
    def post(self):
        username = self.request.get("username")
        user = self.valid_username(username)
        password = self.valid_password(self.request.get('password'))
        verify = self.valid_verify(self.request.get('verify'), self.request.get('password'))
        email = self.valid_email(self.request.get('email'))
        username_error=''
        password_error=''
        verify_error=''
        email_error=''

        if (user and password and verify and email):
            return self.response.out.write("<h1>Welcome,&nbsp&nbsp" + username + "</h1>")
        if not (user):
            username_error="That's not a valid username"
        if not (password):
            password_error='That is not a valid password'
        if not (verify):
            verify_error='Those passwords do not match'
        if not (email):
            email_error='That is not a valid email address'
        self.write_form(username, email, username_error, password_error, verify_error, email_error)


            #self.response.out.write("<h1>Welcome,&nbsp&nbsp" + username + "</h1>")


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
