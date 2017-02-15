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
               <input type='text' name='password' value=''>
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
username_error=""
password_error=""
verify_error=""
email_error=""
errors = {'username_error': username_error, 'password_error': password_error, 'verify_error': verify_error, 'email_error': email_error}
#parameters = dict{"username": username, "passcode": passcode, 'verify': verify, 'email': email, 'username_error': username error, 'passcode_error': passcode_error, 'verify_error': verify_error, 'email_error': email_error}

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username_error="", password_error="", verify_error="", email_error=""):
        self.response.out.write(form % errors)
        #{"username_error": username_error, "password_error": password_error, "verify_error": verify_error, "email_error": email_error}

    def get(self):
        self.write_form()

    def post(self):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        def valid_username(username):
            if USER_RE.match(username):
                return True
            else:
                return False
        PASS_RE = re.compile(r"^.{3,20}$")
        def valid_password(password):
            if PASS_RE.match(password):
                return True
            else:
                return False
        def valid_verify(verify, password):
            if password != verify:
                return False
            else:
                return True
        EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        def valid_email(email):
            if EMAIL_RE.match(email):
                return True
            else:
                return False
        username = self.request.get("username")
        user = valid_username(self.request.get('username'))
        password = valid_password(self.request.get('password'))
        verify = valid_verify(self.request.get('verify'), self.request.get('password'))
        email = valid_email(self.request.get('email'))
        have_error = False
        if not (user):
            errors['username_error']="That's not a valid username"
            have_error = True
        elif not (password):
            errors['password_error']='That is not a valid password'
            have_error = True
        elif not (verify):
            errors['verify_error']='Those passwords do not match'
            have_error = True
        elif not (email):
            errors['email_error']='That is not a valid email address'
            have_error = True
        elif (have_error):
            self.write_form(errors)
        else:
            self.response.out.write("<h1>Welcome,&nbsp&nbsp" + username + "</h1>")
    
                                
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
