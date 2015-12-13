#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
RPi_mcp3008 is a library to listen to the MCP3008 A/D converter chip,
as described in the datasheet.
https://www.adafruit.com/datasheets/MCP3008.pdf

Copyright (C) 2015 Luiz Eduardo Amaral <luizamaral306@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import spidev

# Modes Single
CH0 = 8     # single-ended CH0
CH1 = 9     # single-ended CH1
CH2 = 10    # single-ended CH2
CH3 = 11    # single-ended CH3
CH4 = 12    # single-ended CH4
CH5 = 13    # single-ended CH5
CH6 = 14    # single-ended CH6
CH7 = 15    # single-ended CH7
# Modes Diff
DF0 = 0     # differential CH0 = IN+ CH1 = IN-
DF1 = 1     # differential CH0 = IN- CH1 = IN+
DF2 = 2     # differential CH2 = IN+ CH3 = IN-
DF3 = 3     # differential CH2 = IN- CH3 = IN+
DF4 = 4     # differential CH4 = IN+ CH5 = IN-
DF5 = 5     # differential CH4 = IN- CH5 = IN+
DF6 = 6     # differential CH6 = IN+ CH7 = IN-
DF7 = 7     # differential CH6 = IN- CH7 = IN+

RESOLUTION = 1 << 10 # 10 bits resolution

class MCP3008(spidev.SpiDev):
    '''
    Object that listens the MCP3008 in the SPI port of the RPi.
    Connects the object to the specified SPI device.
    The initialization arguments are MCP3008(bus=0, device=0) where:
    MCP3008(X, Y) will open /dev/spidev-X.Y, same as spidev.SpiDev.open(X, Y).
    '''
    def __init__(self, bus=0, device=0):
        self.bus = bus
        self.device = device
        self.open(self.bus, self.device)
        self.modes = False

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __repr__(self):
        return 'MCP3008 object at bus {0}, device {1}'.format(self.bus, self.device)

    def __call__(self, norm=False):
        return self.read(self.modes, norm)

    @classmethod
    def fixed(cls, modes, bus=0, device=0):
        '''
        Initializes the class with fixed modes, which turns the instance callable.
        The modes argument is a list with the modes of operation to be read (e.g.
        [mcp3008.CH0,mcp3008.Df0]).
        When calling the instance the object will execute a reading of and return the
        values (e.g. print instance()).
        When calling the instance, you can pass the optional argument norm to
        normalize
        the data (e.g. print instance(5.2)).
        '''
        instance = cls(bus, device)
        instance.modes = modes
        return instance

    def _read_single(self, mode):
        '''
        Returns the value of a single mode reading
        '''
        if not 0 <= mode <= 15:
            raise IndexError('Outside the channels scope, please use: 0, 1 ..., 7')
        request = [0x1, mode << 4, 0x0] # [start bit, configuration, listen space]
        _, byte1, byte2 = self.xfer2(request)
        value = (byte1%4 << 8) + byte2
        return value

    def read(self, modes, norm=False):
        '''
        Returns the raw value (0 ... 1024) of the reading.
        The modes argument is a list with the modes of operation to be read (e.g.
        [mcp3008.CH0,mcp3008.Df0]).
        norm is a normalization factor, usually Vref.
        '''
        reading = []
        for mode in modes:
            reading.append(self._read_single(mode))
        if norm:
            return [float(norm)*value/RESOLUTION for value in reading]
        else:
            return reading

    def read_all(self, norm=False):
        '''
        Returns a list with the readings of all the modes
        Data Order:
        [DF0, DF1, DF2, DF3, DF4, DF5, DF6, DF7,
         CH0, CH1, CH2, CH3, CH4, CH5, CH6, CH7]
        norm is a normalization factor, usually Vref.
        '''
        return self.read(range(16), norm)
