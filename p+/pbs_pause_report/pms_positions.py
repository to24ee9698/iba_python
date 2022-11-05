from decimal import Decimal


class PmsPositions(object):
    """ A python class to objectify a patient treatment position. """

    def __init__(self):
        """ Initialization of the Treatment objects. """
        self._pps_x = Decimal(0.0)
        self._pps_y = Decimal(0.0)
        self._pps_z = Decimal(0.0)
        self._pps_rot = Decimal(0.0)
        self._pps_pitch = Decimal(0.0)
        self._pps_roll = Decimal(0.0)
        self._gantry_angle = Decimal(0.0)
        self._snout = Decimal(0.0)

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
    def pps_rot(self):
        return self._pps_rot

    @pps_rot.setter
    def pps_rot(self, value):
        self._pps_rot = value

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
    def gantry(self):
        return self._gantry_angle

    @gantry.setter
    def gantry(self, value):
        self._gantry_angle = value

    @property
    def snout(self):
        return self._snout

    @snout.setter
    def snout(self, value):
        self._snout = value

    def __repr__(self):
        repr_string = 'PPS X: {:.2f}\tPPS Y: {:.2f}\tPPS Z: {:.2f}' \
                        '\tPPS Rot: {:.2f}\tPPS Pitch: {:.2f}\tPPS Roll: {:.2f}\t' \
                        'Gantry: {:.2f}\tSnout: {:.2f} \n'.format(
                                            self._pps_x, self._pps_y, self._pps_z, self._pps_rot, self._pps_pitch,
                                            self._pps_roll, self._gantry_angle, self._snout)
        return repr_string
