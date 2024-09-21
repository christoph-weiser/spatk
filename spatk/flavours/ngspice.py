# SPATK - Spice Analysis ToolKit
# Copyright (C) 2024 Christoph Weiser
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from spatk.genelems import (Args, 
                            Default, 
                            Component, 
                            Component_2T, 
                            Component_3T, 
                            Component_4T, 
                            Comment,
                            Function, 
                            Global, 
                            Include, 
                            Library, 
                            Model,
                            Option,
                            Param,
                            Statement, 
                            Behavioral_source,
                            Bjt,
                            Capacitor,
                            Cccs,
                            Ccvs, 
                            Diode, 
                            Icsw,
                            Inductor,
                            Jfet,
                            Lossless_transmission_line,
                            Lossy_transmission_line,
                            Mesfet,
                            Mosfet,
                            Resistor, 
                            Subckt,
                            SubcktDef, 
                            Uniformely_distributed_rc_line,
                            Vccs,
                            Vcsw,
                            Vcvs, 
                            Vsource)

#----------------------------------------------------------------------
# NGSpice specific element classes
#----------------------------------------------------------------------

class Temp(Statement):
    """ .temp Statement. """
    def __init__(self, *args):
        super(Temp, self).__init__(*args)

    @property
    def value(self):
        return self.elements[1]

    @value.setter
    def value(self, arg):
        self.elements[1] = str(arg)


class Xspice(Default):
    """ A - Xspice Element. """
    def __init__(self, *args):
        super(Xspice, self).__init__(*args)


class Isource(Component_2T):
    """ I - Current Source. """
    def __init__(self, *args):
        super(Isource, self).__init__(*args)

    def parse(self, elements):
        if len(elements) == 4:
            super(Isource, self).parse(elements)
        else:
            var_source = False
            types = ["dc", "ac", "pulse", "exp", "pwl", 
                     "sffm", "am", "trnoise", "trrandom"] 
            for t in types:
                if t in elements[3]:
                    var_source = True
            if var_source:
                self.ports = self._assign_ports(elements[1:3])
                self.value = " ".join(elements[3:])
                self.argsdata = None
            else:
                super(Isource, self).parse(elements)

    @property
    def current(self):
        return self.value

    @current.setter
    def current(self, arg):
        self.value = arg


class Numerical_device_gss(Default):
    """ N - Numerical Device for GSS. """
    def __init__(self, *args):
        super(Numerical_device_gss, self).__init__(*args)



class Vsource(Component_2T):
    """ V - Voltage Source. """
    def __init__(self, *args):
        super(Vsource, self).__init__(*args)

    def parse(self, elements):
        if len(elements) == 4:
            super(Vsource, self).parse(elements)
        else:
            var_source = False
            types = ["dc", "ac", "pulse", "exp", "pwl", 
                     "sffm", "am", "trnoise", "trrandom"] 
            for t in types:
                if t in elements[3]:
                    var_source = True
            if var_source:
                self.ports = self._assign_ports(elements[1:3])
                self.value = " ".join(elements[3:])
                self.argsdata = None
            else:
                super(Vsource, self).parse(elements)

    @property
    def voltage(self):
        return self.value

    @voltage.setter
    def voltage(self, arg):
        self.value = arg


class Single_lossy_transmission_line(Component_4T):
    """ Y - Single Lossy Transmission Line. """
    def __init__(self, *args):
        super(Single_lossy_transmission_line, self).__init__(*args)


#----------------------------------------------------------------------
# NGSpice Element Mapping
#----------------------------------------------------------------------

elementmap = {"*":          Comment,
              ".":          Statement,
              ".MODEL":     Model,
              ".INC":       Include,
              ".INCLUDE":   Include,
              ".LIB":       Library,
              ".LIBRARY":   Library,
              ".OPTION":    Option,
              ".FUNC":      Function,
              ".TEMP":      Temp,
              ".PARAM":     Param,
              ".GLOBAL":    Global,
              ".SUBCKT":    SubcktDef,
              "A":          Xspice,
              "B":          Behavioral_source,
              "C":          Capacitor,
              "D":          Diode,
              "E":          Vcvs,
              "F":          Cccs,
              "G":          Vccs,
              "H":          Ccvs,
              "I":          Isource,
              "J":          Jfet,
              "K":          None,
              "L":          Inductor,
              "M":          Mosfet,
              "N":          Numerical_device_gss,
              "O":          Lossy_transmission_line,
              "P":          None,
              "Q":          Bjt,
              "R":          Resistor,
              "S":          Vcsw,
              "T":          Lossless_transmission_line,
              "U":          Uniformely_distributed_rc_line,
              "V":          Vsource,
              "W":          Icsw,
              "X":          Subckt,
              "XC":         Capacitor,
              "XM":         Mosfet,
              "Y":          Single_lossy_transmission_line,
              "Z":          Mesfet}
