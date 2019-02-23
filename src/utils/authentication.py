from functools import wraps
from flask import g, request, redirect, url_for
from .util import custom_response
from ..model.model import *

def requires_authentication_device(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        deviceId = request.headers.get("device_id")
        apiKey = request.headers.get("api_key")

        if not deviceId or not apiKey:
            return custom_response({ msg: "device_id or api_key headers not found"}, 401)

        device = Device.query.filter(Device.Identifier == deviceId, Device.ApiKey == apiKey).first()

        if not device:
            return custom_response({ 'msg': 'Not valid device or api key'}, 401)

        return f(*args, **kwargs)
    return wrap
        
