class Endpoint:
    def __init__(self, service_name=None, ipv4=None):
        self.serviceName = service_name
        self.ipv4 = ipv4

    def set_service_name(self, service_name):
        self.serviceName = service_name

    def set_ipv4(self, ipv4):
        self.ipv4 = ipv4
        