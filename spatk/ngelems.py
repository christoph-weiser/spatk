# SPATK - Spice Analysis ToolKit
# Copyright (C) 2023 Christoph Weiser
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
                            Statement, 
                            Comment,
                            Model)

#----------------------------------------------------------------------
# NGSpice element classes
#----------------------------------------------------------------------


class Include(Statement):
    """ .include Statement. """
    def __init__(self, *args):
        super(Include, self).__init__(*args)

    @property
    def filename(self):
        return self.elements[1]

    @filename.setter
    def filename(self, arg):
        self.elements[1] = arg


class Library(Statement):
    """ .lib Statement. """
    def __init__(self, *args):
        super(Library, self).__init__(*args)
        if len(self.elements) == 2:
            self._hasfilename = False
        else:
            self._hasfilename = True

    @property
    def filename(self):
        if self._hasfilename:
            return self.elements[1]
        else:
            return None

    @filename.setter
    def filename(self, arg):
        if self._hasfilename:
            self.elements[1] = arg

    @property
    def libname(self):
        if self._hasfilename:
            return self.elements[2]
        else:
            return self.elements[1]

    @libname.setter
    def libname(self, arg):
        if self._hasfilename:
            self.elements[2] = arg
        else:
            self.elements[1] = arg


class Option(Statement):
    """ .option Statement. """
    def __init__(self, *args):
        super(Option, self).__init__(*args)


class Function(Statement):
    """ .func Statement. """
    def __init__(self, *args):
        super(Function, self).__init__(*args)


class Param(Statement):
    """ .param Statement. """
    def __init__(self, *args):
        super(Param, self).__init__(*args)

    @property
    def value(self):
        return self.elements[1].split("=", 1)[1]

    @value.setter
    def value(self, arg):
        s = self.elements[1].split("=", 1)
        self.elements[1] = "{}={}".format(s[0], arg)

    @property
    def name(self):
        return self.elements[1].split("=", 1)[0]

    @name.setter
    def name(self, arg):
        s = self.elements[1].split("=", 1)
        self.elements[1] = "{}={}".format(arg, s[1])


class Global(Statement):
    """ .global Statement. """
    def __init__(self, *args):
        super(Global, self).__init__(*args)


class Xspice(Default):
    """ A - Xspice Element. """
    def __init__(self, *args):
        super(Xspice, self).__init__(*args)


class Behavioral_source(Default):
    """ B - Behavioral Source. """
    def __init__(self, *args):
        super(Behavioral_source, self).__init__(*args)


class Capacitor(Component_2T):
    """ C - Capacitor. """
    def __init__(self, *args):
        super(Capacitor, self).__init__(*args)

    @property
    def capacitance(self):
        return self.value

    @capacitance.setter
    def capacitance(self, arg):
        self.value = arg


class Diode(Component_2T):
    """ D - Diode. """
    def __init__(self, *args):
        super(Diode, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Vcvs(Component_4T):
    """ E - Voltage Controlled Voltage Source. """
    def __init__(self, *args):
        super(Vcvs, self).__init__(*args)


class Cccs(Component_2T):
    """ F - Current Controlled Current Source. """
    def __init__(self, *args):
        super(Cccs, self).__init__(*args)

    @property
    def vname(self):
        return self.elements[3]

    @vname.setter
    def vname(self, arg):
        self.elements[3] = arg

    def parse(self, elements):
        self.ports = self._assign_ports(elements[1:3])
        self.vname = elements[3]
        self.value = elements[4]
        self.argsdata = Args(elements[5:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.vname,
             self.value]
        if self.args:
            l.append(str(self.argsdata))
        return " ".join(l)

    @property
    def args(self):
        return self.argsdata

    @args.setter
    def args(self, arg):
        self.argsdata = arg


class Vccs(Component_4T):
    """ G - Voltage Controlled Current Source. """
    def __init__(self, *args):
        super(Vccs, self).__init__(*args)


class Ccvs(Component_2T):
    """ H - Current Controlled Voltage Source. """
    def __init__(self, *args):
        super(Ccvs, self).__init__(*args)
        self.parse(self.elements)

    @property
    def vname(self):
        return self.elements[3]

    @vname.setter
    def vname(self, arg):
        self.elements[3] = arg

    def parse(self, elements):
        self.ports = self._assign_ports(elements[1:3])
        self.vname = elements[3]
        self.value = elements[4]
        self.argsdata = Args(elements[5:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.vname,
             self.value]
        if self.args:
            l.append(str(self.argsdata))
        return " ".join(l)

    @property
    def args(self):
        return self.argsdata

    @args.setter
    def args(self, arg):
        self.argsdata = arg

class Isource(Component_2T):
    """ I - Current Source. """
    def __init__(self, *args):
        super(Isource, self).__init__(*args)

    @property
    def current(self):
        return self.value

    @current.setter
    def current(self, arg):
        self.value = arg



class Jfet(Component_3T):
    """ J - JFET Transistor. """
    def __init__(self, *args):
        super(Jfet, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Inductor(Component_2T):
    """ L - Inductor. """
    def __init__(self, *args):
        super(Inductor, self).__init__(*args)

    @property
    def inductance(self):
        return self.value

    @inductance.setter
    def inductance(self, arg):
        self.value = arg


class Mosfet(Component_4T):
    """ M - Mosfet Transistor. """
    def __init__(self, *args):
        super(Mosfet, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Numerical_device_gss(Default):
    """ N - Numerical Device for GSS. """
    def __init__(self, *args):
        super(Numerical_device_gss, self).__init__(*args)


class Lossy_transmission_line(Component_4T):
    """ O - Lossy Transmission Line. """
    def __init__(self, *args):
        super(Lossy_transmission_line, self).__init__(*args)


class Bjt(Component):
    """ Q - Bipolar Transistor. """
    def __init__(self, *args):
        super(Bjt, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg

    def parse(self, elements):
        for i, elem in enumerate(self.elements):
            if "=" in elem:
                i = i-1
                break
        if i == 4:
            self.subs_terminal = False
        elif i == 5:
            self.subs_terminal = True
        else:
            raise Exception("Error could not identify BJT device")
        if self.subs_terminal:
            self.ports = self._assign_ports(elements[1:5])
            self.value = elements[5]
            self.argsdata = Args(elements[6:])
        else:
            self.ports = self._assign_ports(elements[1:4])
            self.value = elements[4]
            self.argsdata = Args(elements[5:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.value]
        if self.args:
            l.append(str(self.argsdata))
        return " ".join(l)


class Resistor(Component_2T):
    """ R - Resistor. """
    def __init__(self, *args):
        super(Resistor, self).__init__(*args)

    @property
    def resistance(self):
        return self.value

    @resistance.setter
    def resistance(self, arg):
        self.value = arg


class Vcsw(Component_4T):
    """ S - Voltage Controlled Switch. """
    def __init__(self, *args):
        super(Vcsw, self).__init__(*args)


class Lossless_transmission_line(Component_4T):
    """ T - Lossless Transmission Line. """
    def __init__(self, *args):
        super(Lossless_transmission_line, self).__init__(*args)


class Uniformely_distributed_rc_line(Component_3T):
    """ U - Uniformely Distributed RC Line. """
    def __init__(self, *args):
        super(Uniformely_distributed_rc_line, self).__init__(*args)


class Vsource(Component_2T):
    """ V - Voltage Source. """
    def __init__(self, *args):
        super(Vsource, self).__init__(*args)

    @property
    def voltage(self):
        return self.value

    @voltage.setter
    def voltage(self, arg):
        self.value = arg


class Icsw(Component_2T):
    """ W - Current Controlled Switch. """
    def __init__(self, *args):
        super(Icsw, self).__init__(*args)


class Subckt(Component):
    """ X - Subcircuit. """
    def __init__(self, *args):
        super(Subckt, self).__init__(*args)


class Single_lossy_transmission_line(Component_4T):
    """ Y - Single Lossy Transmission Line. """
    def __init__(self, *args):
        super(Single_lossy_transmission_line, self).__init__(*args)


class Mesfet(Component_3T):
    """ Z - Mesfet Transistor. """
    def __init__(self, *args):
        super(Mesfet, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg

#----------------------------------------------------------------------
# NGSpice Element Mapping
#----------------------------------------------------------------------

elementmap = {"*":          Comment,
              ".":          Statement,
              "model":      Model,
              "include":    Include,
              "library":    Library,
              "option":     Option,
              "function":   Function,
              "param":      Param,
              "global":     Global,
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


#----------------------------------------------------------------------
# Generic Functions
#----------------------------------------------------------------------

def process_statement(line):
    """ Indentify a SPICE statement.

    Required inputs:
    ----------------
    line (str):     SPICE netlist line.


    Returns
    ----------------
    type (str):     Type of SPICE statement.
    """
    identifier = line.split(" ")[0]
    if identifier in   [".inc", ".include"]:
        return "include"
    elif identifier in [".lib", ".library"]:
        return "library"
    elif identifier in [".model"]:
        return "model"
    elif identifier in [".option"]:
        return "option"
    elif identifier in [".func", ".function"]:
        return "function"
    elif identifier in [".global"]:
        return "global"
    elif identifier in [".par", ".param"]:
        return "param"
    else:
        return "."


def identify_linetype(line):
    """ Identify the type of line.

    Required inputs:
    ----------------
    line (str):     SPICE netlist line.

    """
    line = line.lstrip()
    letter_1 = line[0].upper()
    letter_2 = line[1].upper()
    if (letter_1 == "X" and letter_2 in ["M", "C"]):
        elemtype = letter_1 + letter_2
    elif (letter_1 == "."):
        elemtype = process_statement(line)
    else:
        elemtype = letter_1
    if not elemtype in elementmap.keys():
        raise Exception("Linetype not understood by parser")
    else:
        return elemtype
