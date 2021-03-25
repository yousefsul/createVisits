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
        return self.appointments_collection.find()
