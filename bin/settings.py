import json

import psutil
from motor.motor_asyncio import AsyncIOMotorClient

import main

#cfg = configparser.ConfigParser(inline_comment_prefixes=["::"])
#cfg.read("../config.ini")
# todo integrate actual settings into everything
cfg = json.load(open(f"{main.basepath}/config.json"))

class Motor(object):
	def uri():
		return cfg["motor"]["URI"]

	def dbname():
		return cfg["motor"]["db_name"]

	client = AsyncIOMotorClient(uri())

class Output:
	interval = 0.5 #cfg.getfloat("output", "interval")

class CPU(object):
	def count():
		return psutil.cpu_count()

	def count_logical():
		return psutil.cpu_count(logical=True)

