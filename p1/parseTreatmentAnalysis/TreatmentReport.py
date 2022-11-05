import re
from Iteration import next_item


class TreatmentReport(object):
    """ A python class to objectify a a patient treatment capturing the patient id, room, start time,
        and stop time of the field. """

    def __init__(self):
        """ Initialization of the Treatment objects. """
        self._patient_id = None
        self._room = None
        self._field_name = None
        self._start_time = None
        self._stop_time = None
        self._beam_start_time = None
        self._beam_stop_time = None
        self._target_positions = None
        self._actual_positions = None
        self._pauses = 0
        self._beam_prepares = 0
        self._disconnects = 0
        self._partials = 0
        self._layers = None

    @property
    def partial(self):
        return self._partials

    @partial.setter
    def partial(self, value):
        self._partials = value

    @property
    def disconnects(self):
        return self._disconnects

    @disconnects.setter
    def disconnects(self, value):
        self._disconnects = value

    @property
    def pauses(self):
        return self._pauses

    @pauses.setter
    def pauses(self, value):
        self._pauses = value

    @property
    def prepares(self):
        return self._beam_prepares

    @prepares.setter
    def prepares(self, value):
        self._beam_prepares = value

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
    def beam_start_time(self):
        return self._beam_start_time

    @beam_start_time.setter
    def beam_start_time(self, value):
        self._beam_start_time = value

    @property
    def beam_stop_time(self):
        return self._beam_stop_time

    @beam_stop_time.setter
    def beam_stop_time(self, value):
        self._beam_stop_time = value

    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, value):
        self._field_name = value

    def treatment_found(self):
        """ Treatment found is if all properties of the class have been defined.
            Args:
                self - the current object
            Returns:
                True if the treatment has all properties defined or False if not.
        """
        if self._patient_id and self._beam_start_time and self._beam_stop_time and self._room:
            return True

    def parse_layer_energy_dose(self, data, line, layers):
        number = -1
        layers = int(layers)
        self._layers = []
        is_first = True

        while number != layers:
            if line:
                layer_number = re.search('Treament Process - Effective layer \d*', line)
                if layer_number is not None:
                    last, _, number = layer_number.group().partition('layer ')
                    if number is not None:
                        if is_first:
                            count = int(number)
                            value = count
                            while count > 0:
                                self._layers.append((0, 0))
                                count = count - 1
                            is_first = False
                        number = int(number) + 1
                        layer_energy = re.search('energy:\d*.\d*', line)
                        first, _, energy = layer_energy.group().partition(':')
                        layer_dose = re.search('dose:\d*.\d*', line)
                        first, _, dose = layer_dose.group().partition(':')
                        # Fill in Zeros for Layers when partials
                        self._layers.append((energy, dose))
                line = next_item(data)
                end_of_record = re.search('creating Dicom Treatment Record', line)
                if end_of_record is not None:
                    return

    def parse_layers(self, data, line):
        layer_size = re.search('Prescription \d{2}', line)
        if layer_size is not None:
            first, _, size = layer_size.group().partition(' ')
            self.parse_layer_energy_dose(data, line, size)

    def __repr__(self):

        data = '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {:0.2f},' \
               '{:0.2f}, {:0.2f}, {:0.2f}, {:0.2f}, {:0.2f}, {:0.2f}, {:0.2f}, {}'.format(self.patient_id,
                self.room, self._field_name, self.start_time, self.stop_time,
                self._beam_start_time, self._beam_stop_time, self.prepares, self._pauses, self.disconnects,
                float(self._actual_positions.gantry_angle), float(self._actual_positions.snout),
                float(self._actual_positions.pps_x), float(self._actual_positions.pps_y),
                float(self._actual_positions.pps_z), float(self._actual_positions.pps_rotation),
                float(self._actual_positions.pps_pitch), float(self._actual_positions.pps_roll),
                self._actual_positions.accessory)

        if self._layers is not None:
            for item in self._layers:
                data = data + ', {:0.2f}, {:0.2f}'.format(float(item[0]), float(item[1]))

        return data


