import struct
import socket
import time
import base64
import logging
import json
import threading

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport

import constants
import defaults as settings
from data_store import default as default_store
from zipkin_http import HTTPReporter
from span.endpoint import Endpoint
from span.annotation import Annotation
from span.binary_annotation import BinaryAnnotation
from span.span import Span



class ZipkinApi(object):
    def __init__(self, store=None, service_name=None, ipv4=None):
        self.store = store or default_store
        self.service_name = service_name or settings.ZIPKIN_SERVICE_NAME
        self.endpoint = Endpoint()
    
    def set_endpoint(self, ipv4=None):
        self.endpoint = Endpoint(
            ipv4=ipv4,
            service_name=self.service_name
        )

    def record_event(self, message):
        self.store.record(self._build_annotation(message))

    def record_key_value(self, key, value):
        self.store.record(self._build_binary_annotation(key, value))

    def set_rpc_name(self, name):
        self.store.set_rpc_name(name)

    def build_message_json(self):
        span_instance = self._build_span()
        span = {}
        span["name"] = span_instance.name
        span["traceId"] = str(span_instance.trace_id)
        span["binaryAnnotations"] = [{"key": each_bin.key, "value": str(each_bin.value), "endpoint": self._build_json_endpoint(each_bin.endpoint)} for each_bin in span_instance.binary_annotations]
        span["annotations"] = [{"value": each_anno.value, "timestamp":each_anno.timestamp, "endpoint": self._build_json_endpoint(each_anno.endpoint)} for each_anno in span_instance.annotations]
        sr_time = span_instance.annotations[0].timestamp
        ss_time = span_instance.annotations[1].timestamp
        span["duration"] = ss_time - sr_time
        span["id"] = span_instance.span_id
        span["timestamp"] = sr_time
        return [span]

    def report_json_to_zipkin(self):
        json_send = self.build_message_json()
        th = threading.Thread(target=HTTPReporter.report, args=(json_send, ))
        th.start()

    def get_headers_for_downstream_request(self):
        try:
            data = self.store.get()
            headers = {
                constants.TRACE_ID_HDR_NAME: data.trace_id.get_hex() if data.trace_id is not None else None,
                constants.SPAN_ID_HDR_NAME: data.span_id.get_hex() if data.span_id is not None else None,
                constants.SAMPLED_HDR_NAME: self._bool_to_str_true_false(data.sampled),
                constants.FLAGS_HDR_NAME: self._bool_to_str_1_0(data.flags)
            }
            if data.parent_span_id is not None:
                headers[constants.PARENT_SPAN_ID_HDR_NAME] = data.parent_span_id.get_hex()
            for key in headers.keys():
                if headers[key] is None:
                    del headers[key]
            return headers
        except Exception:
            logging.root.exception("failed_to_build_downstream_request_headers")
            return {}

    def _bool_to_str_true_false(self, b):
        if b:
            return 'true'
        return 'false'

    def _bool_to_str_1_0(self, b):
        if b:
            return '1'
        return '0'

    def _build_span(self):
        zipkin_data = self.store.get()
        return Span(
            self.store.get_rpc_name(),
            trace_id=zipkin_data.trace_id.get_binary(),
            parent_id=zipkin_data.parent_span_id.get_binary() if zipkin_data.parent_span_id is not None else None,
            annotations=self.store.get_annotations(),
            binary_annotations=self.store.get_binary_annotations(),
            span_id=zipkin_data.span_id.get_binary()            
        )

    def _build_annotation(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        return Annotation(self.endpoint, time.time() * 1000 * 1000, str(value))

    def _build_binary_annotation(self, key, value):
        return BinaryAnnotation(self.endpoint, key, value)

    @staticmethod
    def _build_json_endpoint(endpoint, keys=["ipv4", "serviceName"]):
        endpoint_dict = {}
        for key in keys:
            endpoint_dict[key] = getattr(endpoint, key)                    
        return endpoint_dict


api = ZipkinApi(default_store)
