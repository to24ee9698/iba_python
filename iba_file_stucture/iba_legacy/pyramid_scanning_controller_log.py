import datetime
import re


def parse_controller_time(line):
    """ Parse a scanning controller line of text to get the date / time.
        scanning controller logs do not print time that same as other PTS logs"""
    time = re.search('\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}:\d{3}', line)
    if time is not None:
        start_time = datetime.datetime.strptime(time.group(), '%d.%m.%Y %H:%M:%S:%f')
        return start_time
    else:
        return None


def parse_error(line):
        """ Dose the line contain the word Beam and SGCU

        Args:
            line:

        Returns:
            The primary dose as a Float
        """
        beam = re.search('_BeamOnInError', line)
        if beam:
            return True