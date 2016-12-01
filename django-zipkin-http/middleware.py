import logging
import django
import json
from span.constants import SERVER_RECV, SERVER_SEND
from zipkin_data import ZipkinData, ZipkinId
from data_store import default as default_data_store
from id_generator import SimpleIdGenerator
from api import api as default_api
import constants
import defaults as settings
import zipkin_http


if django.VERSION[0] == 1 and django.VERSION[1] < 5:
    from django.core.urlresolvers import resolve

    # TODO: caching the resolutions may be a good idea
    def resolve_request(request):
        return resolve(request.path_info)
elif django.VERSION[0] == 1 and django.VERSION[1] >= 5:
    def resolve_request(request):  # pyflakes:ignore
        return request.resolver_match
else:
    def resolve_request(request):  # pyflakes:ignore
        return None


def _hdr_to_meta_key(h):
    return 'HTTP_' + h.upper().replace('-', '_')


class ZipkinDjangoRequestParser(object):
    trace_id_hdr_name = _hdr_to_meta_key(constants.TRACE_ID_HDR_NAME)
    span_id_hdr_name = _hdr_to_meta_key(constants.SPAN_ID_HDR_NAME)
    parent_span_id_hdr_name = _hdr_to_meta_key(constants.PARENT_SPAN_ID_HDR_NAME)
    sampled_hdr_name = _hdr_to_meta_key(constants.SAMPLED_HDR_NAME)
    flags_hdr_name = _hdr_to_meta_key(constants.FLAGS_HDR_NAME)

    def get_zipkin_data(self, request):
        return ZipkinData(
            trace_id=ZipkinId.from_hex(request.META.get(self.trace_id_hdr_name, None)),
            span_id=ZipkinId.from_hex(request.META.get(self.span_id_hdr_name, None)),
            parent_span_id=ZipkinId.from_hex(request.META.get(self.parent_span_id_hdr_name, None)),
            # sampled=request.META.get(self.sampled_hdr_name, 'false') == 'true',
            sampled=True,
            flags=request.META.get(self.flags_hdr_name, '0') == '1'
        )


class ZipkinMiddleware(object):
    def __init__(self, store=None, api=None):
        self.store = store or default_data_store
        self.request_parser = ZipkinDjangoRequestParser()
        self.id_generator = SimpleIdGenerator()
        self.api = api or default_api

    def process_request(self, request):
        try:
            data = self.request_parser.get_zipkin_data(request)
            if data.trace_id is None:
                data.trace_id = self.id_generator.generate_trace_id()
            data.parent_span_id = data.span_id
            data.span_id = self.id_generator.generate_span_id()
            self.store.set(data)
            self.api.set_endpoint(request.META["REMOTE_ADDR"])
            self.api.set_rpc_name(request.method)
            self.api.record_event(SERVER_RECV)
            self.api.record_key_value(constants.ANNOTATION_HTTP_URI, request.get_full_path())
            request.trace_id = str(int(data.trace_id.get_hex(), 16))
            request.span_id = str(int(data.span_id.get_hex(), 16))
        except Exception:
            logging.root.exception('ZipkinMiddleware.process_request failed')

    def process_response(self, request, response):
        try:
            data = self.store.get()
            if data.trace_id is None:
                self.process_request(request)
                self.api.record_event(constants.ANNOTATION_NO_DATA_IN_LOCAL_STORE)
                data = self.store.get()
            self.api.record_event(SERVER_SEND)
            self.api.record_key_value(constants.ANNOTATION_HTTP_STATUSCODE, response.status_code)
            if data.is_tracing():
                self.api.report_json_to_zipkin()
        except Exception:
            logging.root.exception('ZipkinMiddleware.process_response failed')
        return response
