class Treatment(object):
    """ A python class to objectify a patient treatment capturing the patient id, room, start time,
        and stop time of the field. """

    def __init__(self):
        """ Initialization of the Treatment objects. """
        self._room = None
        self._start_time = None
        self._stop_time = None
        self._patient_id = None

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

    def treatment_found(self):
        """ Treatment found is if all properties of the class have been defined.
            Args:
                self - the current object
            Returns:
                True if the treatment has all properties defined or False if not.
        """
        if self._patient_id and self._start_time and self._stop_time and self._room:
            return True

    def __repr__(self):
        return 'Patient: {}\tRoom: {}\tStart: {}\tStop: {}\n'.format(self.patient_id,
                                                                     self.room,
                                                                     self.start_time,
                                                                     self.stop_time)
