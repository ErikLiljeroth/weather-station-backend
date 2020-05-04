#!/usr/bin/python3

import os
import fnmatch
import time
import MySQLdb as mdb
import logging

import pigpio
import Si7021

logging.basicConfig(filename='errorPath',
  level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def insertDB(temp, humi, s_id):

	try:
		con = mdb.connect('localhost', 'sql_user', 'sql_pw', 'db_name');
		cursor = con.cursor()

		sql = "INSERT INTO tableName(temperature, humidity, sensor_id) VALUES ('%s', '%s', '%s')" % (temp, humi, s_id)
		cursor.execute(sql)
		sql = []
		con.commit()
		con.close()

	except mdb.Error as e:
		logger.error(e)


# Get readings from sensor
pi = pigpio.pi()

if not pi.connected:
    exit(0)

s = Si7021.sensor(pi)

s.set_resolution(0)
# Print the resolution.
# print("res=", s.get_resolution())

# Get the sensor-id to use in the database
id1 = s.electronic_id_1()

temp = format(s.temperature(), '.2f')
humi = format(s.humidity(), '.2f')

# Uncomment to print sensor values to log
# print("temp:", temp)
# print("humidity:", humi)

insertDB(temp, humi, id1)

s.cancel()

pi.stop()

