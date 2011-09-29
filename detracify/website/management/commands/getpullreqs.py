from datetime import datetime
from optparse import make_option
from django.core.management.base import NoArgsCommand, BaseCommand, CommandError

from website.githubapi import GithubAPI
#from website.tracapi import TracAPI

from website.models import PullReq
from django.utils import simplejson as json

import logging
log = logging.getLogger('detracify.getpullreqs')

class Command(NoArgsCommand):
    help = (u"Get pull requests for the Django Project from Github")

    def handle_noargs(self, **options):
        gh = GithubAPI()
        pulls = gh.get_open_pull_requests()
        
        for pull in pulls:
            pull.update(pull['user'])
            log.info("""
    Pull %s:
            number: %(number)d
            html_url: %(html_url)s
            patch_url: %(patch_url)s
            user: %(name)s <%(email)s>
            %(body)s
    """ % pull)
            preq, created = PullReq.objects.get_or_create(gh_id=pull['number'])
            if created:
                preq.gh_json = json.dumps(pull)
                preq.save()
            else: # existed before, check for new stuff
                # 2011-09-09T18:35:43Z

                # generate a new patch in trac with the number of total commits in the name:
                # some_identifier_<totalcommits>.diff
                
                updated_at = datetime.strptime(pull['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

                num_commits = len([item for item in pull['discussion'] if item['type']=='commit'])
                num_prev_commits = len([item for item in preq.gh_dict['discussion'] if item['type']=='commit'])

                # if the gh PR is newer, and
                # the number of COMMITS in "discussions" is greater
                if updated_at > preq.updated \
                        and num_commits > num_prev_commits:
                    pass