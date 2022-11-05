import os
import re
import datetime
import TreatmentReport
import Positions
from Iteration import iteration_generator
from Iteration import next_item


def file_walker(directory):
    """" Walk a directory and yield all files in the directory.

    Args:
        directory: - Path of files to be walked through.

    Returns:
        A generator object that will yield each file in the directory when iterated over in a loop or next
    """
    for dirName, subdirList, file_list in os.walk(directory):
        for file_name in file_list:
            yield os.path.join(dirName, file_name)


def is_cancel(line):
    """ A Cancel of the field has been requested by the therapists.

    Args:
        line: A line of text from the treatment process log.

    Returns:
        True if the line passed is a cancel request from the therapist.
        or
        None if it is not a Cancel request.
    """
    cancel_time = find_event_line('TDS=CANCEL_BEAM', line)
    beam_stop_time = find_event_line('TDS=TERMINATED', line)
    if cancel_time is not None or beam_stop_time is not None:
        if cancel_time is not None:
            return cancel_time
        elif beam_stop_time is not None:
            return beam_stop_time


def find_event_line(search_string, line):
    """ Search for a specific string to determine if a event is happening.

    Args:
        search_string:  A python regex expression to find an event in a file.
        line: A line of text from the treatment process log.

    Returns:
        A datetime object representing when the event happened or None.
    """
    if re.search(search_string, line) is not None:
        start_time = parse_time(line)
        return start_time


def parse_patient_id(line):
    """ Parse a line of text to get the patient Id. """
    if re.search('Treament Process - BeamContext: patientId=', line):
        patient_id = re.search('\\*\\*\d{6}\\*\\*', line)
        if patient_id is not None:
            return patient_id.group().strip('*')
    return None


def parse_field_name(line):
    """ Find a field name in a line of text from the pts log files.

    Args:
        search_string:  A python regex expression to find an event in a file.
        line: A line of text from the treatment proccess log.

    Returns:
        A string containing a patient id or None.
    """
    if re.search('Treament Process - BeamContext: patientId=', line):
        field_name = re.search('\\*\\*\w+:\w+\\*\\*', line)
        if field_name is not None:
            return field_name.group().strip('*')


def parse_ois_disconnect(line):
    """ Find a field name in a line of text from the pts log files.

    Args:
        search_string:  A python regex expression to find an event in a file.
        line: A line of text from the treatment process log.

    Returns:
        A string containing a patient id or None.
    """
    prepare = re.search('detect OIS disconnected', line)
    if prepare is not None:
        return True


def find_patient_stop_line(line):
    if re.search('Might be disconnected', line):
        stop_time = parse_time(line)
        return stop_time
    elif re.search('Deactivate current plan', line) is not None:
        stop_time = parse_time(line)
        return stop_time


def parse_time(line):
    """ Parse the timestamp out of a line of the pts log files.

    Args:
        line: A line of text from the treatment proccess log.

    Returns:
        A datetime object resenting the time that line happened at.
    """
    match = re.search('^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}.\d{3}', line)
    if match is not None:
        return datetime.datetime.strptime(match.group(), '%m/%d/%Y %H:%M:%S.%f')


def parse_actual_ppd_positions(treatment, line):
    if find_event_line('TreatmentPosition of existing BeamReport in database is updated to:', line):
        treatment._actual_positions = Positions.parse_line(line)


def parse_combined_log_file(log):
    """ Parse a consolidated log file for patient specific details and report in a csv file.


    Args:
        log: A consolidated log file.

    Returns:
        A list of Treatment objects.
    """

    treatments = []  # Empty list to of treatments
    treatment = TreatmentReport.TreatmentReport()
    treatment.room = 1
    last_patient = None

    # Go through each line of a treatment process log.
    with open(log, "r") as log_file:
        data = iteration_generator(log_file)
        line = next_item(data)
        while line is not None:
            # Has a patient been loaded and is this a patient being loaded line.
            # Each patient load line starts a new field.
            tmp_patient_id = parse_patient_id(line)
            if tmp_patient_id is not None:
                # The load line is for a new patient
                if treatment.patient_id != tmp_patient_id:
                    treatment.patient_id = tmp_patient_id
                    treatment.field_name = parse_field_name(line)
                    treatment.start_time = parse_time(line)
                    if last_patient is not None:
                        last_patient.stop_time = treatment.start_time
                    line = next_item(data)
                    continue

            if parse_patient_id(line) is not None:
                # The load line is for a new patient
                if treatment.patient_id != tmp_patient_id:
                    treatment.patient_id = tmp_patient_id
                    treatment.field_name = parse_field_name(line)
                    treatment.start_time = parse_time(line)
                    if last_patient is not None:
                        last_patient.stop_time = treatment.start_time
                    line = next_item(data)
                    continue

            # A new load statement has been triggered for the same patient.
            if treatment.patient_id == tmp_patient_id and tmp_patient_id is not None:
                # Read the field name
                tmp_field = parse_field_name(line)
                # The same patient and field has been reloaded, a partial.
                if tmp_field == treatment.field_name:
                    treatment.partial = treatment.partial + 1
                # Set these values whether a partial or not.
                treatment.field_name = parse_field_name(line)
                treatment.start_time = parse_time(line)

            treatment.parse_layers(data, line)

            if last_patient is not None:
                last_patient.stop_time = treatment.start_time

            # Look for the actual PPS positions
            parse_actual_ppd_positions(treatment, line)
            # Is a field disconnected and treatment finished.
            if parse_ois_disconnect(line):
                treatment.disconnects = treatment.disconnects + 1

            # A patient has been loaded, but there is no recorded start time yet.
            if treatment.patient_id and treatment.beam_start_time is None:
                # Start time will stay None until a line is found.
                treatment.beam_start_time = find_event_line('TDS=BEAM_ON', line)
                line = next_item(data)
                continue  # Very important to short circuit the for-loop, to make it faster.

            # If the above if-statements have not short-circuited the loop on the previous lines, it means
            # we can look for a stop_time value in the line, which will be None until found.
            treatment.beam_stop_time = is_cancel(line)

            # If all 3 values patientId, start_time, stop_time have been found add a treatment object list
            # of treatments.
            if treatment.treatment_found():
                treatments.append(treatment)
                last_patient = treatment
                treatment = TreatmentReport.TreatmentReport()
                treatment.room = 1
                cancel_time = None
                beam_stop_time = None
            line = next_item(data)

        return treatments


def main(directory):
    file_generator = file_walker(directory)
    patient_list = ['220533']
    with open('Data.csv','w') as f:
        # Write the column headers
        report = 'Patient, Room, Field, Load, Unload, Beam Start, ' \
                 'Beam Stop,' \
               'Prepares, SC Errors, Disconnects, Gantry, Snout, PPS X, PPS Y, PPS Z,' \
               'PPS Rotation, PPS Pitch, PPS Roll, Accessory,'
        for i in range(49):
            report = report + ' Layer {} Energy, Layer {} Dose,'.format(i + 1, i + 1)

        report = report + '\n'
        f.write(report)
        for file in file_generator:
            treatments = parse_combined_log_file(file)
            for treatment in treatments:
                if treatment.patient_id in patient_list:
                    f.write(treatment.__repr__())
                    f.write("\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('/home/pboes/src/python/p1/data/')
