import json

class Patient:
    patients_data = []

    def __init__(self, name, room):
        self.name = name
        self.room = room

    @classmethod
    def add_patient(cls, name, room):
        cls.patients_data.append(cls(name, room))

    @classmethod
    def save_to_file(cls, filename):
        with open(filename, 'w') as file:
            # print([patient.__dict__ for patient in cls.patients_data])
            json.dump([patient.__dict__ for patient in cls.patients_data], file, indent=4)
       


Patient.add_patient("John Doe", "ER-152")
Patient.add_patient("Jane Smith", "ICU-209")
Patient.add_patient("Bob Brown",  "ER-306")


Patient.save_to_file("patients.json")