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

import re
import copy
import datetime
import collections


from spatk.helpers import (read_netlist, 
                           repack_args, 
                           dissect_param,
                           clean_netlist,
                           filter,
                           touches,
                           count_nets,
                           element_types,
                           get_uid)

from spatk.elements import elementmap, identify_linetype


class Circuit:
    """ Circuit represents a abstract SPICE netlist.

    Required inputs:
    ----------------
    netlist  (str, list):   SPICE netlist or path to a spice netlist.


    Optional inputs:
    ----------------
    is_netlist (bool):      Indicator if netlist is a filepath or actual 
                            netlist. Default assumes a path.
                            If this is set the input netlist needs to 
                            be a netlist as a string or a list of strings.

    Description
    ----------------
    Circuit is a abstract netlist representation.
    It contains each circuit element as a parsed and understood element
    with its specific configuration, parameters and ports etc.

    Each individual Circuit element can be accessed using its 
    unqiue id (uid).

    To convert the Circuit back into the netlist format simply cast 
    it into a string or access the netlist property of Circuit.
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

        for elem in elementmap.values():
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
        """ SPICE netlist representation of Circuit. """
        self._synthesize()
        return "".join(self._netlist)


    def reset(self):
        """ Reset the Circuit to the initially parsed Circuit. """
        self.circuit = copy.deepcopy(self.parsed_circuit)


    def parse(self, netlist):
        """ Parse the string netlist into a circuit representation.

        Required inputs:
        ----------------
        netlist (str, list):    SPICE netlist.


        Returns
        ----------------
        elements (dict):        dict of circuit elements. Where
                                the key is the uid (unique id).
        """

        elements = dict()
        ctlsec = False
        hierarchy = collections.deque()
        hierarchy.append("root")
        library = None

        regex_nreq          = re.compile(r"^$|^\.end$")
        reqex_subckt_s      = re.compile(r"^.subckt*")
        reqex_subckt_e      = re.compile(r"^.ends.*")
        reqex_control_s     = re.compile(r"^.control")
        reqex_control_e     = re.compile(r"^.endc")
        reqex_library_def_s = re.compile(r"^.lib [a-zA-Z0-9_.-]*$") 
        reqex_library_def_e = re.compile(r"^.endl.*")

        n = 0

        if isinstance(netlist, str):
            netlist = [netlist]

        for line in netlist:

            if not re.match(regex_nreq, line):

                if re.match(reqex_subckt_s, line):
                    hierarchy.append(line.split(" ")[1])

                if re.match(reqex_library_def_s, line):
                    library = line.split(" ")[1]

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
                            element = elementmap[elemtype]
                            elements[uid] = element(line, location, library, n, uid)
                    else:
                        uid = get_uid(line, n)
                        element = elementmap[elemtype]
                        elements[uid] = element(line, location, library, n, uid)

                if re.match(reqex_subckt_e, line):
                    hierarchy.pop()

                if re.match(reqex_library_def_e, line):
                    library = None

            n = n + 1;
        return elements


    def _synthesize(self):
        """ Create a netlist from a circuit representation.

        Description
        ----------------
        Reverse of parse(). It generates a netlist from a the
        internal Circuit representation.

        """
        netlist = [ "* {}\n\n".format(self.name) ]
        for uid in self.circuit:
            netlist.append("{}\n".format(self.circuit[uid]))
        self._netlist = netlist


    def append(self, line):
        """ Append an element to the Circuit.

        Required inputs:
        ----------------
        line (str):     SPICE netlist line.
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
        filename (str):     Name of the output file.
        """
        with open(filename, "w") as ofile:
            ofile.write("* Netlist written: {}\n".format(datetime.datetime.now()))
            ofile.write(self.netlist)


    def filter(self, key, val, uids=[]):
        """ Filter circuit elements by regex.

        Required inputs:
        ----------------
        key (str):          Property to filter.
        val (str):          Regex to match.


        Optional inputs:
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
        """ Apply function to circuit elements.

        Required inputs:
        ----------------
        func (func):    Function to apply.
        uids (list):    List of circuit element.


        Description
        ----------------
        If func modifies the the object it will alter the internal
        circuit representation also! kwargs are passed along to func.
        """
        for uid in uids:
            element = self.circuit[uid]
            self.circuit[uid] = func(element, **kwargs)


    def touches(self, expr):
        """ Find circuit elements that touch a net.

        Required inputs:
        ----------------
        expr (str):        net name expression to match.


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
        return count_nets(self.circuit)


    def element_types(self):
        """ Find which elements are contained in a circuit.

        Returns
        ----------------
        elements (set): set of element types in circuit.
        """
        return element_types(self.circuit)
