from endpoint import Endpoint



class BinaryAnnotation:
    def __init__(self, endpoint, key=None, value=None):
        if isinstance(endpoint, Endpoint):
            self.endpoint = endpoint
        elif isinstance(endpoint, dict):
            self.endpoint = Endpoint(endpoint["service_name"], endpoint["ipv4"])
        self.key = key
        self.value = value

    def set_binary_annotation(self, key, value):
        self.key = key
        self.value = value
