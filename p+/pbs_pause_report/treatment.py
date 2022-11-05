from pms_positions import PmsPositions


class Treatment(object):
    """ A python class to objectify a a patient treatment capturing the patient id, room, start time,
        and stop time of the field. """

    def __init__(self):
        """ Initialization of the Treatment objects. """
        self._room = None
        self._start_time = None
        self._stop_time = None
        self._patient_id = None
        self._max_range = None
        self._current = None
        self._pauses = []
        self._dose = 0.0
        self._pms_position = None

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        self._patient_id = value

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, value):
        self._room = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def stop_time(self):
        return self._stop_time

    @stop_time.setter
    def stop_time(self, value):
        self._stop_time = value

    @property
    def max_range(self):
        return self._max_range

    @max_range.setter
    def max_range(self, value):
        self._max_range = value

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = value

    @property
    def dose(self):
        return self._dose

    @dose.setter
    def dose(self, value):
        self._dose = self._dose + value

    @property
    def positions(self):
        return self._pms_position

    @positions.setter
    def positions(self, value):
        self._pms_position = value

    def treatment_found(self):
        """ Treatment found is if all properties of the class have been defined.
            Args:
                self - the current object
            Returns:
                True if the treatment has all properties defined or False if not.
        """
        if self._patient_id and self._start_time and self._stop_time and self._room:
            return True

    def add_pause(self, pause):
        self._pauses.append(pause)

    def all_pauses(self):
        return self._pauses

    def number_of_pauses(self):
        count = 0
        for pause in self._pauses:
            count += 1
        return count

    def record(self, cursor):
        cursor.execute("INSERT INTO treatment_field (room, start_time, stop_time, patient_id, maximum_range,"
                       "maximum_current, dose) VALUES (%d, %s, %s, %s, %f, %f, %f)", (self.room, self.start_time,
                                                                                      self.stop_time, self.patient_id,
                                                                                      self.max_range, self.current,
                                                                                      self.dose))

    def __repr__(self):
        repr_string = 'Patient: {}\tRoom: {}\tStart: {}\tStop: {}\tRange: {:.2f}\tMax Current: {:.2f}\n'.format(
                                            self.patient_id, self.room, self.start_time, self.stop_time,
                                            self.max_range, self.current)
        repr_string += self._pms_position.__repr__()
        for pause in self._pauses:
            repr_string += pause.__repr__()

        return repr_string

