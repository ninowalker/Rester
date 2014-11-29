from logging import getLogger
from rester.struct import ResponseWrapper
import json
import requests


class HttpClient(object):
    logger = getLogger(__name__)

    def __init__(self, **kwargs):
        self.extra_request_opts = kwargs

    def request(self, api_url, method, headers, params, is_raw, data=None):
        self.logger.info(
            '\n Invoking REST Call... api_url: %s, method: %s : ', api_url, method)

        try:
            func = getattr(requests, method)
        except AttributeError:
            self.logger.error('undefined HTTP method!!! %s', method)
            raise

        kwargs = dict(headers=headers, params=params, **self.extra_request_opts)
        if data != None:
            kwargs['data'] = data
        response = func(api_url, **kwargs)

        if is_raw:
            payload = {"__raw__": response.text}
        else:
            payload = response.json()

        if response.status_code < 300:
            emit = self.logger.debug
        else:
            emit = self.logger.warn
        emit('Response Headers: %s', str(response.headers))
        if is_raw:
            emit('Response:\n%s\n' + response.text)
        else:
            emit('Response:\n%s\n' + json.dumps(payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, response.headers)
