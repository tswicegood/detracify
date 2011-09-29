import requests
from django.utils import simplejson as json
from django.conf import settings


DEFAULT_API_BASE = 'http://github.com/api/v2/json/pulls/'
API_BASE = getattr(settings, 'GITHUB_API_BASE', DEFAULT_API_BASE)

import logging
log = logging.getLogger('detracify.github')


class GithubAPI(object):
    def __init__(self):
        pass

    def get_open_pull_requests(self):
        open_reqs_url = API_BASE + "pulls/django/django/open"
        log.debug('fetching: %s' % open_reqs_url)
        r = requests.get(open_reqs_url)
        log.debug(r.status_code)
        if not r.status_code == 200:
            log.error('Github returned a non-200 response!: %s' % r.content)
    #    log.debug(r.content)
        data = json.loads(r.content)
        pulls = data['pulls']
        return pulls
