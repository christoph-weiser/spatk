# SPATK - Spice Analysis Toolkit.
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

import re
import copy
import datetime
import hashlib
import collections

#----------------------------------------------------------------------
# Generic Element Classes
#----------------------------------------------------------------------

class Args:
    def __init__(self, args):
        self._args = unpack_args(args)
        for k in self._args.keys():
            setattr(self, "{}".format(k), self._args[k])

    def __str__(self):
        return " ".join(repack_args(self._args))


class Default():
    def __init__(self, line, location, n, uid):
        self.line = line
        self.location = location
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
    def __init__(self, *args):
        super(Component, self).__init__(*args)
        self.elements = self.line.split(" ")
        self.instance = self.elements[0]

    def __str__(self):
        return " ".join(self.elements)

    def _assign_ports(self, elements):
        return {"n"+str(i): p for i,p in enumerate(elements)}


class Component_2T(Component):
    def __init__(self, *args):
        super(Component_2T, self).__init__(*args)
        self.parse(self.elements)
        for k in self._args._args.keys():
            setattr(self, "{}".format(k), self._args._args[k])

    def parse(self, elements):
        self.ports = self._assign_ports(elements[1:3])
        self.value = elements[3]
        self._args = Args(elements[4:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.value]
        if self.args:
            l.append(str(self._args))
        return " ".join(l)

    @property
    def args(self):
        return self._args._args

    @args.setter
    def args(self, arg):
        self._args._args = arg


class Component_3T(Component):
    def __init__(self, *args):
        super(Component_3T, self).__init__(*args)
        self.parse(self.elements)
        for k in self._args._args.keys():
            setattr(self, "{}".format(k), self._args._args[k])

    def parse(self, elements):
        self.ports = self._assign_ports(elements[1:4])
        self.value = elements[4]
        self._args = Args(elements[5:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.value]
        if self.args:
            l.append(str(self._args))
        return " ".join(l)

    @property
    def args(self):
        return self._args._args

    @args.setter
    def args(self, arg):
        self._args._args = arg


class Component_4T(Component):
    def __init__(self, *args):
        super(Component_4T, self).__init__(*args)
        self.parse(self.elements)
        for k in self._args._args.keys():
            setattr(self, "{}".format(k), self._args._args[k])

    def parse(self, elements):
        self.ports = self._assign_ports(elements[1:5])
        self.value = elements[5]
        self._args = Args(elements[6:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.value]
        if self.args:
            l.append(str(self._args))
        return " ".join(l)

    @property
    def args(self):
        return self._args._args

    @args.setter
    def args(self, arg):
        self._args._args = arg


class Statement(Default):
    def __init__(self, *args):
        super(Statement, self).__init__(*args)
        self.elements = self.line.split(" ")

    def __str__(self):
        return " ".join(self.elements)


#----------------------------------------------------------------------
# Element Classes
#----------------------------------------------------------------------

class Comment(Default):
    def __init__(self, *args):
        super(Comment, self).__init__(*args)


# TODO: a model has a well defined structure that
#       can be parsed more detailed.
class Model(Statement):
    def __init__(self, *args):
        super(Model, self).__init__(*args)


class Include(Statement):
    def __init__(self, *args):
        super(Include, self).__init__(*args)

    @property
    def filename(self):
        return self.elements[1]

    @filename.setter
    def filename(self, arg):
        self.elements[1] = arg


class Library(Statement):
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
    def __init__(self, *args):
        super(Option, self).__init__(*args)


class Function(Statement):
    def __init__(self, *args):
        super(Function, self).__init__(*args)


class Param(Statement):
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
    def __init__(self, *args):
        super(Global, self).__init__(*args)


class Xspice(Default):
    def __init__(self, *args):
        super(Xspice, self).__init__(*args)


class Behavioral_source(Default):
    def __init__(self, *args):
        super(Behavioral_source, self).__init__(*args)


class Capacitor(Component_2T):
    def __init__(self, *args):
        super(Capacitor, self).__init__(*args)

    @property
    def capacitance(self):
        return self.value

    @capacitance.setter
    def capacitance(self, arg):
        self.value = arg


class Diode(Component_2T):
    def __init__(self, *args):
        super(Diode, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Vcvs(Component_2T):
    def __init__(self, *args):
        super(Vcvs, self).__init__(*args)


class Cccs(Component_2T):
    def __init__(self, *args):
        super(Cccs, self).__init__(*args)
        for k in self._args._args.keys():
            setattr(self, "{}".format(k), self._args._args[k])

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
        self._args = Args(elements[5:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.vname,
             self.value]
        if self.args:
            l.append(" ".join(self.args))
        return " ".join(l)

    @property
    def args(self):
        return self._args._args

    @args.setter
    def args(self, arg):
        self._args._args = arg


class Vccs(Component_2T):
    def __init__(self, *args):
        super(Vccs, self).__init__(*args)


class Ccvs(Component_2T):

    def __init__(self, *args):
        super(Ccvs, self).__init__(*args)
        self.parse(self.elements)
        for k in self._args._args.keys():
            setattr(self, "{}".format(k), self._args._args[k])

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
        self._args = Args(elements[5:])

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.vname,
             self.value]
        if self.args:
            l.append(" ".join(self.args))
        return " ".join(l)

    @property
    def args(self):
        return self._args._args

    @args.setter
    def args(self, arg):
        self._args._args = arg

class Isource(Component_2T):
    def __init__(self, *args):
        super(Isource, self).__init__(*args)

    @property
    def current(self):
        return self.value

    @current.setter
    def current(self, arg):
        self.value = arg



class Jfet(Component_3T):
    def __init__(self, *args):
        super(Jfet, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Inductor(Component_2T):
    def __init__(self, *args):
        super(Inductor, self).__init__(*args)

    @property
    def inductance(self):
        return self.value

    @inductance.setter
    def inductance(self, arg):
        self.value = arg


class Mosfet(Component_4T):
    def __init__(self, *args):
        super(Mosfet, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Numerical_device_gss(Default):
    def __init__(self, *args):
        super(Numerical_device_gss, self).__init__(*args)


class Lossy_transmission_line(Component_4T):
    def __init__(self, *args):
        super(Lossy_transmission_line, self).__init__(*args)


class Bjt(Component):
    def __init__(self, *args):
        super(Bjt, self).__init__(*args)

        for i, elem in enumerate(self.elements):
            if "=" in elem:
                i = i-1
                break
        if i == 4:
            self.subs_terminal = False
        elif i == 5:
            self.subs_terminal = True
        else:
            print(self.elements, i)
            raise Exception("Error could not identify BJT device")
        self.parse(self.elements)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg

    def parse(self, elements):
        if self.subs_terminal:
            self.ports = self._assign_ports(elements[1:5])
            self.value = elements[5]
            self.args  = elements[6:]
        else:
            self.ports = self._assign_ports(elements[1:4])
            self.value = elements[4]
            self.args  = elements[5:]

    def __str__(self):
        l = [self.instance,
             *self.ports.values(),
             self.value]
        if self.args:
            l.append(" ".join(self.args))
        return " ".join(l)


class Resistor(Component_2T):
    def __init__(self, *args):
        super(Resistor, self).__init__(*args)

    @property
    def resistance(self):
        return self.value

    @resistance.setter
    def resistance(self, arg):
        self.value = arg


class Vcsw(Component_4T):
    def __init__(self, *args):
        super(Vcsw, self).__init__(*args)


class Lossless_transmission_line(Component_4T):
    def __init__(self, *args):
        super(Lossless_transmission_line, self).__init__(*args)


class Uniformely_distributed_rc_line(Component_3T):
    def __init__(self, *args):
        super(Uniformely_distributed_rc_line, self).__init__(*args)


class Vsource(Component_2T):
    def __init__(self, *args):
        super(Vsource, self).__init__(*args)

    @property
    def voltage(self):
        return self.value

    @voltage.setter
    def voltage(self, arg):
        self.value = arg


class Icsw(Component_2T):
    def __init__(self, *args):
        super(Icsw, self).__init__(*args)


class Subckt(Component):
    def __init__(self, *args):
        super(Subckt, self).__init__(*args)



class Single_lossy_transmission_line(Component_4T):
    def __init__(self, *args):
        super(Single_lossy_transmission_line, self).__init__(*args)


class Mesfet(Component_3T):
    def __init__(self, *args):
        super(Mesfet, self).__init__(*args)

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


#--------------------------------------------------------------------------------
# Element Mapping
#--------------------------------------------------------------------------------

ELEMENTMAP = {"*":          Comment,
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


#--------------------------------------------------------------------------------
# Circuit Class
#--------------------------------------------------------------------------------

class Circuit:
    """ Circuit represents a SPICE netlist.

    Required inputs:
    ----------------
    netlist  (str):     spice netlist or path to a spice netlist.


    Optional inputs:
    ----------------
    is_netlist (bool):  Indicator if netlist is a filepath or actual netlist.
                        Default assumes a path.

    Description
    ----------------
    Netlist is a high-level object of any ordinary spice netlist.
    It contains each circuit element as a parsed and understood element
    with its specific configuration, parameters and ports..
    """

    def __init__(self, netlist=None, is_filename=True):
        if netlist:
            if is_filename:
                self.name = netlist
                self._netlist = read_netlist(netlist)
            else:
                self.name = "Netlist"
                self._netlist = clean_netlist(netlist)


        else:
            self.name = "Netlist"
            self._netlist = []

        self.parsed_circuit = self.parse(self._netlist)
        self.circuit = copy.deepcopy(self.parsed_circuit)
        self._synthesize()

        for elem in ELEMENTMAP.values():
            if elem:
                elemname = (elem.__name__).lower()
                setattr(self, "{}s".format(elemname), self._attr(elem))


    def __str__(self):
        return self.netlist


    def __len__(self):
        return len(self.circuit)


    def __add__(self, other):
        self.append(other)
        return self.circuit


    def __setitem__(self, key, item):
        self.circuit[key] = item


    def __getitem__(self, key):
        return self.circuit[key]


    def __iter__(self):
        return iter(self.circuit.keys())


    def _attr(self, elemtype):
        values = []
        for uid in self.circuit:
            if isinstance(self.circuit[uid], elemtype):
                values.append(self.circuit[uid])
        return values


    @property
    def netlist(self):
        """ Simulation ready circuit netlist """
        self._synthesize()
        return "".join(self._netlist)


    def reset(self):
        """ Reset the circuit to the initially parsed circuit. """
        self.circuit = copy.deepcopy(self.parsed_circuit)


    def parse(self, netlist):
        """ Parse the string netlist into a circuit representation.

        Required inputs:
        ----------------
        netlist (str, list):    Spice netlist


        Returns
        ----------------
        elements (dict):        dict of circuit elements. Where
                                the key is the uid (unique id).
        """

        elements = dict()
        ctlsec = False
        hierarchy = collections.deque()
        hierarchy.append("root")

        regex_nreq        = re.compile("^$|^\.end$")
        reqex_subckt_s    = re.compile("^.subckt*")
        reqex_subckt_e    = re.compile("^.ends.*")
        reqex_control_s   = re.compile("^.control")
        reqex_control_e   = re.compile("^.endc")

        n = 0
        for line in netlist:

            if not re.match(regex_nreq, line):

                if re.match(reqex_subckt_s, line):
                    hierarchy.append(line.split(" ")[1])

                if re.match(reqex_control_s, line) or ctlsec:
                    ctlsec = True
                    if re.match(reqex_control_e, line):
                        ctlsec = False

                else:
                    elemtype = identify_linetype(line)
                    location = "/".join(hierarchy)

                    if elemtype == "param":
                        lines = dissect_param(line)
                        for line in lines:
                            uid = get_uid(line, n)
                            element = ELEMENTMAP[elemtype]
                            elements[uid] = element(line, location, n, uid)
                    else:
                        uid = get_uid(line, n)
                        element = ELEMENTMAP[elemtype]
                        elements[uid] = element(line, location, n, uid)
                if re.match(reqex_subckt_e, line):
                    hierarchy.pop()
            n = n + 1;
        return elements


    def _synthesize(self):
        """ Create a netlist from a circuit representation.

        Description
        ----------------
        Reverse of parse(). It generates a netlist from a list from
        the circuit object.
        """
        netlist = [ "* {}\n\n".format(self.name) ]
        for uid in self.circuit:
            netlist.append("{}\n".format(self.circuit[uid]))
        self._netlist = netlist


    def append(self, line):
        """ Append an element to the Circuit.

        Required inputs:
        ----------------
        line (str):     spice netlist line

        """
        parsed = self.parse(line)
        last = list(self.circuit.keys())[-1]
        if last:
            n = self.circuit[last].n + 1
        else:
            n = 0
        for i, uid_parsed in enumerate(parsed):
            uid = get_uid(line, i)
            parsed[uid_parsed].n = n + i
            self.circuit[uid] = parsed[uid_parsed]


    def write(self, filename):
        """ Write the netlist to file

        Optional inputs:
        ----------------
        filename (str):     name of the output file
        """
        with open(filename, "w") as ofile:
            ofile.write("* Netlist written: {}\n".format(datetime.datetime.now()))
            ofile.write(self.netlist)


    def filter(self, key, val, uids=[]):
        """ Filter circuit elements by regex.

        Required inputs:
        ----------------
        key (str):          property to filter
        val (str):          regex for filter

        Required inputs:
        ----------------
        uids (list):        List of preselected circuit element
                            uids (unique id's).

        Returns
        ----------------
        uids (list):        List of uid's that matches the
                            criteria.
        """
        return filter(self.circuit, key, val, uids)


    def apply(self, func, uids, **kwargs):
        """ Apply function to matching circuit elements.

        Required inputs:
        ----------------
        func (func):         Function to apply.
        uids (list):         List of circuit element.


        Description
        ----------------
        If func modifies the the object it will alter the internal
        circuit representation also!
        kwargs are passed along to func.
        """
        for uid in uids:
            element = self.circuit[uid]
            self.circuit[uid] = func(element, **kwargs)


    def touches(self, expr):
        """ Find circuit elements that touch a net.

        Required inputs:
        ----------------
        expr (str):        net name expression to match

        Returns
        ----------------
        uids (list):        List of uid's that matches the
                            criteria.
        """
        return touches(self.circuit, expr)


    def count_nets(self):
        """ Count the number of port connections to any net.

        Returns
        ----------------
        nets(dict): dictionary with net, count pairs.

        """
        return count_nets(self.circuit, expr)


def dissect_param(line):
    elements = line.split(" ")
    lines = []
    for i, elem in enumerate(elements):
        if "=" in elem:
            lines.append(".param {}".format(elem))
    return lines


def touches(circuit, expr):
    """ Find circuit elements that touch a net.

    Required inputs:
    ----------------
    circuit (Circuit): Circuit object to analyze.
    expr (str):        net name expression to match


    Returns
    ----------------
    uids (list):        List of uid's that matches the
                        criteria.
    """
    uids = []
    for k in circuit:
        ports = circuit[k].ports
        for p in ports:
            if re.fullmatch(expr, ports[p]):
                uids.append(k)
    return uids


def count_nets(circuit):
    """ Count the number of port connections to any net.

    Required inputs:
    ----------------
    circuit (Circuit): Circuit object to analyze.

    Returns
    ----------------
    nets(dict): dictionary with net, count pairs.

    """
    nets = {}
    for k,v in circuit.items():
        pdict = v.ports
        if pdict:
            for node in pdict:
                net = pdict[node]
                if net in nets:
                    nets[net] += 1
                else:
                    nets[net] = 1
    return nets


def filter(circuit, key, val, uids=[]):
    """ Filter circuit elements by regex.

    Required inputs:
    ----------------
    circuit (Circuit):  Circuit object to filter.
    key (str):          property to filter
    val (str):          regex for filter


    Required inputs:
    ----------------
    uids (list):        List of preselected circuit element
                        uids (unique id's).

    Returns
    ----------------
    matches (list):     List of uid's that matches the
                        criteria.
    """
    if uids:
        iterable = uids
    else:
        iterable = circuit
    uids = []
    for uid in iterable:
        if key in circuit[uid].__dir__():
            if re.fullmatch(val, str(getattr(circuit[uid], key))):
                uids.append(uid)
    return uids


def unpack_args(args):
    """ Unpack circuit element arguments.

    Required inputs:
    ----------------
    args (list):        Circuit element arguments

    Returns
    ----------------
    unpacked (dict):    Circuit element arguments as dictionary.
                        if there is no assigment (=) then the value
                        is simply None.
    """
    unpacked = dict()
    for elem in args:
        s = elem.split("=",1)
        if len(s) == 1:
            unpacked[s[0]] = None
        else:
            unpacked[s[0]] = s[1]
    return unpacked


def repack_args(args):
    """ Repackage circuit element arguments.

    Required inputs:
    ----------------
    args (dict):        Circuit element arguments as dict

    Returns
    ----------------
    repacked (list):    Circuit element arguments as list
    """
    repacked = []
    for k in args:
        if args[k]:
            repacked.append("{}={}".format(k, args[k]))
        else:
            repacked.append("{}".format(k))
    return repacked


def replace_argument(uid, cir, key, val):
    """ Replace an argument of a circuit element.

    Required inputs:
    ----------------
    uid (str):              Unique identfier of the circuit
                            element.
    cir (CircuitSection):   circuit section in which to replace
                            the argument.
    key (str):              key to identify the argument that is
                            to be replaced.
    val (str):              The value that is inserted as a
                            replacement for the key.

    Returns
    ----------------
    cir (CircuitSection):   circuit section where the argument
                            has been replaced.
    """
    args = unpack_args(cir[uid].args)
    if args[key]:
        args[key] = val
    else:
        replacement = {key: val}
        for k, v in list(args.items()):
            args[replacement.get(k, k)] = args.pop(k)
            tmp = dict()
            for k in args:
                if k == key:
                    tmp[k.upper()] = args[k]
                else:
                    tmp[k] = args[k]
            args = tmp
    args = repack_args(args)
    cir[uid].args = args
    return cir


def read_netlist(filename):
    """ Read a netlist from file.

    Required inputs:
    ----------------
    filename (str):         Name/path of the netlist file.

    Returns
    ----------------
    clean_netlist (str):    Netlist that has been made uniform
                            through the input cleanup process.
    """
    with open(filename, "r") as ifile:
        netlist = ifile.read()
    return clean_netlist(netlist)


def clean_netlist(netlist):
    """ Cleanup a netlist.

    Required inputs:
    ----------------
    netlist (str, list):    Netlist as a single string or list of lines.


    Returns
    ----------------
    netlist (str):          The cleaned netlist


    Description
    ----------------
    This function will cleanup a netlist and unify it such that
    it can be processed in a reliable manner.

    The order of the individual steps matters! Be careful
    when changing something that the order is preserved and
    makes sense.
    """

    # regex_ignore      = re.compile("^\+\s*$|^\s{,}$") # keeps space
    regex_ignore        = re.compile("^\+\s*$|^\s{,}$|^\*.*$")
    regex_eolcomment    = re.compile("\$.*")
    regex_contline      = re.compile("^\+")
    regex_contlin_ws    = re.compile("^\+\s{,}")
    regex_space         = re.compile("\t| {1,}")
    regex_assign_space  = re.compile(" {,}= {,}")
    regex_comma_space   = re.compile(", {1,}")
    regex_include       = re.compile("^.include.*")

    if isinstance(netlist, str):
        netlist = netlist.split("\n")

    netlist = [line.lstrip() for line in netlist]

    # Remove emtpy continued (+) lines, emtpy lines
    # and comments.
    netlist_a0 = []
    for line in netlist:
        if not re.match(regex_ignore, line):
            netlist_a0.append(line)

    # Remove end of line comments
    netlist_a = [re.sub(regex_eolcomment, "", line) for line in netlist_a0]

    # Combine split lines back to one
    netlist_b = []
    for line in netlist_a:
        if re.match(regex_contline, line):
            netlist_b[-1] = netlist_b[-1] + re.sub(regex_contlin_ws, " ", line)
        else:
            netlist_b.append(line)

    # Unify Whitespace
    netlist_c = [re.sub(regex_space, " ", line) for line in netlist_b]

    # Remove whitespace inside expression
    netlist_d = [remove_enclosed_space(line) for line in netlist_c]

    # Remove space around assignments
    netlist_e = [re.sub(regex_assign_space, "=", line) for line in netlist_d]

    # Remove space after comma
    netlist_f = [re.sub(regex_comma_space, ",", line) for line in netlist_e]

    # Lowercase all letters unless .include statement
    netlist_g = []
    for line in netlist_f:
        if re.match(regex_include, line):
            netlist_g.append(line)
        else:
            netlist_g.append(line.lower())

    return [x.strip() for x in netlist_g]


def identify_linetype(line):
    """ Identify the type of line.

    Required inputs:
    ----------------
    line (str):     spice netlist line

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
    if not elemtype in ELEMENTMAP.keys():
        raise Exception("Linetype not understood by parser")
    else:
        return elemtype


def process_statement(line):
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


def remove_enclosed_space(string):
    """ Remove whitespace enclosed in single quotes

    Required inputs:
    ----------------
    string (str):   A string from which the whitespace is to be removed.


    Returns
    ----------------
    string (str):   String with whitespace between single quotes removed.

    """
    state = False
    parsed = []
    for c in string:
        if c == "'":
            if state:
                state = False
            else:
                state = True
            parsed.append(c)
        else:
            if state:
                if c == " ":
                    pass
                else:
                    parsed.append(c)
            else:
                parsed.append(c)
    return "".join(parsed)


def get_uid(s, i):
    """ Create a uid.

    Required inputs:
    ----------------
    s (str):   A string.
    i (str):   A number.

    Returns
    ----------------
    uid (str): uid (unique identifier)
    """
    s = (str(i) + s).encode()
    return hashlib.md5(s).hexdigest()
