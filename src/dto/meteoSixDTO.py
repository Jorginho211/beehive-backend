class MeteoSixDTO():
    def __init__(self, latitude, longitude, timeInstant, temperature, precipitationAmount, relativeHumidity, cloudAreaFraction):
        self.latitude = latitude
        self.longitude = longitude
        self.TimeInstant = timeInstant
        self.Temperature = temperature
        self.PrecipitationAmount = precipitationAmount
        self.RelativeHumidity = relativeHumidity
        self.CloudAreaFraction = cloudAreaFraction