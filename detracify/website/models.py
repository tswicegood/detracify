from datetime import datetime
from django.db import models

from django.utils import simplejson as json


class PullReq(models.Model):
    """
    Represents a pull request from git that will/may need to be pushed into
    Trac as a ticket, or patch on a ticket.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # json data from the pull req api on github
    gh_json = models.TextField(max_length=2048)

    # 'number' from github
    gh_id = models.IntegerField()

    # id from trac
    trac_id = models.IntegerField(null=True)

    @property
    def gh_dict(self):
        if self.gh_json:
            try:
                return json.loads(self.gh_json)
            except Exception:
                return {}
