""" A module to find and parse TCS Treatment Process logs."""

import os
import re
import datetime
import Patient


def find_treatment_process(tarfileobject, patient_id, room, pl):
    treatment_process = re.compile('^pts-treat-proc-{}'.format(room))
    for item in tarfileobject.getmembers():
        if re.search(treatment_process, item.name) is not None:
            file =  tarfileobject.extractfile(item)
            parse_file(file, patient_id, pl)


def parse_file(file, patient_id, pl):
    start_time = None
    stop_time = None
    lines = []

    for rawline in file:
        line = rawline.decode('utf-8','strict')
        if start_time is None:
            start_time = find_patient_start_line(patient_id, line)
        if start_time != None:
            if stop_time is None:
                stop_time = find_patient_stop_line(patient_id, line)
                date = parse_time(line)
                if date is not None:
                    last_date = date
                    lines.append(parse_data_from_line(date, line))
        if start_time is not None and stop_time is not None:           
            pl.append([Patient.Patient(patient_id, start_time, stop_time), lines])
            start_time = None
            stop_time = None
            lines = []
    # This code should only run if the patient was on the table when the system was restarted
    if start_time is not None and stop_time is None:
        pl.append([Patient.Patient(patient_id, start_time, last_date), lines])
            

def find_patient_start_line(patient, line):
    if re.search('patientId=\d{6}', line) is not None:
        current_patient_id = parse_patient_id(line)
        if current_patient_id == patient:
            start_time = parse_time(line)
            return start_time


def find_patient_stop_line(patient, line):
    if re.search('patientId=\d{6}', line) is not None:
        current_patient_id = parse_patient_id(line)
        if current_patient_id != patient:
            stop_time = parse_time(line)
            return stop_time


def parse_patient_id(line):
    """ Parse a line of text to get the patient Id. """
    patient_id = re.search('patientId=\d{6}', line)
    if patient_id is not None:
        first, _, pid = patient_id.group().partition('=')
        return pid
    return None


def parse_time(str):
    """ Parse a line of text to get the patient Id. """
    time = re.search('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', str)
    if time is not None:
        start_time = datetime.datetime.strptime(time.group(), '%Y-%m-%d %H:%M:%S,%f')
        return start_time


def parse_data_from_line(time, line):
    try:
        index = line.find(') - ')
        data = line[index+3:].lstrip()
        if time is not None:
            timestring = time.strftime("%m/%d/%Y %H:%M:%S.%f")
            newlist = [timestring, 'Treament Process', data]
            return newlist
    except IndexError as e:
        pass