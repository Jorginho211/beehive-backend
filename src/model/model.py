from ..exts import db


class User(db.Model):
    __tablename__ = 'Users'
        
    idUser = db.Column('idUser', db.Integer, primary_key=True)
    FirstName = db.Column('FirstName', db.String(255), nullable=False)
    LastName = db.Column('LastName', db.String(255), nullable=False)

    Credential = db.relationship("Credential", uselist=False, back_populates="User")
    Farms = db.relationship("Farm", back_populates="User")

class Credential(db.Model):
    __tablename__ = 'Credentials'

    idUser = db.Column('idUser', db.Integer, db.ForeignKey(User.idUser), primary_key=True)
    Username = db.Column('Username', db.String(255), nullable=False)
    Password = db.Column('Password', db.String(255), nullable=False)
    TokenAuthentication = db.Column('TokenAuthentication', db.String(255))
    
    User = db.relationship("User", uselist=False, back_populates="Credential")


class Farm(db.Model):
    __tablename__ = 'Farms'

    idFarm = db.Column('idFarm', db.Integer, primary_key=True)
    idUser = db.Column('idUser', db.Integer, db.ForeignKey(User.idUser), primary_key=True)
    Name = db.Column('Name', db.String(255), nullable=False)

    User = db.relationship("User", uselist=False, back_populates="Farms")
    Device = db.relationship("Device", uselist=False, back_populates="Farm")
    Beehives = db.relationship("Beehive", back_populates="Farm")

class Device(db.Model):
    __tablename__ = 'Devices'

    idUser = db.Column('idUser', db.Integer, db.ForeignKey(User.idUser), primary_key=True)
    idFarm = db.Column('idFarm', db.Integer, db.ForeignKey(Farm.idFarm), primary_key=True)
    Identifier = db.Column('Identifier', db.String(128), unique = True)
    ApiKey = db.Column('ApiKey', db.String(128))

    Farm = db.relationship("Farm", uselist=False, back_populates="Device")


class Beehive(db.Model):
    __tablename__ = 'Beehives'

    idBeehive = db.Column('idBeehive', db.Integer, primary_key=True)
    idFarm = db.Column('idFarm', db.Integer, db.ForeignKey(Farm.idFarm), primary_key=True)
    idUser = db.Column('idUser', db.Integer, db.ForeignKey(User.idUser), primary_key=True)
    Name = db.Column('Name', db.String(255), nullable=False)

    Farm = db.relationship("Farm", uselist=False, back_populates="Beehives")
    SensorsData = db.relationship("SensorsData", back_populates="Beehive")

    def __init__(self, idBeehive, idFarm, idUser):
        self.idBeehive = idBeehive
        self.idFarm = idFarm
        self.idUser = idUser
        self.Name = "Beehive number: " + str(idBeehive)


class SensorsData(db.Model):
    __tablename__ = 'SensorsData'

    idSensorsData = db.Column('idSensorsData', db.BigInteger, primary_key=True)
    idBeehive = db.Column('idBeehive', db.Integer, db.ForeignKey(Beehive.idBeehive), primary_key=True)
    idFarm = db.Column('idFarm', db.Integer, db.ForeignKey(Farm.idFarm), primary_key=True)
    idUser = db.Column('idUser', db.Integer, db.ForeignKey(User.idUser), primary_key=True)
    Date = db.Column('Date', db.DateTime, nullable=False)
    Weight = db.Column('Weight', db.Integer)

    Beehive = db.relationship("Beehive", uselist=False, back_populates="SensorsData")

    def __init__(self, idSensorsData, idBeehive, idFarm, idUser, weight):
        self.idSensorsData = idSensorsData
        self.idBeehive = idBeehive
        self.idFarm = idFarm
        self.idUser = idUser
        self.Weight = weight

    
