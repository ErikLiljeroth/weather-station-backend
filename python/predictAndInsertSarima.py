import numpy as np
import pandas as pd
from scipy import stats

import os
import logging
import mysql.connector as mdb
import requests
from datetime import datetime

# Sarimax model
from statsmodels.tsa.statespace.sarimax import SARIMAX

# For ACF and PACF
import statsmodels.api as sm

from dotenv import load_dotenv
load_dotenv()

# dotenv variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_DATABASE = os.getenv('DB_DATABASE')
# Tables
DB_FORECAST_TEMP_TABLE = os.getenv('DB_FORECAST_TEMP_TABLE')
DB_MEASUREMENT_TABLE = os.getenv('DB_MEASUREMENT_TABLE')
# Logger
FORECAST_LOGGER_FILEPATH = os.getenv('FORECAST_LOGGER_FILEPATH')

# Setup error logger
logging.basicConfig(filename=FORECAST_LOGGER_FILEPATH,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

def get_fresh_data_from_server_over_http(noRecords = 480):
    URL = 'http://www.erikliljeroth.se/api/data'
    r = requests.get(url=URL)
    data = r.json()
    df = pd.DataFrame(data)
    return df[-noRecords:]

class HandleDB():

    def __init__(self):
        try:
            self.con = mdb.connect(
                host=DB_HOST,
                user=DB_USER,
                passwd=DB_PASSWORD,
                port=DB_PORT,
                db=DB_DATABASE
            )

        except mdb.Error as e:
            logger.error(e)

    def _insert_entries(self, list_of_entries):
        try:
            cursor = self.con.cursor()

            # reorder incoming list (dtg, horizon, pred) => (horizon, dtg, pred)
            list_of_insert_entries = [(e[1], e[0], e[2]) for e in list_of_entries]

            for e in list_of_insert_entries:
                horizon = e[0]
                sql_insert = sql_insert = f'INSERT INTO {DB_FORECAST_TEMP_TABLE} (dtg, {horizon}) VALUES (%s, %s)'
                cursor.execute(sql_insert, (e[1], e[2]))

            self.con.commit()
            cursor.close()
            sql = []
        except Exception as e:
            logger.error(e)

    def _update_entries(self, list_of_entries):
        try:
            cursor = self.con.cursor()

            # items in entries are are in wrong order, change from (dtg, horizon, pred) => (horizon, pred, dtg)
            list_of_update_entries = [(e[1], e[2], e[0]) for e in list_of_entries]
            
            #print(f'update_entries: {list_of_update_entries}')

            for e in list_of_update_entries:
                horizon = e[0]
                sql_update = f'UPDATE {DB_FORECAST_TEMP_TABLE} SET {horizon} = %s WHERE dtg = %s'
                cursor.execute(sql_update, (e[1], e[2]))

            self.con.commit()
            cursor.close()
            sql = []
        except Exception as e:
            logger.error(e)

    def insert_new_predictions_in_DB(self, list_of_entries):
        # Initialization
        entriesToUpdate = []
        entriesToInsert = []

        # Current records in prediction table (dtg's only)
        old_dtgs = self._find_latest_db_prediction_dtgs()
        old_dtgs = [str(i) for i in old_dtgs]

        # Find out which rows to update and which rows to insert
        for idx, entry in enumerate(list_of_entries):
            entry_dtg_str = str(entry[0])
            if entry_dtg_str in old_dtgs:
                entriesToUpdate.append(entry)
            else:
                entriesToInsert.append(entry)

        # insert and update
        self._insert_entries(entriesToInsert)
        self._update_entries(entriesToUpdate)

    def _find_latest_db_prediction_dtgs(self, noRecords=24):
        cursor = self.con.cursor()
        sql = f'SELECT * FROM (SELECT * FROM {DB_FORECAST_TEMP_TABLE} ORDER BY dtg DESC LIMIT {str(noRecords)}) as R ORDER by dtg ASC'
        cursor.execute(sql)
        records = cursor.fetchall()  # Returns list of tuples
        if len(records) > 0:
            return [r[0].strftime('%Y-%m-%d %H:%M:00') for r in records]
        else:
            return []

    def find_latest_db_measurement_dtg(self):
        cursor = self.con.cursor()
        sql = f'SELECT * FROM (SELECT * FROM {DB_MEASUREMENT_TABLE} ORDER BY dtg DESC LIMIT 1) as R ORDER by dtg ASC'
        cursor.execute(sql)
        records = cursor.fetchall()  # Returns list of tuples
        if len(records) > 0:
            return pd.Timestamp(records[0][0].strftime('%Y-%m-%d %H:%M:00'))
        else:
            return None
        

    def fetch_modelling_data_and_latest_timestamp(self, noRecords = 480):
        cursor = self.con.cursor()
        sql = f'SELECT * FROM (SELECT * FROM {DB_MEASUREMENT_TABLE} ORDER BY dtg DESC LIMIT {str(noRecords)}) as R ORDER by dtg ASC'
        cursor.execute(sql)
        records = cursor.fetchall()

        tempdata = [r[1] for r in records]
        humidata = [r[2] for r in records]
        latest_timestamp = pd.Timestamp(records[-1][0].strftime('%Y-%m-%d %H:%M:00'))

        return latest_timestamp, tempdata, humidata

    def close_connection(self):
        self.con.close()
        print('connection to database closed, bye.')

class HandlePredictions():

    def __init__(self, train_data):
        # Current best model:	SARIMAX([1, 8, 48], 1, [48])x(0, 1, [], 48)
        ar = [1, 8, 48]
        ma = [48]
        self.model = SARIMAX(endog=train_data, order=(ar, 1, ma), seasonal_order=(0, 1, 0, 48), simple_differencing=True)
        self.model = self.model.fit(disp=True, low_memory=True, maxiter=8) #start_params = [0.3, -0.04, 0.1, -0.9, 0.6])

    def predict(self, horizon = 12):
        forecast = self.model.get_forecast(steps=12)
        forecast = forecast.summary_frame(alpha=0.05)
        predictions = forecast['mean'].values
        return predictions


def main():

    #df = get_fresh_data_from_server_over_http(noRecords=480)

    db = HandleDB()

    latest_timestamp, tempdata, _ = db.fetch_modelling_data_and_latest_timestamp(noRecords=480)

    #temp = df.temperature.values
    temp = tempdata


    #latest_timestamp = df.dtg.values
    #latest_timestamp = latest_timestamp[-1]
    #latest_timestamp = pd.Timestamp(latest_timestamp)
    latest_timestamp.replace(minute = 0)

    model = HandlePredictions(temp)
    preds = model.predict()
    preds = [float(p) for p in preds]

    #latest_timestamp, tempdata, _ = db.fetch_modelling_data_and_latest_timestamp(noRecords=3)

    futureTimestamps = [str(latest_timestamp + i * pd.Timedelta('30min')) for i in range(1, 13)]
    predictionHorizon = [f'step{i}' for i in range(1, 13)]

    dataToInsert = list(zip(futureTimestamps, predictionHorizon, preds))


    db.insert_new_predictions_in_DB(dataToInsert)

    db.close_connection()


if __name__ == "__main__":
    main()