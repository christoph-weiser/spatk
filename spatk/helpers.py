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
import hashlib

def dissect_param(line):
    """ Seperate combined .param lines into multiple.

    Required inputs:
    ----------------
    line (str):         parameter statement line.


    Returns
    ----------------
    lines (list):       list of seperated parameters.
    """
    elements = line.split(" ")
    lines = []
    for i, elem in enumerate(elements):
        if "=" in elem:
            lines.append(".param {}".format(elem))
    return lines


def touches(circuit, expr):
    """ Find circuit elements that touch a given net.

    Required inputs:
    ----------------
    circuit (Circuit): Circuit object to analyze.
    expr (str):        Net name expression to match.


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


def element_types(circuit):
    """ Find which elements are contained in a circuit.

    Required inputs:
    ----------------
    circuit (Circuit):  Circuit object to analyze.


    Returns
    ----------------
    elements (set):     Set of element types in circuit.
    """
    elements = set()
    for uid in circuit:
        elements.add(circuit[uid].type)
    return elements


def filter(circuit, key, val, uids=[]):
    """ Filter circuit elements by regex.

    Required inputs:
    ----------------
    circuit (Circuit):  Circuit object to filter.
    key (str):          property to filter.
    val (str):          regex for filter.


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
    args (list):        Circuit element arguments.

    Returns
    ----------------
    unpacked (dict):    Circuit element arguments as dictionary.
                        If there is no assigment (=) then the value
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
    args (dict):        Circuit element arguments.

    Returns
    ----------------
    repacked (list):    Circuit element arguments.
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
    cir (CircuitSection):   Circuit section in which to replace
                            the argument.
    key (str):              Key to identify the argument that is
                            to be replaced.
    val (str):              The value that is inserted as a
                            replacement for the key.

    Returns
    ----------------
    cir (CircuitSection):   Circuit section where the argument
                            has been replaced.
    """
    if cir[uid].args[key]:
        cir[uid].args[key] = val
    else:
        content = cir[uid].args.content
        content[val] = content.pop(key)
        cir[uid].args = Args(content)
    return cir


def read_netlist(filename):
    """ Read a netlist from file and sanitize it.

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


def clean_netlist(netlist, keep_comments=False):
    """ Cleanup a netlist.

    Required inputs:
    ----------------
    netlist (str, list):    Netlist as a single string or list 
                            of lines.

    Optional inputs:
    ----------------
    keep_comments (bool):   Dont remove SPICE comments during cleanup.


    Returns
    ----------------
    netlist (str):          The cleaned netlist


    Description
    ----------------
    This function will cleanup a netlist and unify it such that
    it can be processed in a reliable manner.

    The order of the individual steps matters! 
    """
    if keep_comments:
        regex_ignore    = re.compile(r"^\+\s*$|^\s{,}$")
    else:
        regex_ignore    = re.compile(r"^\+\s*$|^\s{,}$|^\*.*$")

    regex_eolcomment    = re.compile(r"\$.*")
    regex_contline      = re.compile(r"^\+")
    regex_contlin_ws    = re.compile(r"^\+\s{,}")
    regex_space         = re.compile(r"\t| {1,}")
    regex_assign_space  = re.compile(r" {,}= {,}")
    regex_comma_space   = re.compile(r", {1,}")
    regex_include       = re.compile(r"^.include.*")
    regex_curlybracket  = re.compile(r"[{}]")

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

    # substitue curly brackets with single quotes
    netlist_g = [re.sub(regex_curlybracket, "'", line) for line in netlist_f]

    # Lowercase all letters unless .include statement
    netlist_h = []
    for line in netlist_g:
        if re.match(regex_include, line):
            netlist_h.append(line)
        else:
            netlist_h.append(line.lower())

    return [x.strip() for x in netlist_h]




def remove_enclosed_space(string):
    """ Remove whitespace enclosed in single quotes.

    Required inputs:
    ----------------
    string (str):   A string from which the whitespace 
                    is to be removed.


    Returns
    ----------------
    string (str):   String with whitespace between 
                    single quotes removed.
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
    """ Create a uid (unique identifier).

    Required inputs:
    ----------------
    s (str):   A string.
    i (str):   A number.


    Returns
    ----------------
    uid (str): uid .
    """
    s = (str(i) + s).encode()
    return hashlib.md5(s).hexdigest()
