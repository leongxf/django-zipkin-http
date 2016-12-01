from endpoint import Endpoint



class Annotation:
    def __init__(self, endpoint, timestamp=None, value=None):
        if isinstance(endpoint, Endpoint):
            self.endpoint = endpoint
        elif isinstance(endpoint, dict):
            self.endpoint = Endpoint(endpoint["service_name"], endpoint["ipv4"])
        self.timestamp = timestamp
        self.value = value

    def set_value(self, value):
        self.value = value

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp