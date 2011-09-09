from optparse import make_option
from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from website import github
from website.models import PullReq
import simplejson as json

import logging
log = logging.getLogger('detracify.getpullreqs')

class Command(NoArgsCommand):
    help = (u"Get pull requests for the Django Project from Github")

    def handle_noargs(self, **options):
        pulls = github.get_open_pull_requests()
        for pull in pulls:
            log.debug(repr(pull)+"\n\n")
            preq, created = PullReq.objects.get_or_create(gh_id=pull['number'])
            if created:
                preq.gh_json = json.dumps(pull)
                preq.save()