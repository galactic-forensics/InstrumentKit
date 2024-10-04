#!/usr/bin/env python

# IMPORTS #####################################################################


from enum import IntEnum

from instruments.units import ureg as u

from instruments.abstract_instruments import Instrument
from instruments.util_fns import convert_temperature, assume_units

# CLASSES #####################################################################


class VRG1000A(Instrument):

    def __init__(self, filelike):
        super().__init__(filelike)
        self.terminator = "\r"

    @property
    def frequency(self):
        """Get/set the frequency unitful.

        If no units were given, assume MHz.

        :raises ValueError: If the frequency is not in valid range.
        """
        answ = self.query("RQ")
        val = float(answ.lstrip("RQ")) * u.kHz
        return val

    @frequency.setter
    def frequency(self, freq):
        freq = assume_units(freq, u.MHz)
        
        if freq < 25 * u.MHz or freq > 42 * u.MHz:
            raise ValueError("Frequency must be between 25 and 42 MHz.")

        freq = freq.to(u.kHz).magnitude
        cmd = f"SF{int(freq)}"
        _ = self.query(cmd)  # sends back empty line plus one line with cmd
        _ = self.read()  # reads the additional line with command

    @property
    def power(self):
        """Get/set the power unitful in W.

        If no units were given, assume W.

        :raises ValueError: If the power is not in valid range.
        """
        answ = self.query("RF")
        print(answ)
        val = float(answ[2:]) * u.W
        return val

    @power.setter
    def power(self, power):
        power = assume_units(power, u.W)

        # if power < 0 or power > 1:
        #     raise ValueError("Power must be between 0 and 1 W.")

        power = power.to(u.W).magnitude
        cmd = f"SP{power:04}"
        answ = self.query(cmd)  # sends back empty line plus one line with cmd
        print(answ)
