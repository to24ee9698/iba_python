#  Data monitor collector for T06
import snap7
from snap7 import util
from snap7.exceptions import Snap7Exception
import time
import logging
from numpy import isclose



def read_boolean_configuration(file):
    dict_temp = {}
    with open(file, 'r') as cfg:
        for line in cfg:
            item = line.split(',')
            if item[0][0] == '#':
                continue
            else:
                dict_temp[item[0]] = (item[1], item[2], item[3])
    return dict_temp


def read_non_boolean_configuration(file):
    dict_temp = {}
    with open(file, 'r') as cfg:
        for line in cfg:
            item = line.split(',')
            if item[0][0] == '#':
                continue
            else:
                dict_temp[item[0]] = (item[1], item[2])
    return dict_temp


def read_plc_real_data(plc, reals):
    data = {}
    for key in reals.keys():
        db = int(reals[key][0])
        address = int(reals[key][1])
        data[key] = plc.db_read(db, address, 4)
        data[key] = snap7.util.get_real(data[key], 0)
    return data


def read_plc_numeric_data(plc, numeric):
    data = {}
    for key in numeric.keys():
        db = int(numeric[key][0])
        address = int(numeric[key][1])
        data[key] = plc.db_read(db, address, 2)
        data[key] = snap7.util.get_int(data[key], 0)
    return data


def read_plc_boolean_data(plc, booleans):
    data = {}
    for key in booleans.keys():
        db = int(booleans[key][0])
        address = int(booleans[key][1])
        bit = int(booleans[key][2])
        data[key] = plc.db_read(db, address, 1)
        data[key] = snap7.util.get_bool(data[key], 0, bit)
    return data


""" Takes in a dictionary and returns a dictionary of the values read from the PLC. """


def collect(locations, data_type):
    try:
        client = snap7.client.Client()
        client.connect('10.1.40.41', 0, 4)
        if data_type == 'real':
            output = read_plc_real_data(client, locations)
        elif data_type == 'numeric':
            output = read_plc_numeric_data(client, locations)
        elif data_type == 'boolean':
            output = read_plc_boolean_data(client, locations)
        else:
            raise ValueError("Data type is not valid. {}".format(data_type))
        return output

    except (Snap7Exception, ValueError) as e:
        print(e)


def compare_real_data(new_values, old_values, tolerance):
    for key in new_values:
        if not isclose(new_values[key],old_values[key], tolerance):
            logging.log(logging.WARN, "Value {} has changed from {} to {}".format(key, old_values[key],
                                                                                  new_values[key]))
            old_values[key] = new_values[key]


def compare_bool_data(new_values, old_values):
    for key in new_values:
        if new_values[key] != old_values[key]:
            logging.log(logging.WARN, "Value {} has changed from {} to {}".format(key, old_values[key],
                                                                                  new_values[key]))
            old_values[key] = new_values[key]


def main():

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    # Read and create dictionaries to store the configuration data.
    logging.log(logging.INFO, "Reading the configuration files")
    calibrations = read_non_boolean_configuration('acu_monitor_calibration_data.csv')
    values = read_non_boolean_configuration('acu_monitor_float_data.csv')
    numerics = read_non_boolean_configuration('acu_monitor_numeric_data.csv')
    booleans = read_boolean_configuration('acu_monitor_boolean_data.csv')

    # Read the initial set of data during startup
    logging.log(logging.INFO, "Reading the configuration data for first time.")
    configuration_data = collect(calibrations, 'real')
    logging.log(logging.INFO, configuration_data)
    logging.log(logging.INFO, "Reading the real values for first time.")
    values_data = collect(values, 'real')
    logging.log(logging.INFO, values_data)
    logging.log(logging.INFO, "Reading the numerical data for first time.")
    numeric_data = collect(numerics, 'numeric')
    logging.log(logging.INFO, numeric_data)
    logging.log(logging.INFO, "Reading the boolean data for first time.")
    boolean_data = collect(booleans, 'boolean')
    logging.log(logging.INFO, boolean_data)

    # while True:
    #     time.sleep(120)
    #     tmp_configuration_data = collect(calibrations, 'real')
    #     tmp_values_data = collect(values, 'real')
    #     tmp_numeric_data = collect(numerics, 'numeric')
    #     tmp_boolean_data = collect(booleans, 'boolean')
    #     compare_real_data(tmp_configuration_data, configuration_data, 0.100)
    #     compare_real_data(tmp_values_data, values_data, 0.100)
    #     compare_real_data(tmp_numeric_data, numeric_data, 0.100)
    #     compare_bool_data(tmp_boolean_data, boolean_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
