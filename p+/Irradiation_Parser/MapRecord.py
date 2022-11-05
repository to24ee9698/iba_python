import os
import re
from  enum import IntEnum,unique

@unique
class MapRec(IntEnum):
    SUBMAP_NUMBER = 0,
    TIME = 1,
    X_WIDTH = 2,
    Y_WIDTH = 3,
    X_POSITION = 4,
    Y_POSITION = 5,
    X_DOSE = 6,
    Y_DOSE = 7,
    X_DOSE_RATE = 8,
    Y_DOSE_RATE = 9,
    X_WIDTH_IC1 = 10,
    Y_WIDTH_IC1 = 11,
    X_POSITION_IC1 = 12,
    Y_POSITION_IC1 = 13,
    DOSE_IC1_X = 14,
    DOSE_IC1_Y  = 15,
    DOSE_RATE_IC1_X = 16,
    DOSE_RATE_IC1_Y  = 17,
    X_CURRENT_PRIM  = 18,
    Y_CURRENT_PRIM  = 19,
    X_VOLTAGE_PRIM = 20,
    Y_VOLTAGE_PRIM = 21,
    X_CURRENT_SEC = 22, 
    Y_CURRENT_SEC = 23,
    X_VOLTAGE_SEC = 24,
    Y_VOLTAGE_SEC = 25,
    DOSE_PRIM = 26,
    DOSE_SEC = 27,
    DOSE_RATE_PRIM = 28,
    DOSE_RATE_SEC = 29,
    BEAMCURRENT = 30

class MapRecord:

    def __init__(self):
        self._layer = []

    def get_layers(self):
        return self._layer

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def total_charge(self):
        return self._total_charge

    @total_charge.setter
    def total_charge(self, value):
        self._total_charge = value

    @property
    def last_element(self):
        return self._last_element

    @last_element.setter
    def last_element(self,value):
        self._last_element = value
  
    def parse_record(self, file):
        with open(file,'r') as f:
            for line in f:
                new_line = line.rstrip()
                data_lists = new_line.split(',')
                self._layer.append(data_lists)
     
        # Filter top of file.
        value = 1
        while value == 1:
            if 'SUBMAP_NUMBER' in self._layer[0]:
                value = 0
            else:
                del self._layer[0]
    
        del self._layer[0]

        # Filter bottom of file.
        value = -1
        while  value == -1:
           del self._layer[-1]
           try:
               value = int(self._layer[-1][0])
           except :
               pass
           self._last_element = self._layer[-1][0]


    def __repr__(self):
        print("Map Record Layer #: {}, Last Element: {}".format(self.id, self.last_element))
        print(self._layer)