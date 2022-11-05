import re


class Positions(object):
    """ A python class to objectify a a patient treatment capturing the patient id, room, start time,
        and stop time of the field. """

    def __init__(self):
        """ Initialization of the Treatment objects. """
        self._gantry_angle = None
        self._pps_x = None
        self._pps_y = None
        self._pps_z = None
        self._pps_rotation = None
        self._pps_pitch = None
        self._pps_roll = None
        self._snout = None
        self.accessory = None

    @property
    def gantry_angle(self):
        return self._gantry_angle

    @gantry_angle.setter
    def gantry_angle(self, value):
        self._gantry_angle = value

    @property
    def pps_x(self):
        return self._pps_x

    @pps_x.setter
    def pps_x(self, value):
        self._pps_x = value

    @property
    def pps_y(self):
        return self._pps_y

    @pps_y.setter
    def pps_y(self, value):
        self._pps_y = value

    @property
    def pps_z(self):
        return self._pps_z

    @pps_z.setter
    def pps_z(self, value):
        self._pps_z = value

    @property
    def pps_rotation(self):
        return self._pps_rotation

    @pps_rotation.setter
    def pps_rotation(self, value):
        self._pps_rotation = value

    @property
    def pps_pitch(self):
        return self._pps_pitch

    @pps_pitch.setter
    def pps_pitch(self, value):
        self._pps_pitch = value

    @property
    def pps_roll(self):
        return self._pps_roll

    @pps_roll.setter
    def pps_roll(self, value):
        self._pps_roll = value

    @property
    def snout(self):
        return self._snout

    @snout.setter
    def snout(self, value):
        self._snout = value

    @property
    def accessory(self):
        return self._accessory

    @accessory.setter
    def accessory(self, value):
        self._accessory = value

    def __repr__(self):
        return 'Gantry: {} \tSnout: {}\nPPS\n X {}\tY: {}\tZ {}\nRotation: {}\tPitch: {}\tRoll: {}\t Accessory: {}' \
            .format(self.gantry_angle, self.snout, self.pps_x, self.pps_y, self.pps_z, self.pps_rotation,
                    self.pps_pitch,
                    self.pps_rotation, self.accessory)


def parse_line(line):
    pos = Positions()
    match = re.search('X=\d*.\d*', line)
    if match is not None:
        first, _, pos.pps_x = match.group().partition('=')
    match = re.search('Y=\d*.\d*', line)
    if match is not None:
        first, _, pos.pps_y = match.group().partition('=')
    match = re.search('Z=\d*.\d*', line)
    if match is not None:
        first, _, pos.pps_z = match.group().partition('=')
    match = re.search('rotation=\d*.\d*', line)
    if match is not None:
        first, _, pos.pps_rotation = match.group().partition('=')
    match = re.search('pitch=\d*.\d*', line)
    if match is not None:
        first, _, pos.pps_pitch = match.group().partition('=')
    match = re.search('roll=\d*.\d*', line)
    if match is not None:
        first, _, pos.pps_roll = match.group().partition('=')
    match = re.search('gantryPosition=\d*.\d*', line)
    if match is not None:
        first, _, pos.gantry_angle = match.group().partition('=')
    match = re.search('snoutPosition=\d*.\d*', line)
    if match is not None:
        first, _, pos.snout = match.group().partition('=')
    match = re.search('AccessoriesDrawer=\w+', line)
    if match is not None:
        first, _, pos.accessory = match.group().partition('=')
    return pos
