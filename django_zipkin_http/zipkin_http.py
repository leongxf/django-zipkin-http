import logging
import requests
from defaults import ZIPKIN_HTTP_HOST, ZIPKIN_HTTP_API, ZIPKIN_HTTP_SPAN


class HTTPReporter:
    def __init__(self, host):
        self.host = host

    @classmethod
    def report(cls, json, host=ZIPKIN_HTTP_HOST):
        logging.debug("Sending: %s" % json)
        r = cls(host)._send_span(json)
        if r.status_code == 202:
            return r.status_code, r.text
        else:
            raise Exception("Error occured when reporting to zipkin:", r.text)
            

    def _send_span(self, json_input):
        url = self.host + ZIPKIN_HTTP_API + ZIPKIN_HTTP_SPAN
        return requests.post(url, json=json_input)
