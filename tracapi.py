#!/usr/bin/python -u

import xmlrpclib
import datetime

class TicketAPI (object):
    def __init__ (self, username, passwd):
        self.server_url = 'https://%s:%s@code.djangoproject.com/login/rpc'  % (username, passwd)
        self.server_proxy = xmlrpclib.ServerProxy(self.server_url)
        
    def changelog_test (self, ticket_id):
        """Return change log for past 24 hours"""
        
        dt = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        return self.get_changelog(ticket_id, dt)
        
    def get_changelog (self, ticket_id, ts=None):
        """Returns a list of changes, if time stamp is given, will return only
        changes equal to or after date time.  Pretty sure date time should be UTC 
        but don't quote me on that.  @pizzapanther
        """
        
        changelog = self.server_proxy.ticket.changeLog(ticket_id)
        
        if ts:
            ret = []
            for change in changelog:
                if change[0] >= ts:
                   ret.append(change)
                   
            return ret
            
        return changelog
        