""" A module to find and parse TCS Beam Common Process logs."""

import re
import datetime
import tarfile


def find_bap_process( tarfileobject, p, lines):
    bcp = re.compile('^pts-beam-access-point-process')
    if isinstance(tarfileobject, tarfile.TarFile):
        for item in tarfileobject.getmembers():
            if re.search(bcp, item.name) is not None:
                file = tarfileobject.extractfile(item)
                parse_file(p.start_time, p.stop_time, file, lines)


def parse_file(start_time, stop_time, file, lines):
    for rawline in file:
        line = rawline.decode('utf-8','strict')
        line_time = parse_time(line)
        if line_time is not None and line_time > start_time:
            if line_time < stop_time:
                lines.append(parse_data_from_line(line_time, line))
            else:
                return


def parse_time(str):
    """ Parse a line of text to get the date / time. """
    time = re.search('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3}', str)
    if time is not None:
        start_time = datetime.datetime.strptime(time.group(), '%Y-%m-%dT%H:%M:%S,%f')
        return start_time


def parse_data_from_line(time, line):
    try:
        index = line.find(' - ')
        data = line[index+3:].lstrip()
        if time is not None:
            timestring = time.strftime("%m/%d/%Y %H:%M:%S.%f")
            newlist = [timestring, 'BAP',  data]
            return newlist
    except IndexError as e:
        pass

    