from flask import request, Blueprint
from flasgger import swag_from
from ..utils.util import custom_response, custom_response_csv
from ..utils.authentication import requires_authentication_device

from ..engine.sensors_data import add_sensors_data
from ..model.schemas.SensorsDataSchema import SensorsDataSchema

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

    add_sensors_data(deviceId, data)
    return custom_response({ "msg" : "Save Data"}, 200)


#
@devices_api.route('/data', methods=['GET'])
def get_sensors_data():
    userId = request.args.get("user_id")
    
    sql = text("""SELECT Users.idUser, Farms.idFarm, Farms.Name, Beehives.idBeehive, Beehives.Name, SensorsData.idSensorsData, SensorsData.Date, SensorsData.Weight FROM Users INNER JOIN Farms ON Users.idUser = Farms.idUser INNER JOIN Beehives ON Farms.idFarm = Beehives.idFarm INNER JOIN SensorsData ON Beehives.idBeehive = SensorsData.idBeehive WHERE Users.idUser = :idUser;""")

    rs = db.engine.execute(sql, {"idUser": userId})

    csv = ""
    csv += ",".join(rs.keys()) + "\n"

    for record in rs:
        csv += ",".join(str(v) for v in record) + "\n"

    return custom_response_csv(csv, 200)


