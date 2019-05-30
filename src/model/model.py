from peewee import *
from ..exts import db

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    Email = CharField(column_name='Email')
    FirstName = CharField(column_name='FirstName')
    LastName = CharField(column_name='LastName')
    idUser = AutoField(column_name='idUser')

    class Meta:
        table_name = 'Users'

class Farms(BaseModel):
    Latitude = DecimalField(column_name='Latitude', null=True)
    Longitude = DecimalField(column_name='Longitude', null=True)
    Name = CharField(column_name='Name')
    idFarm = IntegerField(column_name='idFarm')
    idUser = ForeignKeyField(column_name='idUser', field='idUser', model=Users)

    User = ForeignKeyField(backref='Users_id_user_set', column_name='idUser', field='idUser', model=Users)

    class Meta:
        table_name = 'Farms'
        indexes = (
            (('idFarm', 'idUser'), True),
        )
        primary_key = CompositeKey('idFarm', 'idUser')

class Beehives(BaseModel):
    Name = CharField(column_name='Name')
    idBeehive = IntegerField(column_name='idBeehive')
    idFarm = ForeignKeyField(column_name='idFarm', field='idFarm', model=Farms)
    idUser = ForeignKeyField(column_name='idUser', field='idUser', model=Users)

    Farm = ForeignKeyField(backref='Farms_id_farm_set', column_name='idFarm', field='idFarm', model=Farms)
    User = ForeignKeyField(backref='Users_id_user_set', column_name='idUser', field='idUser', model=Users)

    class Meta:
        table_name = 'Beehives'
        indexes = (
            (('idBeehive', 'idUser', 'idFarm'), True),
            (('idFarm', 'idUser'), False),
        )
        primary_key = CompositeKey('idBeehive', 'idFarm', 'idUser')

class Credentials(BaseModel):
    Password = CharField(column_name='Password')
    TokenAuthentication = CharField(column_name='TokenAuthentication', null=True)
    TokenForgot = CharField(column_name='TokenForgot', null=True)
    Username = CharField(column_name='Username')
    idUser = ForeignKeyField(column_name='idUser', field='idUser', model=Users, primary_key=True)

    User = ForeignKeyField(backref='Users_id_user_set', column_name='idUser', field='idUser', model=Users)

    class Meta:
        table_name = 'Credentials'

class Devices(BaseModel):
    ApiKey = CharField(column_name='ApiKey', null=True)
    Identifier = CharField(column_name='Identifier', unique=True)
    idFarm = ForeignKeyField(column_name='idFarm', field='idFarm', model=Farms)
    idUser = ForeignKeyField(column_name='idUser', field='idUser', model=Users)

    Farm = ForeignKeyField(backref='Farms_id_farm_set', column_name='idFarm', field='idFarm', model=Farms)
    User = ForeignKeyField(backref='Users_id_user_set', column_name='idUser', field='idUser', model=Users)

    class Meta:
        table_name = 'Devices'
        indexes = (
            (('idFarm', 'idUser'), False),
            (('idUser', 'idFarm'), True),
        )
        primary_key = CompositeKey('idFarm', 'idUser')

class MeteoSixData(BaseModel):
    CloudAreaFraction = DecimalField(column_name='CloudAreaFraction')
    Date = DateTimeField(column_name='Date', constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    DatePrediction = DateTimeField(column_name='DatePrediction', constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    PrecipitationAmount = DecimalField(column_name='PrecipitationAmount')
    RelativeHumidity = DecimalField(column_name='RelativeHumidity')
    Temperature = IntegerField(column_name='Temperature')
    idUser = ForeignKeyField(column_name='idUser', field='idUser', model=Users)
    idFarm = ForeignKeyField(column_name='idFarm', field='idFarm', model=Farms)
    idMeteoSixData = IntegerField(column_name='idMeteoSixData')
    
    Farm = ForeignKeyField(backref='Farms_id_farm_set', column_name='idFarm', field='idFarm', model=Farms)
    User = ForeignKeyField(backref='Users_id_user_set', column_name='idUser', field='idUser', model=Users)

    class Meta:
        table_name = 'MeteoSixData'
        indexes = (
            (('idFarm', 'idUser'), False),
            (('idMeteoSixData', 'idFarm', 'idUser'), True),
        )
        primary_key = CompositeKey('idFarm', 'idMeteoSixData', 'idUser')

class SensorsData(BaseModel):
    Date = DateTimeField(column_name='Date', constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], index=True)
    Weight = IntegerField(column_name='Weight', index=True, null=True)
    idBeehive = ForeignKeyField(column_name='idBeehive', field='idBeehive', model=Beehives)
    idFarm = ForeignKeyField(column_name='idFarm', field='idFarm', model=Farms)
    idSensorsData = BigIntegerField(column_name='idSensorsData')
    idUser = ForeignKeyField(column_name='idUser', field='idUser', model=Users)


    Beehive = ForeignKeyField(backref='Beehives_id_Beehive_set', column_name='idBeehive', field='idBeehive', model=Beehives)
    Farm = ForeignKeyField(backref='Farms_id_farm_set', column_name='idFarm', field='idFarm', model=Farms)
    User = ForeignKeyField(backref='Users_id_user_set', column_name='idUser', field='idUser', model=Users)

    class Meta:
        table_name = 'SensorsData'
        indexes = (
            (('idBeehive', 'idUser', 'idFarm'), False),
            (('idSensorsData', 'idUser', 'idFarm', 'idBeehive'), True),
        )
        primary_key = CompositeKey('idBeehive', 'idFarm', 'idSensorsData', 'idUser')

class SensorsDataHasMeteoSixData(BaseModel):
    idBeehive = ForeignKeyField(column_name='idBeehive', field='idBeehive', model=Beehives)
    idFarm = ForeignKeyField(column_name='idFarm', field='idFarm', model=Farms)
    idMeteoSixData = ForeignKeyField(column_name='idMeteoSixData', field='idMeteoSixData', model=MeteoSixData)
    idSensorsData = ForeignKeyField(column_name='idSensorsData', field='idSensorsData', model=SensorsData)
    idUser = ForeignKeyField(column_name='idUser', field='idUser', model=Users)

    Beehive = ForeignKeyField(backref='Beehives_id_Beehive_set', column_name='idBeehive', field='idBeehive', model=Beehives)
    Farm = ForeignKeyField(backref='Farms_id_farm_set', column_name='idFarm', field='idFarm', model=Farms)
    MeteoSixData = ForeignKeyField(backref="MeteoSixData_id_meteo_six_data_set", column_name='idMeteoSixData', field='idMeteoSixData', model=MeteoSixData)
    SensorsData = ForeignKeyField(backref='SensorsData_id_sensors_data_set', column_name='idSensorsData', field='idSensorsData', model=SensorsData)
    User = ForeignKeyField(backref='Users_id_user_set', column_name='idUser', field='idUser', model=Users)


    class Meta:
        table_name = 'SensorsData_has_MeteoSixData'
        indexes = (
            (('idSensorsData', 'idUser', 'idFarm', 'idBeehive'), False),
            (('idSensorsData', 'idUser', 'idFarm', 'idBeehive', 'idMeteoSixData'), True),
        )
        primary_key = CompositeKey('idBeehive', 'idFarm', 'idMeteoSixData', 'idSensorsData', 'idUser')

