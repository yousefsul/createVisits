from connectMongoDB import ConnectMongoDB

"""
class Search

Methods:

constructor  -->
    no params

    call from --> main method
----------------------------------------------------------
search_patients_appoitemnts
    no params

    call from --> main method
----------------------------------------------------------
Functions:
merge_patient_appointment -->
    param tow dictionary : the first one for the appointemnt and the second one for the paitent

    call from --> search_patients_appoitemnts method

    return merged dictionary for the tow dictionaries
    """


def merge_patient_appointment(patient_data, appointemnt_data):
    res = {**patient_data, **appointemnt_data}
    return res


class CreateVisits:
    def __init__(self):
        self.patients = None
        self.appointemnts = None
        self.patient_data = None
        self.appointemnt_data = None
        self.visits_data = []
        self.connection = ConnectMongoDB()

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