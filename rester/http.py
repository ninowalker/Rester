from logging import getLogger
from rester.struct import ResponseWrapper
import json
import requests
import time


class HttpClient(object):
    logger = getLogger(__name__)

    # added header with how long the response took.
    H_ELAPSED = '__elapsed__'

    def __init__(self, **kwargs):
        if kwargs.pop('session', False):
            self._client = requests.Session()
        else:
            self._client = requests
        self.extra_request_opts = kwargs

    def request(self, api_url, method, headers, params, is_raw, data=None):
        self.logger.info(
            '\n Invoking REST Call... api_url: %s, method: %s, headers %s : ', api_url, method, headers)

        try:
            func = self._func(method)
        except AttributeError:
            self.logger.error('undefined HTTP method!!! %s', method)
            raise

        kwargs = dict(headers=headers, params=params, **self.extra_request_opts)
        if data != None:
            kwargs['data'] = data
        start = time.time()
        response = func(api_url, **kwargs)
        elapsed = time.time() - start

        if is_raw == True or (is_raw is None and 'application/json' not in response.headers.get('content-type', '')):
            payload = {"__raw__": response.text}
        else:
            payload = response.json()

        rheaders = dict(response.headers)
        rheaders[self.H_ELAPSED] = elapsed

        if response.status_code < 300:
            emit = self.logger.debug
        else:
            emit = self.logger.warn
        emit('Response Headers: %s', str(rheaders))
        if is_raw:
            emit('Response:\n%s\n' + response.text)
        else:
            emit('Response:\n%s\n' + json.dumps(payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, rheaders)

    def _func(self, method):
        return getattr(self._client, method)