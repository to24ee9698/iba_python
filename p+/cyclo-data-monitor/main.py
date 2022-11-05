#!/bin/python3
# Data monitor collector for T06

import snap7
from snap7 import util
from snap7.exceptions import Snap7Exception
import logging
import psycopg2
import psycopg2.extras
import datetime
import smtplib
from email.mime.text import MIMEText
import time

PLC_RACK = 0
PLC_SLOT = 4
PLC_ADDRESS = '10.1.40.41'
MONITORING_DB = 82
DB_CONN_SETTINGS = "dbname=acu user=postgres password=postgres host=10.1.40.221 port=5432"
SMTP_SERVER = '10.1.40.13'
SENDER = 'ACU Monitor'
NOTIF_EMAIL = 'croll@mcrs3.fpti.org'
DATA_BLOCKS_SQL = "SELECT DISTINCT(location_db) AS db, MAX(location_address) AS max_address, location_data_type " \
                  "AS data_type FROM location GROUP BY location_db, location_data_type;"
LOCATIONS_SQL = "SELECT location_id, location_description AS description, location_db AS db, " \
                "location_address AS address, location_data_type AS data_type, location_bit AS bit FROM location;"


def read_real(db, address):
    data = util.get_real(db, address)
    return data


def read_int(db, address):
    data = util.get_int(db, address)
    return data


def read_bool(db, address, bit):
    data = util.get_bool(db, address, bit)
    return data


def get_size(address, data_type):
    if data_type == 'real':
        return address + 4
    if data_type == 'int':
        return address + 2
    if data_type == 'bool':
        return address + 1


def collect(data_blocks, locations):
    conn = None
    plc = None
    try:
        # Connect to timescaledb database
        conn = psycopg2.connect(DB_CONN_SETTINGS)
        cur = conn.cursor()

        # Connect to plc
        plc = snap7.client.Client()
        connection_time = datetime.datetime.now()
        plc.connect(PLC_ADDRESS, PLC_RACK, PLC_SLOT)

        plc_data = {}
        for data_block in data_blocks:
            size = get_size(int(data_block['max_address']), data_block['data_type'])
            plc_data[data_block['db']] = plc.db_read(int(data_block['db']), 0, size)

        # Disconnect from plc
        plc.disconnect()
        disconnect_time = datetime.datetime.now()
        connected_time = (disconnect_time - connection_time)
        logging.log(logging.DEBUG, "time spent connected to plc: {} s".format(connected_time.total_seconds()))

        # Initialize data & time
        data = {}
        current_time = datetime.datetime.utcnow()

        for location in locations:
            location_id = location['location_id']
            description = location['description']
            db = int(location['db'])
            address = int(location['address'])
            data_type = location['data_type']
            data[description] = {}
            data[description]['db'] = db
            if data_type == 'real':
                value = read_real(plc_data[db], address)
                data[description]['value'] = value
                if db == MONITORING_DB:
                    cur.execute("INSERT INTO location_data (location_data_id, location_data_time, location_data_value) "
                                "VALUES (%s, %s, %s)", (location_id, current_time, value))
            elif data_type == 'int':
                data[description]['value'] = read_int(plc_data[db], address)
            elif data_type == 'bool':
                bit = int(location['bit'])
                data[description]['value'] = read_bool(plc_data[db], address, bit)
            else:
                raise ValueError("Data type is not valid. {}".format(data_type))

        # Commit query to database
        conn.commit()
        cur.close()
        return data

    except (Snap7Exception, psycopg2.DatabaseError, ValueError, Exception) as e:
        print(e)

    finally:
        if conn is not None:
            conn.close()
            logging.log(logging.DEBUG, 'closing timescaledb connection')


def read_database(sql):
    conn = None
    try:
        logging.log(logging.DEBUG, 'connecting to the timescaledb database')
        conn = psycopg2.connect("dbname=acu user=postgres password=postgres host=10.1.40.221 port=5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(sql)
        query_result = cur.fetchall()
        cur.close()

        return query_result

    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

    finally:
        if conn is not None:
            conn.close()
            logging.log(logging.DEBUG, 'closing timescaledb connection')


def send_mail(text):
    msg = MIMEText(text)
    msg['Subject'] = 'ACU data change detected!'
    msg['From'] = SENDER
    msg['To'] = NOTIF_EMAIL
    s = smtplib.SMTP(SMTP_SERVER)
    s.sendmail(SENDER, NOTIF_EMAIL, msg.as_string())
    s.quit()


def compare_data(new_values, old_values):
    changes = ''
    for key in new_values:
        if new_values[key]['db'] != MONITORING_DB:
            if new_values[key]['value'] != old_values[key]['value']:
                change = "{} has changed from {} to {}\n".format(key, old_values[key]['value'],
                                                                 new_values[key]['value'])
                changes += change
                logging.log(logging.WARN, change)
                old_values[key] = new_values[key]
    return changes


def main():

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    # Read and create list to store the device data.
    logging.log(logging.DEBUG, "reading location and data block information from the database")
    data_blocks = read_database(DATA_BLOCKS_SQL)
    locations = read_database(LOCATIONS_SQL)
    logging.log(logging.DEBUG, data_blocks)
    logging.log(logging.DEBUG, locations)

    # Read the initial set of data during startup
    logging.log(logging.DEBUG, "reading the plc data")
    locations_data = collect(data_blocks, locations)
    logging.log(logging.INFO, locations_data)

    while True:
        time.sleep(60)
        # Read and create list to store the device data.
        logging.log(logging.DEBUG, "reading location and data block information from the database")
        data_blocks = read_database(DATA_BLOCKS_SQL)
        locations = read_database(LOCATIONS_SQL)
        logging.log(logging.DEBUG, data_blocks)
        logging.log(logging.DEBUG, locations)

        # Read the initial set of data during startup
        logging.log(logging.DEBUG, "reading the plc data")
        tmp_locations_data = collect(data_blocks, locations)
        logging.log(logging.INFO, locations_data)

        # Check for any changes to calibration data
        changes = compare_data(tmp_locations_data, locations_data)
        if changes:
            send_mail(changes)
        else:
            logging.log(logging.DEBUG, "no calibration changes detected")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
