DEFAULT_ZIPKIN_ID_GENERATOR_CLASS = 'django-zipkin-http.id_generator.SimpleIdGenerator'
DEFAULT_ZIPKIN_SERVICE_NAME = "HTTP-service"
DEFAULT_ZIPKIN_DATA_STORE_CLASS = 'django-zipkin-http.data_store.ThreadLocalDataStore'

DEFAULT_ZIPKIN_HTTP_HOST = "http://localhost:9411" 
DEFAULT_ZIPKIN_HTTP_API = "/api/v1/"
DEFAULT_ZIPKIN_HTTP_SPAN = "spans" 

TRACE_ID_HDR_NAME = "X-B3-TraceId"
SPAN_ID_HDR_NAME = "X-B3-SpanId"
PARENT_SPAN_ID_HDR_NAME = "X-B3-ParentSpanId"
SAMPLED_HDR_NAME = "X-B3-Sampled"
FLAGS_HDR_NAME = "X-B3-Flags"

ANNOTATION_HTTP_URI = 'http.uri'
ANNOTATION_HTTP_STATUSCODE = 'http.statuscode'

ANNOTATION_NO_DATA_IN_LOCAL_STORE = 'No ZipkinData in thread local store. This can happen if process_request ' + \
                                    'didn\'t run due to a previous middleware returning a response. Timing ' + \
                                    'information is invalid.'
