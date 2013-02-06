'''
Created on Dec 31, 2012

@author: "David Lai"
'''

import email
import imaplib

class IMapEmailAccountObject(object):

    _mail = None

    def __init__(self, server_address, username, password):
        """
        Constructor
        @param server_address: Email Server address.
        @type server_address: str
        @param username: Username
        @type username: str
        @param password: Password
        @type password: str
        """
        print "connecting to {0}, using {1},{2}".format(server_address, username, password)
        self._mail = imaplib.IMAP4_SSL(server_address)
        self._mail.login(username, password)
        print "connected."


    def check_email_exists_by_subject(self, subject):
        """
        Searches for Email by Subject.  Returns True or False.
        
        @param subject: Subject to search for.
        @type subject: str
        @return: True if found, false if not found.
        @rtype: Boolean
        """
        # Select inbox to fetch the latest mail on server.
        self._mail.select("inbox")
        
        query_str = "(ALL SUBJECT '{0}')".format(subject)
        resp,items = self._mail.search(None, query_str)
        if not resp == 'OK':
            raise RuntimeError("Error occurred while searching. Response Code:" + resp)
        else:
            pass

        # Check if there are any results
        results = items[0].split() #items[0] is an space separated list of email IDs.
        if len(results) > 0:
            return True
        else:
            return False

    def find_emails_by_subject(self, subject):
        """
        Searches for Email by Subject.  Returns email's imap message IDs 
        as a list if matching subjects is found.
        
        @param subject: Subject to search for.
        @type subject: str
        @return: List of Integers representing imap message UIDs.
        @rtype: list
        """
        # Select inbox to fetch the latest mail on server.
        self._mail.select("inbox")
        
        query_str = "(ALL SUBJECT '{0}')".format(subject)
        resp,items = self._mail.uid('search', None, query_str)
        if not resp == 'OK':
            raise RuntimeError("Error occurred while searching. Response Code:" + resp)
        else:
            pass

        return items[0].split() #items[0] is an space separated list of email IDs.

    def get_email_message(self, message_uid, message_type="text/plain"):
        """
        Fetch contents of email.
        @param message_uid: IMAP Message UID number.
        @type message_uid: int 
        @param message_type: Can be 'text' or 'html'
        @type message_type: str  
        """
        self._mail.select("inbox")
        result = self._mail.uid('fetch', message_uid, "(RFC822)")
        msg = email.message_from_string(result[1][0][1])

        try:
            #Try to handle as multiplart message first.
            for part in msg.walk():
                if part.get_content_type() == message_type :
                    return part.get_payload()
        except:
            #handle as plain text email
            return msg.get_payload()

    def __del__(self):
        "Destructor - disconnect from imap when we're done."
        try:
            # Disconnect email.
            self._mail.logout()
        except Exception as e:
            print e
        self._mail = None
