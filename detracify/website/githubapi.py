import requests
import simplejson as json
from django.conf import settings
from website.models import PullReq

API_BASE = getattr(settings, 'GITHUB_API_BASE', 'http://github.com/api/v2/json/pulls/')

import logging
log = logging.getLogger('detracify.github')

def get_open_pull_requests():
    open_reqs_url = API_BASE + "pulls/django/django/open"
    log.debug('fetching: %s' % open_reqs_url)
    r = requests.get(open_reqs_url)
    log.debug(r.status_code)
    if not r.status_code == 200:
        log.error('Github returned a non-200 response!: %s' % r.content)
#    log.debug(r.content)
    data = json.loads(r.content)
    pulls = data['pulls']
    for pull in pulls:
        log.info("""
Pull %s:
        number: %d
        http_url: %s
        patch_url: %s
        user: %s <%s>
        %s
""" % (
            pull['number'], pull['number'],
            pull['html_url'], pull['patch_url'],
            pull['user']['name'], pull['user']['email'],
            pull['body']
        ))
    return pulls
