import re
from pause import Pause as Pause
import datetime


def parse_scanning_controller_file(file, fields):
    """ Parse a scanning controller file that may or may not contain Pauses

    Args:
        file:  A scanning controller log file
        fields: A list of treatment objects.

    Returns:
        None , but prints out a Common separated list of fields and Beam Messages received during a field.
    """
    error = False
    error_lines = []
    last_time = datetime.datetime.now()
    field_generator = iteration_generator(fields)
    field = next_item(field_generator)
    if field is None:
        return

    for raw_line in file:
        line = raw_line.decode('utf-8', 'strict')
        line_time = parse_scanning_controller_time(line)
        if line_time is not None and not error:
            last_time = line_time
            if parse_sc_error(line) and field.start_time < last_time < field.stop_time:
                error = True
                pbs_pause = Pause()
            if last_time > field.stop_time:
                field = next_item(field_generator)
                if field is None:
                    return
        elif error:
            if parse_clear_error(line):
                error = False
                pbs_pause.process_lines()
                field.add_pause(pbs_pause)
            else:
                pbs_pause.add_line(line)


def parse_scanning_controller_time(line):
    """ Parse a scanning controller line of text to get the date / time.
        scanning controller logs do not print time that same as other PTS logs"""
    time = re.search('\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}:\d{3}', line)
    if time is not None:
        start_time = datetime.datetime.strptime(time.group(), '%d.%m.%Y %H:%M:%S:%f')
        return start_time
    else:
        return None


def parse_sc_error(line):
    """ Dose the line contain the word SC_ERROR

    Args:
        line:

    Returns:
        The primary dose as a Float
    """
    beam = re.search('SC_ERROR', line)
    if beam:
        return True


def parse_clear_error(line):
    """ Dose the line contain the word ClearErrors

    Args:
        line:

    Returns:
        The primary dose as a Float
    """
    beam = re.search('ClearErrors', line)
    if beam:
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




