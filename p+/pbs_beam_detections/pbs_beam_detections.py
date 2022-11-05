#!/usr/bin/env python3

""" A module to parse the OUTPUT.tar.gz file generated by the TCS software system to look for
  Abnormal Beam conditions between when TDS=BEAM_ON and TDS=TERMINATE

  Usage:  pbs_beam_detections.py /directory_to_OUTPUT.tar.gz files.
    ** If on Linux / Unix make sure to chmod +x the script before trying this.
"""
import os
import re
import tarfile
import datetime


class Treatment(object):
    """ A python class to objectify a patient treatment capturing the patient id, room, start time,
        and stop time of the field. """
    def __init__(self):
        """ Initialization of the Treatment objects. """
        self._room = None
        self._start_time = None
        self._stop_time = None
        self._patient_id = None

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        self._patient_id = value

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, value):
        self._room = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self,value):
        self._start_time = value

    @property
    def stop_time(self):
        return self._stop_time

    @stop_time.setter
    def stop_time(self,value):
        self._stop_time = value

    def treatment_found(self):
        """ Treatment found is if all properties of the class have been defined.
            Args:
                self - the current object
            Returns:
                True if the treatment has all properties defined or False if not.
        """
        if self._patient_id and self._start_time and self._stop_time and self._room:
            return True
    
    def __repr__(self):
        return 'Patient: {}\tRoom: {}\tStart: {}\tStop: {}\n'.format(self.patient_id,
                                                                        self.room,
                                                                        self.start_time,
                                                                        self.stop_time)


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


def find_tar_gz_files(directory):
    """ Walks through a directory and finds all tarballs  *.tar.gz.

    Args:
        directory: - Path of files to be searched for tarballs.

    Returns:
        A generator object that will yield each tarball in a given directory structure.
    """
    normal_record = re.compile('tar.gz$')
    file_walk = file_walker(directory)
    for file in file_walk:
        if re.search(normal_record, file) is not None:
            yield file


def find_tar_files_in_tarball(tarball):
    """ Walks through a tarball file and finds all tar files inside.

    Args:
        tarball: - A tar file

    Returns:
        A generator object that will yield each file in a given tarball.
    """
    tar_files = re.compile('.tar$')
    with tarfile.open(tarball, "r") as f:
        for item in f.getmembers():
            if re.search(tar_files, item.name) is not None:
                file = f.extractfile(item)
                yield file


def find_process_log_file(tarfileobject, search_string):
    """ Goes through list of files in a tar file and finds a process log file with a name
    that matches the search_string pattern.
    
    Args:
        tarfileobject:  A tarfileobject that contains treatment process logs.
         
    Returns:
        A file of the given search string found in a tar file.
    """
    treatment_process = re.compile(search_string)
    for item in tarfileobject.getmembers():
        if re.search(treatment_process, item.name) is not None:
            log = tarfileobject.extractfile(item)
            yield log 


def parse_treatment_file(log, room):
    """ Parse a treatment process log file with the given room number.
    
    Args:
        log: A pts-treat-process log file.

    Returns:
        A list of Treatment objects.
    """

    treatments = []  # Empty list to of treatments
    treatment =  Treatment()
    treatment.room = room
    # Go through each line of a treatment process log. 
    for rawline in log:
        line = rawline.decode('utf-8','strict') # Since the data is in a compressed file, have to decode.
        # Has a patient been loaded and is this a patient being loaded line.
        # Each patient load line starts a new field.
        if treatment.patient_id is None:
            treatment.patient_id = parse_patient_id(line)
            continue  # Very important to short circuit the for-loop, to make it faster.

        # A patient has been loaded, but there is no recorded start time yet. 
        if treatment.patient_id and treatment.start_time is None:
            # Start time will stay None until a line is found.
            treatment.start_time = find_event_line('TDS=BEAM_ON', line)
            continue # Very important to short circuit the for-loop, to make it faster.

        # If the above if-statements have not short circuited the loop on the previous lines, it means 
        # we can look for a stop_time value in the line, which will be None until found.
        treatment.stop_time = find_event_line('TDS=TERMINATED', line)
        #if is_cancel(line):
        #    treatment = Treatment()
        #    treatment.room = room

        # If all 3 values patientId, start_time, stop_time have been found add a treatment object list of treatments. 
        if treatment.treatment_found():
            treatments.append(treatment)
            treatment = Treatment()
            treatment.room = room
    return treatments


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


def is_rpc_update(line):
    """ Determine if the line in the file is an updateRpc Dose call.
    
    Args:
        line:  
         
    Returns:
        True if the line contains the RpcUpdate Dose call or None.
    """
    if re.search('beamlineId:1, mapId:', line) is not None:
        return True


def iteration_generator(collection):
    """ Create a generator object to iterate over a collection.
    
    Args:
        collection:  Any collection object that can be iterated over.   
         
    Returns:
        A generator object that can be used to control iteration of a series of objects in a collection.
    """
    for item in collection:
        yield item


def next_item(generator):
    """ Get the next item in a generator, while surpressing the StopIteration Error and return None instead.
    
    Args:
        generator:  A generator object that will yield the objects of a collection.   
         
    Returns:
        Successive items in the list of the collection. None if the collection has completed yielding items.
    """
    try:
        item = next(generator)
        return item
    except StopIteration as e:
        return None


def parse_beam_error(line):
    """ Dose the line contain the word Beam and SGCU

    Args:
        line:

    Returns:
        The primary dose as a Float
    """
    beam = re.search('_BeamOnInError', line)
    if beam:
        return True


def parse_scanning_controller_time(line):
    """ Parse a scanning controller line of text to get the date / time.
        scanning controller logs do not print time that same as other PTS logs"""
    time = re.search('\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}:\d{3}', line)
    if time is not None:
        start_time = datetime.datetime.strptime(time.group(), '%d.%m.%Y %H:%M:%S:%f')
        return start_time
    else:
        return None


def parse_scanning_controller_file(file, fields):
    """ Parse a scanning controller file that may or may not contain AbnormalBeamDetections or
    BeamOnInErrorThreshold errors.

    Args:
        file:  A scanning controller log file
        fields: A list of treatment objects.

    Returns:
        None , but prints out a Common separated list of fields and Beam Messages received during a field.
    """
    with open('history/BeamDetections.txt', 'a') as output:
        field_generator = iteration_generator(fields)
        field = next_item(field_generator)
        if field is None:
            return
        output.write(field.__repr__())

        last_time = datetime.datetime.now()
        for raw_line in file:
            line = raw_line.decode('utf-8', 'strict')
            line_time = parse_scanning_controller_time(line)
            if line_time is not None:
                last_time = line_time
            if line_time is None and field.start_time < last_time < field.stop_time: # Signal that an Error has occurred.
                if parse_beam_error(line):
                    output.write('{}\n'.format(line))
            if last_time > field.stop_time:
                field = next_item(field_generator)
                if field is None:
                    return
                output.write(field.__repr__())


def main(directory):
    """ Main program flow that will take a path to the directory containing OUTPUT.tar.gz files
    and parse them. First by finding the time when each treatment started and the time the first layer
    is started for a field. It then calculates the dose delivered in this time and outputs it to a csv file.

    Args:
        directory: Path that contains all Output.tar.gz files for a site.

    Returns:
        None
    """
    treatments = []
    room = 2
    for zipped_tarballs in find_tar_gz_files(directory):
        for tarball in find_tar_files_in_tarball(zipped_tarballs):
            with tarfile.open(fileobj=tarball) as f:  # This loops through each tar.gz file
                # Parse each treatment process room log and add to treatments
                treatment_logs = iteration_generator(find_process_log_file(f, '^pts-treat-proc-{}'.format(room)))
                for log in treatment_logs: # We must parse all treatment logs found, in case of room restarts.
                    treatments.extend(parse_treatment_file(log, room))  # Use extend on list.
                # Take all treatments found and find the dose for each from PBSDR log
                scanning_controller_logs = find_process_log_file(f,'^pts-scanning')
                for log in scanning_controller_logs:  # We must parse all scanning controller logs found
                    parse_scanning_controller_file(log, treatments)
                # Reset the treatments after each tar file is parsed.
                treatments = [] 


#if __name__ == '__main__':
#    main(sys.argv[1])

main('/home/pboes/data/p+/Output/')
