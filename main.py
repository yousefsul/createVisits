import logging
from createVisits import CreateVisits


# formatting my code logging
logging_format = "%(asctime)s =>  %(message)s"
logging.basicConfig(filename="visitsList.log", filemode="w", format=logging_format, level=logging.INFO,
                    datefmt="%H:%M:%S")

if __name__ == '__main__':
    """
    Main Method
    Create object from class CreateVisits
    call method search_patients_appoitemnts
    """
    create_visits = CreateVisits()
    create_visits.search_patients_appoitemnts()