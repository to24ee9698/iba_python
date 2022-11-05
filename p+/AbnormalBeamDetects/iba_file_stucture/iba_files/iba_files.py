import re
import datetime
import tarfile
from file_helpers import find_files_named


""" Iba log files are timestamped in the file name as not all versions of linux support
a file creation time. Functions in this module help extract creation time from names."""


def parse_line_time(line):
    """ Parse the timestamp out of a line of the pts log files.

    Args:
        line: A line of text from the treatment proccess log.

    Returns:
        A datetime object resenting the time that line happened at.
    """
    match = re.search('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', line)
    if match is not None:
        return datetime.datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S,%f')


def parse_log_file_creation_time(file_name):
    """ Parse the timestamp out of a line of the pts log files.

        Args:
            file_name: Name of a file that contains a date string.

        Returns:

            A datetime object resenting the time that the iba file was created.

        Throws:
           ValueError if no Date string or not proper date string is contain in name.
        """
    match = re.search('\d{8}_\d{6}', file_name)
    if match is not None:
        return datetime.datetime.strptime(match.group(), '%Y%m%d_%H%M%S')
    else:
        raise ValueError('No date found in {}'.format(file_name))


def parse_log_file_room_number(file_name):
    """ Parse the room number from the name of a pts log files.

        Args:
            file_name: Name of a file that contains a room number.

        Returns:

            A room number integer.

        Raises:
           ValueError if no room number exists.
    """
    match = re.search('-\d{1}-', file_name)
    if match is not None:
        return int(match.group().strip('-'))
    else:
        raise ValueError('No room number found'.format(file_name))


def find_room_log_files(path, file_name, room):
    """ Given a path, name, and room number create a generator for all files that contain that combination.

         Args:
             path:     The directory where the files are stored.
             file_name: The name of the file used to search for files of a type. The
             room:      Room number in file.

         Returns:

             A generator that yields all files which contain a given name and room number.

         Raises:

            StopIteration: if no file found.
    """
    files = find_files_named(path, file_name)
    for file in files:
        file_room = parse_log_file_room_number(file)
        if file_room == room:
            yield file


def find_latest_log_file(path, file_name, room):
    """ Given a path, name, and room number find the most recent file that containing that combination.

         Args:
             path:     The directory where the files are stored.
             file_name: The name of the file used to search for files of a type. The
             room:      Room number in file.

         Returns:

             The most recent file that matches the input criteria.

         Raises:

            StopIteration: if no file found.
    """
    if room is None:
        file_generator = find_files_named(path, file_name)
    else:
        file_generator = find_room_log_files(path, file_name, room)

    most_recent_file = None
    most_recent = datetime.datetime(1972, 8, 13, 4, 50, 43, 79043)
    for file in file_generator:
        file_time = parse_log_file_creation_time(file)
        if file_time > most_recent:
            most_recent = file_time
            most_recent_file = file

    return most_recent_file









