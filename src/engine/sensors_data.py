from ..model.model import *
from ..exts import db

def add_sensors_data(device_id, data):
    device = Device.query.filter(Device.Identifier == device_id).first()

    for BeehiveData in data:
        idBeehive = BeehiveData['number']

        weight = None
        if "weight" in BeehiveData:
                weight = BeehiveData['weight']

        create_beehive(idBeehive, device.Farm.idFarm, device.Farm.idUser)
        add_beehive_data(idBeehive, device.Farm.idFarm, device.Farm.idUser, weight)


def create_beehive(idUser, idFarm, idBeehive):
    beehive = Beehive.query.filter(Beehive.idUser == idUser, Beehive.idFarm == idFarm, Beehive.idBeehive == idBeehive).first()
    if not beehive:
        beehive = Beehive(idBeehive, idFarm, idUser)
        db.session.add(beehive)
        db.session.commit()

def add_beehive_data(idBeehive, idFarm, idUser, weight):
    newSensorsDataId = 1

    sensorsData = SensorsData.query.filter(SensorsData.idUser == idUser, SensorsData.idFarm == idFarm, Beehive.idBeehive == idBeehive).order_by(SensorsData.idSensorsData.desc()).first()
    if sensorsData:
        newSensorsDataId += sensorsData.idSensorsData

    sensorsData = SensorsData(newSensorsDataId, idBeehive, idFarm, idUser, weight)
    db.session.add(sensorsData)
    db.session.commit()
