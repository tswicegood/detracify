from datetime import datetime
from django.db import models

import simplejson as json

class PullReq(models.Model):
    """
    Represents a pull request from git that will/may need to be pushed into Trac as a ticket,
    or patch on a ticket.

    {
      "state": "open",
      "base": {
        "label": "technoweenie:master",
        "ref": "master",
        "sha": "53397635da83a2f4b5e862b5e59cc66f6c39f9c6",
        "user": {...},
        "repository": {...}
      },
      "head": {
        "label": "smparkes:synchrony",
        "ref": "synchrony",
        "sha": "83306eef49667549efebb880096cb539bd436560",
        "user": {...},
        "repository": {...}
      },
      "discussion": [
        {
          "type": "IssueComment",
          "gravatar_id": "821395fe70906c8290df7f18ac4ac6cf",
          "created_at": "2010/10/07 07:38:35 -0700",
          "body": "Did you intend to remove net/http?  Otherwise, this looks good.  Have you tried running the LIVE tests with it?\r\n\r\n    ruby test/live_server.rb # start the demo server\r\n    LIVE=1 rake",
          "updated_at": "2010/10/07 07:38:35 -0700",
          "id": 453980,
          "user": {...}
        },
        {
          "type": "Commit",
          "committed_date": "2010-11-04T16:27:45-07:00",
          "authored_date": "2010-11-04T16:27:45-07:00",
          "id": "83306eef49667549efebb880096cb539bd436560",
          "author": {
            "name": "Steven Parkes",
            "email": "smparkes@smparkes.net",
            "login": "smparks" // filled if user is on GitHub
          },
          "committer": { ... }, // same as author
          "message": "add em_synchrony support",
          "user": {...}, // GitHub user info with gravatar_id
          "tree": "101492b4af83d1298225e573bbe7478952ba9f0a",
          "parents": [{"id": "0a0b888d8eabded106a30e8a9cddc47e6cacbf37"}]
        },
        {
          "type": "PullRequestReviewComment",
          "diff_hunk": "@@ -1,12 +1,12 @@\n Aquaman is a comic book superhero who appears in DC Comics....",
          "body": "some comment about the change",
          "path": "aquaman.txt",
          "position": 19,
          "commit_id": "54bb654c9e6025347f57900a4a5c2313a96b8035",
          "original_commit_id": "54bb654c9e6025347f57900a4a5c2313a96b8035",
          "user": {...},
          "created_at": "2011-02-07T14:39:03-05:00",
          "updated_at": "2011-02-07T14:39:03-05:00"
        }
      ],
      "issue_user": {...},
      "user": {...},
      "title": "Synchrony",
      "body": "Here's the pull request.\r\n\r\nThis isn't generic EM: require's Ilya's synchrony and needs to be run on its own fiber, e.g., via synchrony or rack-fiberpool.\r\n\r\nI thought about a \"first class\" em adapter, but I think the faraday api is sync right now, right? Interesting idea to add something like rack's async support to faraday, but that's an itch I don't have right now.",
      "position": 4.0,
      "number": 15,
      "votes": 0,
      "comments": 4,
      "diff_url": "https://github.com/technoweenie/faraday/pull/15.diff",
      "patch_url": "https://github.com/technoweenie/faraday/pull/15.patch",
      "labels": [],
      "html_url": "https://github.com/technoweenie/faraday/pull/15",
      "issue_created_at": "2010-10-04T12:39:18-07:00",
      "issue_updated_at": "2010-11-04T16:35:04-07:00",
      "created_at": "2010-10-04T12:39:18-07:00",
      "updated_at": "2010-11-04T16:30:14-07:00"
    }

    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    gh_json = models.TextField(max_length=2048) # json data from the pull req api on github

    gh_id = models.IntegerField() # 'number' from github

    trac_id = models.IntegerField(null=True) # id from trac

    @property
    def gh_dict(self):
        if self.gh_json:
            try:
                return json.loads(self.gh_json)
            except Exception, e:
                return {}

    