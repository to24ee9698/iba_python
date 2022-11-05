import os
import re
from  enum import IntEnum,unique

@unique
class LayerSpec(IntEnum):
    
    ELEMENT_ID = 0,
    SPOT_ID = 1,
    ELEMENT_TYPE = 2,
    X_CURRENT_TARGET_SP = 3,
    Y_CURRENT_TARGET_SP = 4,
    MAX_DURATION = 5,
    TARGET_CHARGE = 6,
    BEAM_CURRENT_SP = 7,
    MIN_BEAM_CURRENT_FB = 8,
    MAX_BEAM_CURRENT_FB = 9,
    MIN_CHARGE_PRIM = 10,
    MAX_CHARGE_PRIM = 11,
    MIN_CHARGE_SEC = 12,
    MAX_CHARGE_SEC = 13,
    MIN_CHARGE_TER = 14,
    MAX_CHARGE_TER = 15,
    X_CURRENT_MIN_PRIM_FB = 16,
    Y_CURRENT_MIN_PRIM_FB = 17,
    X_CURRENT_MAX_PRIM_FB = 18,
    Y_CURRENT_MAX_PRIM_FB = 19,
    X_VOLT_MIN_PRIM_FB = 20,
    Y_VOLT_MIN_PRIM_FB = 21,
    X_VOLT_MAX_PRIM_FB = 22,
    Y_VOLT_MAX_PRIM_FB = 23,
    X_CURRENT_MIN_SEC_FB = 24,
    Y_CURRENT_MIN_SEC_FB = 25,
    X_CURRENT_MAX_SEC_FB = 26,
    Y_CURRENT_MAX_SEC_FB = 27,
    X_VOLT_MIN_SEC_FB = 28,
    Y_VOLT_MIN_SEC_FB = 29,
    X_VOLT_MAX_SEC_FB = 30,
    Y_VOLT_MAX_SEC_FB = 31,
    X_MIN_FIELD = 32,
    Y_MIN_FIELD = 33,
    X_MAX_FIELD = 34,
    Y_MAX_FIELD = 35,
    MIN_DOSE_RATE_PRIM = 36,
    MAX_DOSE_RATE_PRIM = 37,
    MIN_DOSE_RATE_SEC = 38,
    MAX_DOSE_RATE_SEC = 39,
    MIN_DOSE_RATE_TER = 40,
    MAX_DOSE_RATE_TER = 41,
    X_MIN_WIDTH = 42,
    X_MAX_WIDTH = 43,
    Y_MIN_WIDTH = 44,
    Y_MAX_WIDTH = 45,
    X_POS_LOW = 46,
    X_POS_HIGH = 47,
    Y_POS_LOW = 48,
    Y_POS_HIGH = 49,
    X_MIN_IC1_POS = 50,
    X_MAX_IC1_POS = 51,
    Y_MIN_IC1_POS = 52,
    Y_MAX_IC1_POS = 53,
    X_MIN_IC1_WIDTH = 54,
    X_MAX_IC1_WIDTH = 55,
    Y_MIN_IC1_WIDTH = 56,
    Y_MAX_IC1_WIDTH = 57



class LayerSpecification:

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
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        self._id = value

    @property
    def total_charge(self):
        return self._total_charge

    @total_charge.setter
    def total_charge(self, value):
        self._total_charge = value

    @property
    def scanning_magnet_x_offset(self):
        return self._scanning_magnet_x_offset

    @scanning_magnet_x_offset.setter
    def scanning_magnet_x_offset(self, value):
        self._scanning_magnet_x_offset = value

    @property
    def scanning_magnet_y_offset(self):
        return self._scanning_magnet_y_offset

    @scanning_magnet_y_offset.setter
    def scanning_magnet_y_offset(self, value):
        self._scanning_magnet_y_offset = value

    @property
    def ion_chamber_x_offset(self):
        return self._ion_chamber_x_offset

    @ion_chamber_x_offset.setter
    def ion_chamber_x_offset(self, value):
        self._ion_chamber_x_offset = value

    @property
    def ion_chamber_y_offset(self):
        return self._ion_chamber_y_offset

    @ion_chamber_y_offset.setter
    def ion_chamber_y_offset(self, value):
        self._ion_chamber_y_offset = value

    @property
    def elements(self):
        return int(self._elements)

    @elements.setter
    def elements(self,value):
        self._elements = int(value)

    def parse_specification(self, file):

        with open(file,'r') as f:
            for line in f:
                data_lists = line.split(',')
                self._layer.append(data_lists)

        self._id = self._layer[1][0]
        self._range = self._layer[1][1]
        self._total_charge = self._layer[1][2]
        self._elements = self._layer[1][3]
        self._scanning_magnet_x_offset = self._layer[3][0]
        self._scanning_magnet_y_offset = self._layer[3][1]
        self._ion_chamber_x_offset = self._layer[3][0]
        self._ion_chamber_y_offset = self._layer[3][1]
        del self._layer[0:5]

    def __repr__(self):
        print("Layer #: {}, Range: {}, Total Charge {}, Elements: {}, SM X: {}, SM Y {}, IC X: {}, IC Y: {}".format
              (self.id,self.range,self.total_charge,self.elements,self.scanning_magnet_x_offset,
               self.scanning_magnet_y_offset,self.ion_chamber_x_offset,self.ion_chamber_y_offset)) 
        print(self._layer)
