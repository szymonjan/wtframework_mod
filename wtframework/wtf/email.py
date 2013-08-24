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

#This is required to avoid the namespace conflict of this 'email' module with the 'email' lib.
from __future__ import absolute_import
from email.parser import HeaderParser
import email
import imaplib
import re

class IMapEmailAccountObject(object):
    """
    IMapEmailAccountObject is a class to assist in connecting to Imap email 
    accounts for test verification.  It provides methods for searching through 
    the inbox and retrieving content for verification.
    
    Usage Example::

        #Instantiate a Email Account Obj.
        email = IMapEmailAccountObject("mail.gmail.com", "yourlogin", "yourpassword")
        #Verify received email with subject.
        self.assertTrue( email.check_email_exists_by_subject("Your Subject Line")
        # Get the UIDs of a messages that contain subject.
        uid - email.find_emails_by_subject("My Subject Line")
        #Fetch the contents of the email as a string.
        message_contents = email.get_email_message(uid[0])

    """

    def __init__(self, server_address, username, password):
        """
        Constructor
        
        Args:
            server_address (str): Email Server address.
            username (str): Username
            password (str): Password

        """
        print "connecting to {0}, using {1},{2}".format(server_address, username, password)
        self._mail = imaplib.IMAP4_SSL(server_address)
        self._mail.login(username, password)
        print "connected."


    def check_email_exists_by_subject(self, subject):
        """
        Searches for Email by Subject.  Returns True or False.
        
        Args:
            subject (str): Subject to search for.
        
        Returns: 
            True - email found, False - email not found

        """
        # Select inbox to fetch the latest mail on server.
        self._mail.select("inbox")
        
        try:
            matches = self.__search_email_by_subject(subject)
            if len(matches) <= 0:
                return False
            else:
                return True
        except Exception as e:
            raise e

    def find_emails_by_subject(self, subject, limit=50):
        """
        Searches for Email by Subject.  Returns email's imap message IDs 
        as a list if matching subjects is found.

        Args:
            subject (str) - Subject to search for.

        Kwargs:
            limit (int) - Limit search to X number of matches, default 50

        Returns:
            list - List of Integers representing imap message UIDs.

        """
        # Select inbox to fetch the latest mail on server.
        self._mail.select("inbox")
        
        matches = []
        parser = HeaderParser()
        
        matching_msg_nums = self.__search_email_by_subject(subject)

        for msg_num in matching_msg_nums[-limit:]:
            _, msg_data = self._mail.fetch(msg_num, '(RFC822)')
            raw_msg = msg_data[0][1]
            msg_headers = parser.parsestr(raw_msg, True)
            if msg_headers['subject'] == subject:
                uid = re.search("UID\\D*(\\d+)\\D*", self._mail.fetch(msg_num, 'UID')[1][0]).group(1)
                matches.append(uid)

        return matches



    def get_email_message(self, message_uid, message_type="text/plain"):
        """
        Fetch contents of email.

        Args:
            message_uid (int): IMAP Message UID number.
        
        Kwargs:
            message_type: Can be 'text' or 'html'

        """
        self._mail.select("inbox")
        result = self._mail.uid('fetch', message_uid, "(RFC822)")
        msg = email.message_from_string(result[1][0][1])

        try:
            #Try to handle as multipart message first.
            for part in msg.walk():
                if part.get_content_type() == message_type :
                    return part.get_payload()
        except:
            #handle as plain text email
            return msg.get_payload()



    def raw_search(self, *args, **kwargs):
        """
        Find the a set of emails matching each regular expression passed in against the (RFC822) content.
        
        Args:
            *args: list of regular expressions.
        
        Kwargs:
            limit (int) - Limit to how many of the most resent emails to search through.
            date (datetime) - If specified, it will filter avoid checking messages older 
                              than this date.

        """
        limit = 50
        try:
            limit = kwargs['limit'] 
        except KeyError:
            pass
        
        # Get first X messages.
        self._mail.select("inbox")

        #apply date filter.
        try:
            date = kwargs['date']
            date_str = date.strftime("%d-%b-%Y")
            _, email_ids = self._mail.search(None, '(SINCE "%s")' % date_str)
        except KeyError:
            _, email_ids = self._mail.search(None, 'ALL')
        
        email_ids = email_ids[0].split() #Above call returns email IDs as an array containing 1 str
        
        matching_uids = []
        for _ in range(1, min(limit, len(email_ids))):
            email_id = email_ids.pop()
            rfc_body = self._mail.fetch(email_id, "(RFC822)")[1][0][1]
            
            match = True
            for expr in args:
                if re.search(expr, rfc_body) is None:
                    match = False
                    break

            if match:
                uid = re.search("UID\\D*(\\d+)\\D*", self._mail.fetch(email_id, 'UID')[1][0]).group(1)
                matching_uids.append(uid)

        return matching_uids



    def __search_email_by_subject(self, subject):
        "Get a list of message numbers"
        _, data = self._mail.search(None, 'SUBJECT', subject)
        return data[0].split()

    def __del__(self):
        "Destructor - disconnect from imap when we're done."
        try:
            # Disconnect email.
            self._mail.logout()
        except Exception as e:
            print e
        self._mail = None

