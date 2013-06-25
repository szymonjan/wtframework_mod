##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

import unittest
from wtframework.wtf.config import WTF_CONFIG_READER
from wtframework.wtf.email import IMapEmailAccountObject
from unittest.case import SkipTest


class TestImapEmail(unittest.TestCase):

    
    def setUp(self):
        self.expected_subject = WTF_CONFIG_READER.get("email.expected_subject")
        self.expected_message = WTF_CONFIG_READER.get("email.expected_message")
        
        email_config = WTF_CONFIG_READER.get("email")
        account_config = email_config['primary']

        email_server = account_config['server']
        username = account_config['username']
        password = account_config['password']

        email_type = account_config['type']
        if email_type == 'IMAP':
            self.mail = IMapEmailAccountObject(email_server, username, password)
        else:
            raise TypeError("Unsupported email type '{0}'".format(type)) 


    def tearDown(self):
        pass

    @SkipTest #This test requires an imap email account
    def test_search_by_subject(self):


        print "Searching for email by subject", self.expected_subject
        message_num = self.mail.find_emails_by_subject(self.expected_subject)[0]
        message = self.mail.get_email_message(message_num)
        print message_num, message
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()