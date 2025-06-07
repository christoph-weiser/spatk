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

from spatk.helpers import unpack_args, repack_args

#----------------------------------------------------------------------
# Generic Element Classes
#----------------------------------------------------------------------
class Args(dict):
    def __init__(self, data):

        if isinstance(data, list):
            _data = unpack_args(data)

        super().__init__(_data)

        for k in _data.keys():
            setattr(self, k, _data[k])

    def __str__(self):
        return " ".join(repack_args(self.__dict__))

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        super().__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        super().__setattr__(key, value)


class Default():
    """ Default Circuit Element classs.

    Required inputs:
    ----------------
    line (str):     spice netlist line.
    location (str): location in the netlist hierachy
    n (int):        line number in the netlist.
    uid (str):      unique identifier for this element
    """
    def __init__(self, line, location, lib, n, uid):
        self.line = line
        self.location = location
        self.lib = lib
        self.uid = uid
        self.n = n
        self.instance = None
        self.ports = dict()
        self._value = None

    def __str__(self):
        return self.line

    def parse(self, line):
        pass

    @property
    def type(self):
        return (self.__class__.__name__).lower()

    @property
    def parent(self):
        if self.location != "root":
            return self.location.split("/")[-1]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, arg):
        self._value = arg


class Component(Default):
    """ Generic Component Element Class. """
    def __init__(self, *args):
        super(Component, self).__init__(*args)
        self.elements = self.line.split(" ")
        self.instance = self.elements[0]
        self.parse(self.elements)

    def __str__(self):
        return " ".join(self.elements)

    def _assign_ports(self, elements):
        return {"n"+str(i): p for i,p in enumerate(elements)}

    @property
    def args(self):
        return self.argsdata

    @args.setter
    def args(self, arg):
        self.argsdata = arg


class Component_2T(Component):
    """ Component with two terminals. """
    def __init__(self, *args):
        super(Component_2T, self).__init__(*args)

    def parse(self, elements):
        self.ports = self._assign_ports(elements[1:3])
        self.value = elements[3]
        self.argsdata = Args(elements[4:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.value]
        if self.args:
            l.append(str(self.argsdata))
        return " ".join(l)


class Component_3T(Component):
    """ Component with three terminals. """
    def __init__(self, *args):
        super(Component_3T, self).__init__(*args)

    def parse(self, elements):
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


class Component_4T(Component):
    """ Component with four terminals. """
    def __init__(self, *args):
        super(Component_4T, self).__init__(*args)

    def parse(self, elements):
        self.ports = self._assign_ports(elements[1:5])
        self.value = elements[5]
        self.argsdata = Args(elements[6:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.value]
        if self.args:
            l.append(str(self.argsdata))
        return " ".join(l)


class Statement(Default):
    """ Generic Spice statement Class"""
    def __init__(self, *args):
        super(Statement, self).__init__(*args)
        self.elements = self.line.split(" ")

    def __str__(self):
        return " ".join(self.elements)


class Comment(Default):
    """ Comment. """
    def __init__(self, *args):
        super(Comment, self).__init__(*args)

    def __str__(self):
        return self.line


class Model(Statement):
    """ .model Statement. """
    def __init__(self, *args, expanded=False):
        super(Model, self).__init__(*args)
        self.argsdata = Args(self.elements[3:])
        self.expanded = expanded

    def __str__(self):
        l = [".model",
             self.name,
             self.model_type]
        if self.args:
            if self.expanded:
                l.append("\n+")
                l.append("\n+ ".join(repack_args(self.args.__dict__)))
            else:
                l.append(str(self.argsdata))
        return " ".join(l)

    @property
    def args(self):
        return self.argsdata

    @args.setter
    def args(self, arg):
        self.argsdata = arg

    @property
    def name(self):
        return self.elements[1]

    @name.setter
    def name(self, arg):
        self.elements[1] = arg

    @property
    def model_type(self):
        return self.elements[2]

    @model_type.setter
    def model_type(self, arg):
        self.elements[2] = arg


class Subckt(Component):
    """ X - Subcircuit. """
    def __init__(self, *args):
        super(Subckt, self).__init__(*args)

    @property
    def value(self):
        return self.elements[-1]

    @value.setter
    def value(self, arg):
        self.elements[-1] = arg

    @property
    def name(self):
        return self.elements[-1]

    @name.setter
    def name(self, arg):
        self.elements[-1] = arg


class SubcktDef(Statement):
    """ .subckt Statement. """
    def __init__(self, *args):
        super(SubcktDef, self).__init__(*args)

    @property
    def value(self):
        return self.elements[1]

    @value.setter
    def value(self, arg):
        self.elements[1] = arg

    @property
    def name(self):
        return self.elements[1]

    @name.setter
    def name(self, arg):
        self.elements[1] = arg


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



class Option(Statement):
    """ .option Statement. """
    def __init__(self, *args):
        super(Option, self).__init__(*args)


class Function(Statement):
    """ .func Statement. """
    def __init__(self, *args):
        super(Function, self).__init__(*args)


class Global(Statement):
    """ .global Statement. """
    def __init__(self, *args):
        super(Global, self).__init__(*args)


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


class Vccs(Component_4T):
    """ G - Voltage Controlled Current Source. """
    def __init__(self, *args):
        super(Vccs, self).__init__(*args)


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


class Lossy_transmission_line(Component_4T):
    """ O - Lossy Transmission Line. """
    def __init__(self, *args):
        super(Lossy_transmission_line, self).__init__(*args)


class Vcsw(Component_4T):
    """ S - Voltage Controlled Switch. """
    def __init__(self, *args):
        super(Vcsw, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


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

    def parse(self, elements):
        self.ports = self._assign_ports(elements[1:3])
        if (len(elements) == 4):
            self.value = elements[3]
        else:
            self.value = elements[3:]

    @property
    def voltage(self):
        return self.value

    @voltage.setter
    def voltage(self, arg):
        self.value = arg

    def __str__(self):
        if (len(self.elements) == 4):
            l = [self.instance,
                 *self.ports.values(),
                 self.value]
            return " ".join(l)
        else:
            l = [self.instance,
                 *self.ports.values(),
                 " ".join(self.value)]
            return " ".join(l)


class Icsw(Component_2T):
    """ W - Current Controlled Switch. """
    def __init__(self, *args):
        super(Icsw, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


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

