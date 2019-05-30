from flask import Flask, g #flask
from peewee import *

app = Flask(__name__)
db = MySQLDatabase('beehive', **{'charset': 'utf8', 'use_unicode': True, 'user': 'root', 'password': 'root'})