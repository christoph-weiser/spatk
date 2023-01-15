# SPATK - A spice netlist toolkit.
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

class Default():
    def __init__(self, line, location, n, uid):
        self.line = line
        self.location = location
        self.uid = uid
        self.n = n
        self.instance = None
        self.type = None
        self.ports = list()
        self.value = None

    def __str__(self):
        return self.line


class Component():
    def __init__(self, line, location, n, uid):
        self.elements = line.split(" ")
        self.location = location
        self.uid = uid
        self.n = n
        self.instance = self.elements[0]
        self.type = None
        self.ports = dict()
        self.value = None

    def __str__(self):
        pass

    def parse(self, line):
        pass


class Component_2T(Component):
    def __init__(self, *args):
        super(Component_2T, self).__init__(*args)
        self.parse(self.elements)

    def parse(self, elements):
        self.ports = {"n1": elements[1],
                      "n2": elements[2]}
        self.value = elements[3]
        self.args  = elements[4:]

    def __str__(self):
        l = [self.instance,
             self.ports["n1"],
             self.ports["n2"],
             self.value,
             " ".join(self.args)]
        return " ".join(l)


class Component_3T(Component):
    def __init__(self, *args):
        super(Component_3T, self).__init__(*args)
        self.parse(self.elements)

    def parse(self, elements):
        self.ports = {"n1": elements[1],
                      "n2": elements[2],
                      "n3": elements[3]}
        self.value = elements[4]
        self.args  = elements[5:]

    def __str__(self):
        l = [self.instance,
             self.ports["n1"],
             self.ports["n2"],
             self.ports["n3"],
             self.value,
             " ".join(self.args)]
        return " ".join(l)


class Component_4T(Component):
    def __init__(self, *args):
        super(Component_4T, self).__init__(*args)
        self.parse(self.elements)

    def parse(self, elements):
        self.ports = {"n1": elements[1],
                      "n2": elements[2],
                      "n3": elements[3],
                      "n4": elements[4]}
        self.value = elements[5]
        self.args  = elements[6:]

    def __str__(self):
        l = [self.instance,
             self.ports["n1"],
             self.ports["n2"],
             self.ports["n3"],
             self.ports["n4"],
             self.value,
             " ".join(self.args)]
        return " ".join(l)

#----------------------------------------------------------------------
# Element Classes
#----------------------------------------------------------------------

class Comment(Default):
    def __init__(self, *args):
        super(Comment, self).__init__(*args)
        self.type = "comment"


class Statement(Default):
    def __init__(self, *args):
        super(Statement, self).__init__(*args)
        self.type = "statement"


class Xspice(Default):
    def __init__(self, *args):
        super(Xspice, self).__init__(*args)
        self.type = "xspice"


class Behavioral_source(Default):
    def __init__(self, *args):
        super(Behavioral_source, self).__init__(*args)
        self.type = "behavioral source"


class Capacitor(Component_2T):
    def __init__(self, *args):
        super(Capacitor, self).__init__(*args)
        self.parse(self.elements)
        self.type = "capacitor"

    @property
    def capacitance(self):
        return self.value

    @capacitance.setter
    def capacitance(self, arg):
        self.value = arg


class Diode(Component_2T):
    def __init__(self, *args):
        super(Diode, self).__init__(*args)
        self.parse(self.elements)
        self.type = "diode"

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Vcvs(Component_4T):
    def __init__(self, *args):
        super(Vcvs, self).__init__(*args)
        self.parse(self.elements)
        self.type = "vcvs"


class Cccs(Component_2T):
    def __init__(self, *args):
        super(Cccs, self).__init__(*args)
        self.parse(self.elements)
        self.type = "Cccs"
        self.value = self.elements[4]

    @property
    def vname(self):
        return self.self.elements[3]

    @vname.setter
    def vname(self, arg):
        self.elements[3] = arg


class Vccs(Component_4T):
    def __init__(self, *args):
        super(Vccs, self).__init__(*args)
        self.parse(self.elements)
        self.type = "vccs"


class Ccvs(Component_2T):
    def __init__(self, *args):
        super(Ccvs, self).__init__(*args)
        self.parse(self.elements)
        self.type = "ccvs"
        self.value = self.elements[4]

    @property
    def vname(self):
        return self.self.elements[3]

    @vname.setter
    def vname(self, arg):
        self.elements[3] = arg


class Isource(Component_2T):
    def __init__(self, *args):
        super(Isource, self).__init__(*args)
        self.parse(self.elements)
        self.type = "isource"

    @property
    def current(self):
        return self.value

    @current.setter
    def current(self, arg):
        self.value = arg



class Jfet(Component_3T):
    def __init__(self, *args):
        super(Jfet, self).__init__(*args)
        self.parse(self.elements)
        self.type = "jfet"

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Inductor(Component_2T):
    def __init__(self, *args):
        super(Inductor, self).__init__(*args)
        self.parse(self.elements)
        self.type = "inductor"

    @property
    def inductance(self):
        return self.value

    @inductance.setter
    def inductance(self, arg):
        self.value = arg



class Mosfet(Component_4T):
    def __init__(self, *args):
        super(Mosfet, self).__init__(*args)
        self.parse(self.elements)
        self.type = "mosfet"

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


class Numerical_device_gss(Default):
    def __init__(self, *args):
        super(Numerical_device_gss, self).__init__(*args)
        self.type = "numerical device gss"


class Lossy_transmission_line(Component_4T):
    def __init__(self, *args):
        super(Lossy_transmission_line, self).__init__(*args)
        self.parse(self.elements)
        self.type = "lossy transmission line"


class Bjt(Component):
    def __init__(self, *args):
        super(Bjt, self).__init__(*args)
        self.type = "bjt"

        for i, elem in enumerate(self.elements):
            if "=" in elem:
                break
        if i == 5:
            self.subs_terminal = False
        elif i == 6:
            self.subs_terminal = True
        else:
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
            self.ports = {"n1": elements[1],
                          "n2": elements[2],
                          "n3": elements[3],
                          "n4": elements[4]}
            self.value = elements[5]
            self.args  = elements[6:]
        else:
            self.ports = {"n1": elements[1],
                          "n2": elements[2],
                          "n3": elements[3]}
            self.value = elements[4]
            self.args  = elements[5:]


    def __str__(self):
        if self.subs_terminal:
            l = [self.instance,
                 self.ports["n1"],
                 self.ports["n2"],
                 self.ports["n3"],
                 self.ports["n4"],
                 self.value,
                 " ".join(self.args)]
        else:
            l = [self.instance,
                 self.ports["n1"],
                 self.ports["n2"],
                 self.ports["n3"],
                 self.value,
                 " ".join(self.args)]
        return " ".join(l)


class Resistor(Component_2T):
    def __init__(self, *args):
        super(Resistor, self).__init__(*args)
        self.parse(self.elements)
        self.type = "resistor"

    @property
    def resistance(self):
        return self.value

    @resistance.setter
    def resistance(self, arg):
        self.value = arg



class Vcsw(Component_4T):
    def __init__(self, *args):
        super(Vcsw, self).__init__(*args)
        self.parse(self.elements)
        self.type = "vcsw"


class Lossless_transmission_line(Component_4T):
    def __init__(self, *args):
        super(Lossless_transmission_line, self).__init__(*args)
        self.parse(self.elements)
        self.type = "lossless transmission line"


class Uniformely_distributed_rc_line(Component_3T):
    def __init__(self, *args):
        super(Uniformely_distributed_rc_line, self).__init__(*args)
        self.parse(self.elements)
        self.type = "uniformely distributed rc line"


class Vsource(Component_2T):
    def __init__(self, *args):
        super(Vsource, self).__init__(*args)
        self.parse(self.elements)
        self.type = "vsource"

    @property
    def voltage(self):
        return self.value

    @voltage.setter
    def voltage(self, arg):
        self.value = arg


class Icsw(Component_2T):
    def __init__(self, *args):
        super(Icsw, self).__init__(*args)
        self.parse(self.elements)
        self.type = "icsw"


class Subcircuit(Component):
    def __init__(self, *args):
        super(Subcircuit, self).__init__(*args)
        self.type = "subcircuit"

    def __str__(self):
        return " ".join(self.elements)


class Single_lossy_transmission_line(Component_4T):
    def __init__(self, *args):
        super(Single_lossy_transmission_line, self).__init__(*args)
        self.parse(self.elements)
        self.type = "single lossy transmission line"


class Mesfet(Component_3T):
    def __init__(self, *args):
        super(Mesfet, self).__init__(*args)
        self.parse(self.elements)
        self.type = "mesfet"

    @property
    def model(self):
        return self.value

    @model.setter
    def model(self, arg):
        self.value = arg


#--------------------------------------------------------------------------------
# Element Mapping
#--------------------------------------------------------------------------------

ELEMENTMAP = {"*":  Comment,
              ".":  Statement,
              "A":  Xspice,
              "B":  Behavioral_source,
              "C":  Capacitor,
              "D":  Diode,
              "E":  Vcvs,
              "F":  Cccs,
              "G":  Vccs,
              "H":  Ccvs,
              "I":  Isource,
              "J":  Jfet,
              "K":  None,
              "L":  Inductor,
              "M":  Mosfet,
              "N":  Numerical_device_gss,
              "O":  Lossy_transmission_line,
              "P":  None,
              "Q":  Bjt,
              "R":  Resistor,
              "S":  Vcsw,
              "T":  Lossless_transmission_line,
              "U":  Uniformely_distributed_rc_line,
              "V":  Vsource,
              "W":  Icsw,
              "X":  Subcircuit,
              "XC": Capacitor,
              "XM": Mosfet,
              "Y":  Single_lossy_transmission_line,
              "Z":  Mesfet}


#--------------------------------------------------------------------------------
# Circuit Class
#--------------------------------------------------------------------------------

class Circuit():
    """ Circuit represents a spice netlist.

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
    The object allows however to filter the netlist elements by their type
    arguments and ports.

        name:           When read from file filename, otherwise this can be
                        used a identifier and will be writen to the first line
                        of the netlist object.

        parsed_circuit: This variable holds a string with the original netlist

        circuit:        A list of all the netlist elements in a dict fashion
                        with "instance", "type",  "ports",  "args" keys.

        netlist:        A spice netlist generated from the "circuit" list/dict.
    """

    def __init__(self, netlist=None, is_filename=True):
        if netlist:
            if is_filename:
                self.name = netlist
                self._netlist = read_netlist(netlist)
            else:
                self.name = "Netlist"
                self._netlist = netlist
        else:
            self.name = "Netlist"
            self._netlist = []

        self.parsed_circuit = self.parse(self._netlist)
        self.circuit = copy.deepcopy(self.parsed_circuit)
        self.synthesize()


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


    @property
    def netlist(self):
        """ Simulation ready circuit netlist """
        self.synthesize()
        return "".join(self._netlist)


    def reset(self):
        """ Reset the circuit to the first parsed circuit. """
        self.circuit = copy.deepcopy(self.parsed_circuit)


    def parse(self, netlist):
        """ Parse the string netlist into a circuit representation.

        Required inputs:
        ----------------
        netlist (str, list):    Spice netlist


        Returns
        ----------------
        elements (dict):        dict of circuit elements. Where
                                the key is the uid.
        """
        elements = dict()
        if isinstance(netlist, str):
            netlist = netlist.split("\n")
        inside_ctl_section=False
        hierarchy = collections.deque()
        hierarchy.append("root")
        for i,line in enumerate(netlist):
            line = line.strip()
            if not re.match("^$|^\.end$|^\s*\*", line):
            # if not re.match("^$|^\.end$", line): # Keep comments
                if re.match("^.subckt*", line):
                    hierarchy.append(line.split(" ")[1])
                if re.match("^.control", line) or inside_ctl_section:
                    inside_ctl_section = True
                    if re.match("^.endc", line):
                        inside_ctl_section = False
                else:
                    elemtype = identify_linetype(line)
                    uid = (hashlib.md5((str(i)+line).encode())).hexdigest()
                    location = "/".join(hierarchy)
                    element =  ELEMENTMAP[elemtype]
                    instance = element(line, location, i, uid)
                    elements[uid] = instance
                if re.match("^.ends.*", line):
                    hierarchy.pop()
        return elements


    def synthesize(self):
        """ Create a netlist from a circuit representation.

        Description
        ----------------
        Reverse of parse(). It generates a netlist from a list from
        the circuit object.
        Synthesize will update the object internal netlist when called.

        """
        netlist = [ "* {}\n\n".format(self.name) ]
        for uid in self.circuit:
            netlist.append("{}\n".format(self.circuit[uid]))
        self._netlist = netlist


    def append(self, line):
        """ Append an element to the circuit dict.

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
            uid = (hashlib.md5((str(i)+line).encode())).hexdigest()
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


    def filter(self, filt):
        """ Filter circuit elements by regex.

        Required inputs:
        ----------------
        filt (tuple):       Pair of property and regex

        Returns
        ----------------
        matches (list):     List of uid's that matches the
                            criteria.

        """
        key = filt[0]
        val = filt[1]
        uids = []
        for uid in self.circuit:
            if key in self.circuit[uid].__dir__():
                if re.fullmatch(val, str(getattr(self.circuit[uid], key))):
                    uids.append(uid)
        return uids


    def apply(self, func, filt, **kwargs):
        """ Apply function to matching circuit elements.

        Required inputs:
        ----------------
        func (func):                function to apply to matching elements.
        filt (tuple, list , dict):  pairs of key to circuit element dict
                                    and regex to match in that key.
                                    See also self.filter for more info.

        Returns
        ----------------
        n (int):                    number of modified circuit elements


        Description
        ----------------
        Filter the circuit representation for matching elements.
        Then apply func to all those elements.
        If func modifies the the object it will alter the internal
        circuit representation also!
        kwargs are passed along to func.
        """
        matches = self.filter(filt)
        if matches:
            for uid in matches:
                element = self.circuit[uid]
                self.circuit[uid] = func(element, **kwargs)
        return len(matches)


    def touches(self, expr):
        """ Find circuit elements that touch a net.

        Required inputs:
        ----------------
        expr (str): net name expression to match


        Returns
        ----------------
        uids (list):        List of uid's that matches the
                            criteria.
        """
        uids = []
        for k in self.circuit:
            ports = self.circuit[k].ports
            for p in ports:
                if re.fullmatch(expr, ports[p]):
                    uids.append(k)
        return uids


    def count_nets(self):
        """ Count the number of port connections to any net.

        Returns
        ----------------
        nets(dict): dictionary with net, count pairs.

        """
        nets = {}
        for k,v in self.circuit.items():
            pdict = v.ports
            if pdict:
                for node in pdict:
                    net = pdict[node]
                    if net in nets:
                        nets[net] += 1
                    else:
                        nets[net] = 1
        return nets


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

    if isinstance(netlist, str):
        netlist = netlist.split("\n")

    netlist = [line.lstrip() for line in netlist]

    # Remove emtpy continued (+) lines, emtpy lines
    # and comments.
    netlist_a0 = []
    for line in netlist:
        if not re.match("^\+\s*$|^\s{,}$|^\*.*$",line):
        # if not re.match("^\+\s*$|^\s{,}$",line): # Keep comments
            netlist_a0.append(line)

    # Remove end of line comments
    netlist_a = [re.sub("\$.*", "", line) for line in netlist_a0]

    # Combine split lines back to one
    netlist_b = []
    for line in netlist_a:
        if re.match("^\+",line):
            netlist_b[-1] = netlist_b[-1] + re.sub("^\+\s{,}", " ", line)
        else:
            netlist_b.append(line)

    # Unify Whitespace
    netlist_c = [re.sub("\t| {1,}", " ", line) for line in netlist_b]

    # Remove whitespace inside expression
    netlist_d = [remove_enclosed_space(line) for line in netlist_c]

    # Remove space around assignments
    netlist_e = [re.sub(" {1,}= {1,}", "=", line) for line in netlist_d]

    # Lowercase all letters unless .include statement
    netlist_f = []
    for line in netlist_e:
        if re.match("^.include.*", line):
            netlist_f.append(line)
        else:
            netlist_f.append(line.lower())

    netlist = "\n".join(netlist_f)
    return netlist


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
    else:
        elemtype = letter_1
    if not elemtype in ELEMENTMAP.keys():
        raise Exception("Linetype not understood by parser")
    else:
        return elemtype


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
