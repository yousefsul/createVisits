import datetime
import logging

from pymongo import MongoClient

MONGO_CLIENT = "mongodb://yousef:Ys2021xch@209.151.150.58:63327/?authSource=admin&readPreference=primary&appname" \
               "=MongoDB%20Compass&ssl=false"


class ConnectMongoDB:
    def __init__(self):
        try:
            self.mongo_client = MongoClient(MONGO_CLIENT)
            self.dev_db = self.mongo_client.devDB
            self.client_db = self.mongo_client.client_2731928905_DB
            self.patients_collection = None
            self.appointments_collection = None
            self.clients_collection = None
            self.visits_collection = None
        except ConnectionError:
            logging.error("constructor Method:         Error while connect to mongoDB")
            print("Error while connection to mongoDB")

    def connect_to_patients_collection(self):
        self.patients_collection = self.client_db.patientsColl

    def connect_to_appointments_collection(self):
        self.appointments_collection = self.client_db.appointmentsColl

    def get_patinets_data(self):
        return self.patients_collection.find()

    def get_appointments_data(self):
        return self.appointments_collection.find(
            {"header_section.current_status.status": "new"}
        )

    def connect_to_client_collection(self):
        self.clients_collection = self.dev_db.clientsColl

    def get_afroza_ahmed_info(self):
        return self.clients_collection.find_one(
            {
                "client_info.contact.first": "Afroza",
                "client_info.contact.last": "Ahmed"
            }
        )

    def connect_to_visits_collection(self):
        self.visits_collection = self.client_db.visitsColl

    def insert_to_visits_collection(self, result):
        try:
            self.visits_collection.insert(result)
        except Exception as e:
            print("An Exception occurred ", e)

    def update_status_for_appointment_collection(self, appointment_id):
        self.appointments_collection.update_one(
            {"_id": appointment_id},
            {"$push": {
                "header_section.status_history": {
                    "status": "visit created",
                    "date": {
                        "date": datetime.datetime.now().date().strftime("%Y%m%d"),
                        "time": datetime.datetime.now().time().strftime("%H:%M:%S")
                    }
                }
            }}
        )

    def update_appointment_current_status(self, appointment_id):
        self.appointments_collection.find_and_modify(
            query={"_id": appointment_id},
            update={"$set": {
                "header_section.current_status.status": "visit created",
                "header_section.current_status.date": {
                    "date": datetime.datetime.now().date().strftime("%Y%m%d"),
                    "time": datetime.datetime.now().time().strftime("%H:%M:%S")
                }}
            },
            upsert=True
        )
