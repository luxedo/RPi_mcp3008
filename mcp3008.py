#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
RPi_mcp3008 is a library to listen to the MCP3008 A/D converter chip, as described in the datasheet.
https://www.adafruit.com/datasheets/MCP3008.pdf
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

class MCP3008(object):
    '''
    Object that listens the MCP3008 in the SPI port of the RPi
    Connects the object to the specified SPI device.
    MCP3008(X, Y) will open /dev/spidev-X.Y, same as spidev.SpiDev.open(X, Y)
    '''
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def close(self):
        self.spi.close()

    def read(self, mode, norm=False):
        '''
        Returns the raw value (0 ... 1024) of the reading.
        mode is the mode of operation (e.g. mcp3008.CH0)
        norm is a normalization factor, usually Vref
        '''
        if not 0 <= mode <= 15:
            raise IndexError('Outside the channels scope, please use: 0, 1 ..., 7')
        request = [0x1, mode << 4, 0x0] # [start bit, configuration, listen space]
        _, byte1, byte2 = self.spi.xfer(request)
        value = (byte1%4 << 8) + byte2
        if norm:
            return float(norm)*value/RESOLUTION
        else:
            return value

    def read_all(self, norm=False):
        '''
        Returns a list with the readings of all the channels and modes
        Order:
        [DF0, DF1, DF2, DF3, DF4, DF5, DF6, DF7,
         CH0, CH1, CH2, CH3, CH4, CH5, CH6, CH7]
        norm is a normalization factor, usually Vref
        '''
        return [self.read(x, norm) for x in range(16)]

if __name__ == '__main__':
    with MCP3008() as chip:
        print(chip.read_all(4.35))
        print(chip.read_all())
