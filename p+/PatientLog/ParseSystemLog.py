""" A module to find and parse TCS Beam Common Process logs."""

import os
import re
import datetime
import tarfile


def create_search_string(directory, filename):
    day = parse_day_filename(filename)
    return directory + '/System/' + day + '-SYSTEM.tar.gz'


def parse_day_filename(str):
    day = re.search('\d{8}', str)
    if day is not None:
        return day.group()


def find_system_log(filename, p, lines):
    sys = re.compile('.rtdat$')
    bckup = re.compile('.rtdat_bck$')
    with tarfile.open(filename, 'r:gz') as f:
        for item in f.getmembers():
            if re.search(sys, item.name) is not None:
                file = f.extractfile(item)
                parse_file(p.start_time, p.stop_time, file, lines)
            if re.search(bckup, item.name) is not None:
                file =  f.extractfile(item)
                parse_file(p.start_time, p.stop_time, file, lines)
 

def parse_file(start_time, stop_time, file, lines):
    for rawline in file:
        try:
            line = rawline.decode('utf-8')
            line_time = parse_time(line)
            if line_time is not None and line_time > start_time: 
                if line_time < stop_time:
                    lines.append(parse_data_from_line(line_time, line))
                else:
                    return
        except UnicodeDecodeError as e:
            pass

def parse_time(str):
    """ Parse a line of text to get the date / time. """
    time = re.search('\d{2}-\d{2}-\d{4}_\d{2}:\d{2}:\d{2}:\d{3}', str)
    if time is not None:
        start_time = datetime.datetime.strptime(time.group(), '%m-%d-%Y_%H:%M:%S:%f')
        return start_time

def parse_data_from_line(time, line):
    try:
        cut_point = re.search('\d{2}-\d{2}-\d{4}_\d{2}:\d{2}:\d{2}:\d{3}:\d{3}:\d{3}', line)
        if cut_point is not None:
            data = line[cut_point.regs[0][1]:].lstrip()
        if time is not None:
            timestring = time.strftime("%m/%d/%Y %H:%M:%S.%f")
            newlist = [timestring, 'SYSTEM', data]
            return newlist
    except IndexError as e:
        pass

    
