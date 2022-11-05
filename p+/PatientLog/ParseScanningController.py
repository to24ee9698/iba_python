""" A module to find and parse TCS Treatment Process logs."""

import os
import re
import datetime
import Patient
import tarfile


def find_scanning_controller(tarfileobject, p, lines):
    sc = re.compile('^pts-scanningcontroller-gateway')
    if isinstance(tarfileobject, tarfile.TarFile):
        for item in tarfileobject.getmembers():
            if re.search(sc, item.name) is not None:
                file = tarfileobject.extractfile(item)
                parse_file(p.start_time, p.stop_time, file, lines)


def parse_file(start_time, stop_time, file, lines):
    last_time = None
    for raw_line in file:
        line = raw_line.decode('utf-8', 'strict')
        line_time = parse_time(line)
        if line_time is not None and line_time > start_time:
            if line_time < stop_time:
                lines.append(parse_data_from_line(line_time, line))
        else:
            if line_time is None and last_time is not None:
                tmp_line = last_time.strftime('%d.%m.%Y %H:%M:%S:%f') + ' '
                tmp_line.join(line)
                lines.append(tmp_line)
                return


def parse_time(str):
    """ Parse a line of text to get the date / time. """
    time = re.search('\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}:\d{3}', str)
    if time is not None:
        start_time = datetime.datetime.strptime(time.group(), '%d.%m.%Y %H:%M:%S:%f')
        return start_time
    else:
        return None


def parse_data_from_line(time, line):
    try:
        if time is not None:
            index = line.rfind(' ', 0, 24)
            data = line[index:]
            timestring = time.strftime("%m/%d/%Y %H:%M:%S.%f")
            newlist = [timestring, 'SC', data]
            return newlist
    except IndexError as e:
        e.print()
