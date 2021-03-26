import math
"""
class VisitInfo

Methods:

constructor  -->
    param : client info data

    call from --> create_visit method in Search class
----------------------------------------------------------
getters
----------------------------------------------------------
"""


class ClientInfo:
    def __init__(self, client_info):
        self.client_info = client_info

    def get_client_info(self):
        return self.client_info.get("client_info")

    def get_service_facility_info(self):
        return self.client_info.get("service_facility_info")

    def get_billing_provider_info(self):
        return self.client_info.get("billing_provider")

    def get_rendering_provider_info(self):
        return self.client_info.get("rendering_provider")