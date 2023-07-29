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

from spatk.helpers import unpack_args, repack_args

#----------------------------------------------------------------------
# Generic Element Classes
#----------------------------------------------------------------------

class Args(object):
    """ Object representing Circuit element arguments.

    Required inputs:
    ----------------
    args  (list, dict):     list/dict of arguments.
    """
    def __init__(self, args):
        if isinstance(args, list):
            data = unpack_args(args)
        elif isinstance(args, dict):
            data = args
        for k in data.keys():
            setattr(self, k, data[k])

    def __str__(self):
        return " ".join(repack_args(self.__dict__))

    def __bool__(self):
        return bool(self.__dict__)

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    @property
    def content(self):
        return self.__dict__


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


class Model(Statement):
    """ .model Statement. """
    def __init__(self, *args):
        super(Model, self).__init__(*args)
        self.argsdata = Args(self.elements[3:])

    def __str__(self):
        l = [".model",
             self.name,
             self.type]
        if self.args:
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
    def type(self):
        return self.elements[2]

    @type.setter
    def type(self, arg):
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
