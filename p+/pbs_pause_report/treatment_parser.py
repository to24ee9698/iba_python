import re
import datetime
from treatment import Treatment
from pause import Pause as Pause
from pms_positions import PmsPositions


def parse_treatment_file(log, room, compressed = True):
    """ Parse a treatment process log file with the given room number.

    Args:
        log: A pts-treat-process log file.
        room: The room number.
    Returns:
        A list of Treatment objects.
    """

    treatments = []  # Empty list to of treatments
    treatment = Treatment()
    treatment.room = room
    # Go through each line of a treatment process log.
    for raw_line in log:
        if compressed:
            line = raw_line.decode('utf-8', 'strict')  # Since the data is in a compressed file, have to decode.
            # Has a patient been loaded and is this a patient being loaded line.
            # Each patient load line starts a new field.
        else:
            line = raw_line
        if treatment.patient_id is None:
            treatment.patient_id = parse_patient_id(line)
            continue  # Very important to short circuit the for-loop, to make it faster.

        # Search for gantry angle, beam current, and range at nozzle entrance
        parse_max_current(line, treatment)
        parse_range(line, treatment)

        # A patient has been loaded, but there is no recorded start time yet.
        if treatment.patient_id and treatment.start_time is None:
            # Start time will stay None until a line is found.
            treatment.start_time = find_event_line('TDS=BEAM_ON', line)
            continue  # Very important to short circuit the for-loop, to make it faster.

        # Search for BSS Errors to add to the treatment object
        is_bss_error(line, treatment)

        # Look for line to parse PMS positions from record.

        # If the above if-statements have not short circuited the loop on the previous lines, it means
        # we can look for a stop_time value in the line, which will be None until found.
        pps_position_record(line, treatment)

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


def is_bss_error(line, treatment):
    error = re.search('ERROR', line)
    if error:
        bss = re.search("BSS cyclic check", line)
        if bss:
            error_type = re.search('GTR2-PBS.\S*', line)
            if error_type:
                label, _, value = error_type.group().partition('.')
                pause = Pause()
                pause.type = 'BSS'
                pause.data = value
                treatment.add_pause(pause)


def is_cancel(line):
    """ A Cancel of the field has been requested by the therapists.

    Args:
        line: A line of text from the treatment process log.

    Returns:
        True if the line passed is a cancel request from the therapist.
        or
        None if it is not a Cancel request.
    """
    if re.search('Canceling layer requested', line) is not None:
        return True


def find_event_line(search_string, line):
    """ Search for a specific string to determine if a event is happening.

    Args:
        search_string:  A python regex expression to find an event in a file.
        line: A line of text from the treatment proccess log.

    Returns:
        A datetime object representing when the event happened or None.
    """
    if re.search(search_string, line) is not None:
        start_time = parse_time(line)
        return start_time


def pps_position_record(line, field):
    """ Search for a specific PPS position string.

    Args:
        line: A line of text from the treatment proccess log.
        field: a treatment object.
    """
    if re.search('PpsPosition', line) is not None:
        parse_pms_positions(line, field)


def parse_pms_positions(line, field):
    positions = PmsPositions()
    current_x = re.search('X:+([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current_x:
        label, _, value = current_x.group().partition(':')
        positions._pps_x = float(value)
    current_y = re.search('Y:+([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current_y:
        label, _, value = current_y.group().partition(':')
        positions._pps_y = float(value)
    current_z = re.search('Z:+([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current_z:
        label, _, value = current_z.group().partition(':')
        positions._pps_z = float(value)
    current_rot = re.search('Rotation:+([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current_rot:
        label, _, value = current_rot.group().partition(':')
        positions._pps_rot = float(value)
    current_pitch = re.search('Pitch:+([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current_pitch:
        label, _, value = current_pitch.group().partition(':')
        positions._pps_pitch = float(value)
    current_roll = re.search('Roll:+([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current_roll:
        label, _, value = current_roll.group().partition(':')
        positions._pps_Roll = float(value)
    current_gantry = re.search('Gantry:+([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current_gantry:
        label, _, value = current_gantry.group().partition(':')
        positions._gantry_angle = float(value)
    current_snout = re.search('Snout:+([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current_snout:
        label, _, value = current_snout.group().partition(':')
        positions._snout = float(value)
    field.positions = positions


def parse_max_current(line, treatment):
    """ Find a gantry angle in a line of text from the pts log files.

    Args:
        line: A line of text from the treatment proccess log.
        treatment: The field to add the gantry angle too.

    Returns:
        A string containing a gantry angle or None.
    """
    current = re.search('bms maximal beam current: +([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if current:
        label, _, value = current.group().partition(':')
        treatment.current = float(value)


def parse_range(line, treatment):
    """ Find a gantry angle in a line of text from the pts log files.

    Args:
        line: A line of text from the treatment proccess log.
        treatment: The field to add the gantry angle too.

    Returns:
        A string containing a gantry angle or None.
    """
    max_range = re.search('bms range at nozzle entrance: +([+-]?(?:0|[1-9]\d*)(?:\.\d*))', line)
    if max_range:
        label, _, value = max_range.group().partition(':')
        treatment.max_range = float(value)


def parse_patient_id(line):
    """ Find a patient ID in a line of text from the pts log files.

    Args:
        search_string:  A python regex expression to find an event in a file.
        line: A line of text from the treatment proccess log.

    Returns:
        A string containing a patient id or None.
    """
    patient_id = re.search('patientId=\d{6}', line)
    if patient_id is not None:
        first, _, pid = patient_id.group().partition('=')
        return pid


def parse_time(line):
    """ Parse the timestamp out of a line of the pts log files.

    Args:
        line: A line of text from the treatment proccess log.

    Returns:
        A datetime object resenting the time that line happened at.
    """
    match = re.search('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', line)
    if match is not None:
        return datetime.datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S,%f')


def parse_dose(line):
    """ Find the primary dose from a line in the pbsdr.

    Args:
        line:

    Returns:
        The primary dose as a Float
    """
    dose = re.search('primaryDose:+([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))', line)
    if dose:
        label, _, value = dose.group().partition(':')
        return float(value)
