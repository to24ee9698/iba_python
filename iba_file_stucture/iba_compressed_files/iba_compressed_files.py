import re
import datetime
import tarfile
from file_helpers import find_files_named
from file_helpers import find_tar_files_in_tarball


""" Iba log files are timestamped in the file name as not all versions of linux support
a file creation time. Functions in this module help extract creation time from names."""


def parse_compressed_file_date(file_name):
    """ Parse the date number from the name of a compressed pts file.

        Args:
            file_name: Name of a file that contains a room number.

        Returns:

            A datetime object representing the date of the file.

        Raises:
           ValueError if no room number exists.
    """
    match = re.search('\d{8}', file_name)
    if match is not None:
        return datetime.datetime.strptime(match.group(), '%Y%m%d')
    else:
        raise ValueError('No room number found'.format(file_name))


def find_compressed_logs_dated(path, start_date, stop_date):
    """ Given a path find the compressed output logs between given dates

         Args:
             path: The directory where the files are stored.
             start_date: The first date to get logs from
             stop_date: the last date to get logs from

         Returns:

             A generator that yields all files which are between two dates.

         Raises:

            StopIteration: if no file found.
    """
    file_generator = find_files_named(path, 'OUTPUT*.tar.gz')
    for file_name in file_generator:
        file_date = parse_compressed_file_date(file_name)
        if start_date <= file_date <= stop_date:
            yield file_name


def find_room_log_file_in_compressed_tarball(tarball, file_name, room):
    """ Given a path, name, and room number create a generator for all files that contain that combination found
        in a given tarball object.

         Args:
             tarball:   The tarball that should contain the file.
             file_name: The name of the file used to search for files of a type. The
             room:      Room number in file.

         Returns:

             A generator that yields all files which contain a given name and room number.

         Raises:

            StopIteration: if no file found.
    """

    if room is not None:
        log_name = re.compile('{}-{}'.format(file_name, room))
    else:
        log_name = re.compile('{}'.format(file_name))

    for item in tarball.getmembers():
        if re.search(log_name, item.name) is not None:
            yield tarball.extractfile(item)


def find_named_dated_files_in_compressed_logs(path, file_name, room, date):
    """ Given a path find the files of a file name and room from a specific date.

        Args:
            path: The directory where the files are stored.
            file_name: The prefix of the file name
            room: room number if for a specific room
            date: The first date to get logs from

         Returns:

             A generator that yields all files match name and date.

         Raises:

            StopIteration: if no file found.
    """

    # Convert the date object to a range of dates of where the file should be in compressed logs.
    # The date stamp on the compressed log is usually a day or 2 after the actual file dates.
    start_date = date
    compressed_log_generator = find_compressed_logs_dated(path, start_date, start_date + 2)
    for compressed_log in compressed_log_generator:
        tar_file_generator = find_tar_files_in_tarball(compressed_log)
        for tar_file in tar_file_generator:
            for result_files in find_room_log_file_in_compressed_tarball(tar_file, file_name, room):
                yield result_files








