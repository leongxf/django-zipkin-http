import threading
import functools

from utils import import_class
import defaults as settings
from zipkin_data import ZipkinData
from span.annotation import Annotation
from span.binary_annotation import BinaryAnnotation


class BaseDataStore(object):
    def set(self, data):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def _record_annotation(self, annotation):
        raise NotImplementedError

    def _record_binary_annotation(self, annotation):
        raise NotImplementedError

    def record(self, annotation):
        if not self.get().is_tracing():
            return
        if isinstance(annotation, Annotation):
            self._record_annotation(annotation)
        elif isinstance(annotation, BinaryAnnotation):
            self._record_binary_annotation(annotation)
        else:
            raise ValueError("Argument to %s.record must be an instance of Annotation or BinaryAnnotation" % self.__class__.__name__)

    def set_rpc_name(self, name):
        raise NotImplementedError

    def get_rpc_name(self):
        raise NotImplementedError

    def get_annotations(self):
        raise NotImplementedError

    def get_binary_annotations(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


def _clear_and_retry_on_attribute_error(method):
    @functools.wraps(method)
    def f(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except AttributeError as e:
            self.clear()
            return method(self, *args, **kwargs)
    return f


class ThreadLocalDataStore(BaseDataStore):
    zipkin_data = ZipkinData()
    annotations = []
    binary_annotations = []
    rpc_name = None

    @_clear_and_retry_on_attribute_error
    def get(self):
        return self.zipkin_data

    @_clear_and_retry_on_attribute_error
    def set(self, data):
        self.zipkin_data = data
        self.annotations = []
        self.binary_annotations = []
        self.rpc_name = None

    @_clear_and_retry_on_attribute_error
    def _record_annotation(self, annotation):
        self.annotations.append(annotation)

    @_clear_and_retry_on_attribute_error
    def _record_binary_annotation(self, annotation):
        self.binary_annotations.append(annotation)

    @_clear_and_retry_on_attribute_error
    def get_annotations(self):
        return self.annotations

    @_clear_and_retry_on_attribute_error
    def get_binary_annotations(self):
        return self.binary_annotations

    @_clear_and_retry_on_attribute_error
    def set_rpc_name(self, name):
        self.rpc_name = name

    @_clear_and_retry_on_attribute_error
    def get_rpc_name(self):
        return self.rpc_name

    @classmethod
    def clear(cls):
        cls.zipkin_data = ZipkinData()
        cls.annotations = []
        cls.binary_annotations = []
        cls.rpc_name = None


default = import_class(settings.ZIPKIN_DATA_STORE_CLASS)()
