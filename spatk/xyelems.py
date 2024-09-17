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
                            Comment,
                            Function, 
                            Global, 
                            Include,
                            Library, 
                            Model,
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
                            Isource,
                            Jfet,
                            Lossless_transmission_line,
                            Lossy_transmission_line,
                            Mesfet,
                            Mosfet,
                            Resistor, 
                            Subckt,
                            SubcktDef,
                            Vccs,
                            Vcsw,
                            Vcvs,
                            Vsource)

#----------------------------------------------------------------------
# Xyce element classes
#----------------------------------------------------------------------

class Option(Statement):
    """ .option Statement. """
    def __init__(self, *args):
        super(Option, self).__init__(*args)

    @property
    def pkg(self):
        return self.elements[1]

    @pkg.setter
    def pkg(self, arg):
        self.elements[1] = arg


    @property
    def setting(self):
        return self.elements[2].split("=")[0]

    @pkg.setter
    def pkg(self, arg):
        s = self.elements[2].split("=", 1)[0]
        self.elements[2] = "{}={}".format(arg,s[1])


#----------------------------------------------------------------------
# Xyce Element Mapping
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
              "subckt":     SubcktDef,
              "A":          None,
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
              "N":          None,
              "O":          Lossy_transmission_line,
              "P":          None,
              "Q":          Bjt,
              "R":          Resistor,
              "S":          Vcsw,
              "T":          Lossless_transmission_line,
              "U":          None,
              "V":          Vsource,
              "W":          Icsw,
              "X":          Subckt,
              "XC":         Capacitor,
              "XM":         Mosfet,
              "YPDE":       None,
              "YACC":       None,
              "YLIN":       None,
              "YMEMRISTOR": None,
              "Y":          None,
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
    elif identifier in [".subckt"]:
        return "subckt"
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
    if letter_1 != "*":
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
