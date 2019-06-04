from ..model.model import *
from ..dto.meteoSixDTO import MeteoSixDTO

from datetime import datetime, timedelta
import requests

def add_meteosix_data(device_id):
    device = Devices.select().where(Devices.Identifier == device_id).first()

    if device.Farm.Latitude is None or device.Farm.Longitude is None:
        return None

    meteosixDTO = get_meteosix_data(device.Farm.Latitude, device.Farm.Longitude)

    if meteosixDTO is None:
        return None

    return insert_meteosix_data(device.idFarm, device.idUser, meteosixDTO)


def get_meteosix_data(latitude, longitude): 
    timeRounded = rounder_time(datetime.now())
    strTime = timeRounded.strftime("%Y-%m-%dT%H:%M:%S")
    url = "http://servizos.meteogalicia.es/apiv3/getNumericForecastInfo?coords=%.8f,%.8f&variables=temperature,cloud_area_fraction,precipitation_amount,relative_humidity&startTime=%s&endTime=%s&lang=en&API_KEY=ceA4A5AePD035sIW2069WhsoCIwSCb7et68EuMy8J7lrkQFw07Vp4Vxp31bp32AZ" %(longitude, latitude, strTime, strTime)
    response = requests.get(url)

    json = response.json()

    if  response.status_code != requests.codes.ok:
        return None

    variables = json['features'][0]['properties']['days'][0]['variables']
    return MeteoSixDTO(
        latitude = latitude,
        longitude = longitude,
        timeInstant = timeRounded,
        temperature = variables[0]['values'][0]['value'],
        precipitationAmount = variables[1]['values'][0]['value'],
        relativeHumidity = variables[2]['values'][0]['value'],
        cloudAreaFraction = variables[3]['values'][0]['value']
    )


def insert_meteosix_data(idFarm, idUser, meteoSixDTO):
    newMeteoSixId = 1

    meteoSixData = MeteoSixData.select().where(MeteoSixData.idUser == idUser, MeteoSixData.idFarm == idFarm).order_by(MeteoSixData.idMeteoSixData.desc()).first()
    
    if meteoSixData:
        newMeteoSixId += meteoSixData.idMeteoSixData

    meteoSixData = MeteoSixData.create(
        idMeteoSixData = newMeteoSixId,
        idFarm = idFarm,
        idUser = idUser,
        DatePrediction = meteoSixDTO.TimeInstant,
        Temperature = meteoSixDTO.Temperature,
        RelativeHumidity = meteoSixDTO.RelativeHumidity,
        PrecipitationAmount = meteoSixDTO.PrecipitationAmount,
        CloudAreaFraction = meteoSixDTO.CloudAreaFraction
    )

    meteoSixData.save();

    return meteoSixData

def rounder_time(t):
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

