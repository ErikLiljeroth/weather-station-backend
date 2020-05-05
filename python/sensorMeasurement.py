#!/usr/bin/python3

import os
from datetime import datetime
import fnmatch
import time
import mysql.connector as mdb
import logging

import pigpio
import Si7021

from dotenv import load_dotenv
load_dotenv()

# dotenv variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_INSERT_TABLE = os.getenv('DB_INSERT_TABLE')
LOGGER_PATH_AND_FILENAME = os.getenv('LOGGER_PATH_AND_FILENAME')

# Setup error logger
logging.basicConfig(filename=LOGGER_PATH_AND_FILENAME,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


def insertDB(temp, humi, s_id):

    try:
        con = mdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            db=DB_DATABASE
        )
        cursor = con.cursor()

        sql = f'INSERT INTO {DB_INSERT_TABLE} (dtg, temperature, humidity, sensor_id) VALUES (%(dtg)s, %(temp)s, %(humi)s, %(s_id)s)'

        now = datetime.now()
        formatted_now = now.strftime('%Y-%m-%d %H:%M:00')

        dataToInsert = {
            'dtg': formatted_now,
            'temp': temp,
            'humi': humi,
            's_id': s_id
        }

        cursor.execute(sql, dataToInsert)

        sql = []
        con.commit()
        cursor.close()
        con.close()

    except mdb.Error as e:
        logger.error(e)


def main():
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

    insertDB(temp, humi, id1)

    s.cancel()
    pi.stop()


if __name__ == "__main__":
    main()
