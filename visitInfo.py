import shortuuid
from bson import Decimal128

"""
class CisitInfo

Methods:

constructor  -->
    param : visit info data

    call from --> create_visit method in CreateVisits class
----------------------------------------------------------
getters
----------------------------------------------------------
Functions 
generate_line_id -->
    params no params 
    
    call from get_service_line
"""


def generate_line_id():
    return int(shortuuid.ShortUUID(alphabet="0123456789").random(length=10).lower())


class VisitInfo:
    def __init__(self, visit_info, rendering_provider):
        self.visit_info = visit_info
        self.rendering_provider = rendering_provider
        self.events_date = {
            "onset_of_current": "",
            "initial_treatment": "",
            "last_visit": "",
            "first_visit": "",
        }
        self.physician_ordering = [{}]
        self.referring_ordering = [{}]
        self.supervising_ordering = [{}]
        self.service_line = []

    def get_patient_info(self):
        return self.visit_info.get("patient_info")

    def get_events_date(self):
        return self.events_date

    def get_physician_ordering(self):
        return self.physician_ordering

    def get_referring_ordering(self):
        return self.referring_ordering

    def get_supervising_ordering(self):
        return self.supervising_ordering

    def get_service_line(self):
        service_line = {
            "date_of_service": self.visit_info.get("date_of_service"),
            "place_of_service": self.visit_info.get("place_of_service"),
            "cpt": self.visit_info.get("billing_code"),
            "rendering_provider": self.rendering_provider,
            "modifiers": self.visit_info.get("modifiers"),
            "total_charge": self.visit_info.get("total_fee"),
            "unit": self.visit_info.get("units"),
            "pointer": self.get_dx_code_pointers(),
            "line_number_control": generate_line_id(),
            "payment": {
                "insurance": Decimal128(str(0.00)),
                "patient": Decimal128(str(0.00))
            },
            "patient_balance": Decimal128(str(0.00))
        }
        self.service_line.append(service_line)
        return self.service_line

    def get_dx_codes(self):
        return self.visit_info.get("patient_info").get("dx_codes")

    def get_primary_insurance(self):
        return self.visit_info.get("primary_insurance")

    def get_secondary_insurance(self):
        return self.visit_info.get("secondary_insurance")

    def get_tertiary_insurance(self):
        return self.visit_info.get("tertiary_insurance")

    def get_dx_code_pointers(self):
        pointer = []
        pointer_count = 1
        for _ in self.get_dx_codes():
            pointer.append(str(pointer_count))
            pointer_count += 1
        return pointer

    def get_home_plan_insurance(self):
        return self.visit_info.get("home_plan_insurance")

    def get_plan_admin(self):
        return self.visit_info.get("plan_admin")
