import re
import datetime


class Pause(object):
    """ A python class to objectify a pause event during a pbs treatment. """

    def __init__(self):
        """ Initialization of the Treatment objects. """
        self._time = None
        self._type = None
        self._device = None
        self._lines = []
        self._data = None

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def add_line(self, line):
        self._lines.append(line)

    def process_lines(self):
        current_time = 200000
        data_line = False
        for line in self._lines:
            self._time = parse_scanning_controller_time(self._lines[0])
            tokens = line.split(' ')
            try:
                if line[0][0] == '(' and data_line == True:  # This indicates a data line.
                    self.type = tokens[0][1:]
                    if '_POS' in tokens[0]:
                        self._data = (tokens[2], tokens[3], tokens[5], tokens[7])
                    else:
                        self._data = (tokens[1], tokens[2], tokens[4], tokens[6])
                    data_line = False
                    continue
                else:
                    index = tokens.index('Timeslice:')
                    time = tokens[index + 1]
                    if int(time) < current_time:
                        current_time = int(time)
                        self._device = tokens[0]
                        self._type = tokens[3]
                        data_line = True

            except ValueError:
                pass

    def __repr__(self):
        return '\tPause: Device {}\t Type {}\t Time: {} \n\t\tData: {}\n'.format(self._device, self._type, self._time,
                                                                           self._data)


def parse_scanning_controller_time(line):
    """ Parse a scanning controller line of text to get the date / time.
    scanning controller logs do not print time that same as other PTS logs"""
    time = re.search('\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}:\d{3}', line)
    if time is not None:
        start_time = datetime.datetime.strptime(time.group(), '%d.%m.%Y %H:%M:%S:%f')
        return start_time
    else:
        return None
