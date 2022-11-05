#!/bin/python3
# Data monitor collector for T06

import logging
import smtplib
from email.mime.text import MIMEText
import iba_file_stucture
import datetime

SMTP_SERVER = '10.1.40.13'
SENDER = 'Abnormal Beam Detection'
NOTIF_EMAIL = 'pjb@mcrs3.fpti.org'
MOST_RECENT_CHECK = None

DIRECTORY = '/TCS/runtimeStore/log/output'

def send_mail(text):
    msg = MIMEText(text)
    msg['Subject'] = 'Abnormal Beam Detected'
    msg['From'] = SENDER
    msg['To'] = NOTIF_EMAIL
    s = smtplib.SMTP(SMTP_SERVER)
    s.sendmail(SENDER, NOTIF_EMAIL, msg.as_string())
    s.quit()


def parse_treatment_file(log, room):
    """ Parse a treatment process log file with the given room number.

    Args:
        log: A pts-treat-process log file.

    Returns:
        A list of Treatment objects.
    """

    treatments = []  # Empty list to of treatments
    treatment = Treatment()
    treatment.room = room
    # Go through each line of a treatment process log.
    for rawline in log:
        line = rawline.decode('utf-8', 'strict')  # Since the data is in a compressed file, have to decode.
        # Has a patient been loaded and is this a patient being loaded line.
        # Each patient load line starts a new field.
        if treatment.patient_id is None:
            treatment.patient_id = parse_patient_id(line)
            continue  # Very important to short circuit the for-loop, to make it faster.

        # A patient has been loaded, but there is no recorded start time yet.
        if treatment.patient_id and treatment.start_time is None:
            # Start time will stay None until a line is found.
            treatment.start_time = find_event_line('TDS=BEAM_ON', line)
            continue  # Very important to short circuit the for-loop, to make it faster.

        # If the above if-statements have not short circuited the loop on the previous lines, it means
        # we can look for a stop_time value in the line, which will be None until found.
        treatment.stop_time = find_event_line('TDS=TERMINATED', line)
        # if is_cancel(line):
        #    treatment = Treatment()
        #    treatment.room = room

        # If all 3 values patientId, start_time, stop_time have been found add a treatment object list of treatments.
        if treatment.treatment_found():
            treatments.append(treatment)
            treatment = Treatment()
            treatment.room = room
            return treatments


def main():

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.log(logging.DEBUG, "Checking for Abnormal Beams during Patient Treatment")
    # Check for any changes to calibration data
    my_file = iba_file_stucture.iba_files.find_latest_log_file(DIRECTORY, 'pts-treat', 2)
    if my_file is not None:



#    send_mail(changes)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

