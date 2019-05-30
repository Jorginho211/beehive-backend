from ..model.model import *

def add_sensors_data(device_id, data, meteoSixData):
    device = Devices.select().where(Devices.Identifier == device_id).first()

    for BeehiveData in data:
        idBeehive = BeehiveData['number']

        weight = None
        if "weight" in BeehiveData:
            weight = BeehiveData['weight']

        create_beehive(idBeehive, device.Farm.idFarm, device.Farm.idUser)
        sensorsData = add_beehive_data(idBeehive, device.Farm.idFarm, device.Farm.idUser, weight)
        
        if meteoSixData:
            asociate_meteo_six_data_with_sensors_data(meteoSixData, sensorsData)


def create_beehive(idBeehive, idFarm, idUser):
    beehive = Beehives.select().where(Beehives.idUser == idUser, Beehives.idFarm == idFarm, Beehives.idBeehive == idBeehive).first()
    if not beehive:
        beehive = Beehives.create(
            idBeehive = idBeehive, 
            idFarm = idFarm, 
            idUser = idUser)
        beehive.save()


def add_beehive_data(idBeehive, idFarm, idUser, weight):
    newSensorsDataId = 1

    sensorsData = SensorsData.select().where(SensorsData.idUser == idUser, SensorsData.idFarm == idFarm, SensorsData.idBeehive == idBeehive).order_by(SensorsData.idSensorsData.desc()).first()
    if sensorsData:
        newSensorsDataId += sensorsData.idSensorsData

    sensorsData = SensorsData.create(
        idSensorsData = newSensorsDataId, 
        idBeehive = idBeehive, 
        idFarm = idFarm, 
        idUser = idUser, 
        Weight = weight)

    sensorsData.save()

    return sensorsData

def asociate_meteo_six_data_with_sensors_data(meteoSixData, sensorsData):
    sensorsDataMeteoSixData = SensorsDataHasMeteoSixData.create(
        idUser = sensorsData.idUser,
        idFarm = sensorsData.idFarm,
        idBeehive = sensorsData.idBeehive,
        idSensorsData = sensorsData.idSensorsData,
        idMeteoSixData = meteoSixData.idMeteoSixData)

    sensorsDataMeteoSixData.save();
