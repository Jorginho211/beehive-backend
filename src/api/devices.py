from flask import request, Blueprint
from flasgger import swag_from
from ..utils.util import custom_response, custom_response_csv
from ..utils.authentication import requires_authentication_device

from ..exts import db
from ..engine.sensors_data import add_sensors_data
from ..engine.meteosix_data import add_meteosix_data
from ..model.schemas.SensorsDataSchema import SensorsDataSchema

from ..model.model import *

from marshmallow import ValidationError,pprint
import json

#Temporales para obtener los datos
from ..exts import db
from sqlalchemy.sql import text

devices_api = Blueprint('devices', __name__)

@devices_api.route('/device', methods=['POST'])
@requires_authentication_device
@swag_from('docs/devices/save_sensors_data.yml')
def save_sensors_data():
    deviceId = request.headers.get("device_id")
    data = request.json

    errors = SensorsDataSchema(many=True).validate(data)
    if errors:
        return custom_response({ "msg" : "Not satisfied model"}, 400)            

    meteoSixData = add_meteosix_data(deviceId)
    add_sensors_data(deviceId, data, meteoSixData)

    return custom_response({ "msg" : "Save Data"}, 200)


#
@devices_api.route('/data', methods=['GET'])
def get_sensors_data():
    userId = request.args.get("user_id")
    
    sql = """SELECT Users.idUser, Farms.idFarm, Farms.Name, Beehives.idBeehive, Beehives.Name, SensorsData.idSensorsData, 
                    SensorsData.Date, MeteoSixData.Temperature, MeteoSixData.RelativeHumidity, MeteoSixData.CloudAreaFraction, 
                    MeteoSixData.PrecipitationAmount, Round(SensorsData.Weight/10, 1)
                    FROM Users 
                    INNER JOIN Farms ON Users.idUser = Farms.idUser 
                    INNER JOIN Beehives ON Farms.idFarm = Beehives.idFarm 
                    INNER JOIN SensorsData ON Beehives.idBeehive = SensorsData.idBeehive 
                    LEFT JOIN SensorsData_has_MeteoSixData ON SensorsData_has_MeteoSixData.idSensorsData = SensorsData.idSensorsData 
                        AND SensorsData_has_MeteoSixData.idUser = SensorsData.idUser 
                        AND SensorsData_has_MeteoSixData.idFarm = SensorsData.idFarm 
                        AND SensorsData_has_MeteoSixData.idBeehive = SensorsData.idBeehive 
                    LEFT JOIN MeteoSixData ON SensorsData_has_MeteoSixData.idMeteoSixData = MeteoSixData.idMeteoSixData 
                    WHERE Users.idUser = %s ORDER BY SensorsData.Date"""
    
    cursor = db.execute_sql(sql, (userId))

    csv = ""
    csv = "idUser, idFarm, Name, idBeehive, Name, idSensorsData, Date, Temperature(ºC), Humidity(%), CloudAreaFraction(%), Precipitation(Lm2), Weight(Kg)\n"

    for row in cursor.fetchall():
        csv += ",".join(str(v) for v in row) + "\n"

    # csv = ""
    # csv += ",".join(rs.keys()) + "\n"

    # for record in rs:
    #     csv += ",".join(str(v) for v in record) + "\n"

    return custom_response_csv(csv, 200)


