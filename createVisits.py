import datetime

import shortuuid

from clientInfo import ClientInfo
from connectMongoDB import ConnectMongoDB
from visitInfo import VisitInfo

"""
class Search

Methods:

constructor  -->
    params no params

    call from --> main method
----------------------------------------------------------
search_patients_appoitemnts
    params no params

    call from --> main method
----------------------------------------------------------
Functions:
merge_patient_appointment -->
    params tow dictionary : the first one for the appointemnt and the second one for the paitent

    call from --> search_patients_appoitemnts method

    return merged dictionary for the tow dictionaries
----------------------------------------------------------
get_current_status -->
    params no params 
    
    call from create_visits method
----------------------------------------------------------
generate_vist_id -->
    params no params 
    
    call from create_visits method
    """


# retrun merged dictionary for the appointment and patient
def merge_patient_appointment(patient_data, appointemnt_data):
    res = {**patient_data, **appointemnt_data}
    return res


# create visit with current status new
def get_current_status():
    current_status = {
        "status": "new",
        "date": {
            "date": datetime.datetime.now().date().strftime("%Y%m%d"),
            "time": datetime.datetime.now().time().strftime("%H:%M:%S")
        }
    }
    return current_status


# return id for each new visit
def generate_vist_id():
    return int(shortuuid.ShortUUID(alphabet="0123456789").random(length=10).lower())


class CreateVisits:
    """
    define patients,appointment,patient_data,appointemnt_data as none
    define visits_data lists to have all visits for patients
    define visit date and time created
    create object from class ConnectMongoDB named connection
    """

    def __init__(self):
        self.patients = None
        self.appointemnts = None
        self.patient_data = None
        self.appointemnt_data = None
        self.visits_data = []
        self.visit_date = datetime.datetime.now().date().strftime("%Y%m%d")
        self.visit_time = datetime.datetime.now().time().strftime("%H:%M:%S")
        self.status_histroy = [get_current_status()]
        self.connection = ConnectMongoDB()

    """
    get the patients and appointemnts from database search for the matching result by name 
    call merge_patient_appointment method and append the result to visits list 
    """

    def search_patients_appoitemnts(self):
        self.connection.connect_to_patients_collection()
        self.connection.connect_to_appointments_collection()
        self.patient_data = self.connection.get_patinets_data()
        self.appointemnt_data = self.connection.get_appointments_data()
        for appointemnt_data in self.appointemnt_data:
            for patient_data in self.patient_data:
                if appointemnt_data.get("patient_name")["last"] == \
                        patient_data.get("patient_info")["patient_name"]["last"] \
                        and appointemnt_data.get("patient_name")["first"] == \
                        patient_data.get("patient_info")["patient_name"]["first"]:
                    self.visits_data.append(merge_patient_appointment(patient_data, appointemnt_data))
                    self.patient_data.rewind()
                    break

    """
    get the client information and consrtuct the vistis sections 
    insert the result in database 
    """

    def create_visits(self):
        self.connection.connect_to_visits_collection()
        self.connection.connect_to_client_collection()
        client = self.connection.get_afroza_ahmed_info()
        client_info = ClientInfo(client)
        rendering_provider_info = client_info.get_rendering_provider_info()
        for visit in self.visits_data:
            visit_info = VisitInfo(visit, rendering_provider_info)
            result = {
                "header_section": {
                    "visit_id": generate_vist_id(),
                    "date_created": {
                        "date": self.visit_date,
                        "time": self.visit_time
                    },
                    "current_status": get_current_status(),
                    "status_history": self.status_histroy
                },
                "client_info": client_info.get_client_info(),
                "patient_info": visit_info.get_patient_info(),
                "insurance_info": {
                    "primary_insurance": visit_info.get_primary_insurance(),
                    "secondary_insurance": visit_info.get_secondary_insurance(),
                    "tertiary_insurance": visit_info.get_tertiary_insurance()
                },
                "home_plan_insurance": visit_info.get_home_plan_insurance(),
                "plan_admin": visit_info.get_plan_admin(),
                "service_facility_info": client_info.get_service_facility_info(),
                "billing_provider_info": client_info.get_billing_provider_info(),
                "events_date": visit_info.get_events_date(),
                "miscellaneous": {"prior_authorization_number": ""},
                "physician": {
                    "ordering": visit_info.get_physician_ordering(),
                    "referring": visit_info.get_referring_ordering(),
                    "supervising": visit_info.get_supervising_ordering(),
                },
                "service_line": visit_info.get_service_line()
            }
            self.connection.insert_to_visits_collection(result)
            self.connection.update_status_for_appointment_collection(visit_info.get_appointment_id())
            self.connection.update_appointment_current_status(visit_info.get_appointment_id())
