"""" field is a class to encapsulate a field that was treated on the TCS system. """

import datetime


class Patient(object):

    def __init__(self, pid, start, stop):
        self._patient_id = pid
        self._start_time = start
        self._stop_time = stop

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        self._patient_id = value

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

    def create_file_name_from_id_start_time(self):
      return self.patient_id + self._start_time.strftime("_%m_%d_%Y.txt")

    def __repr__(self):
        str = "Patient: {},  Start Time: {},  Stop Time {}\n".format(self.patient_id,self._start_time, self._stop_time)
        return str
