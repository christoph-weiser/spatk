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
                            Subckt,
                            SubcktDef, 
                            Include,
                            Library,
                            Model,
                            Option,
                            Param,
                            Global,
                            Capacitor,
                            Diode,
                            Mosfet,
                            Vccs,
                            Vcvs,
                            Cccs,
                            Ccvs,
                            Isource,
                            Jfet,
                            Inductor,
                            Bjt,
                            Resistor,
                            Vsource,
                            )


#----------------------------------------------------------------------
# Hspice element classes
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


#----------------------------------------------------------------------
# Hspice Element Mapping
#----------------------------------------------------------------------

elementmap = {"*":          Comment,
              ".":          Statement,
              "model":      Model,
              "include":    Include,
              "library":    Library,
              "option":     Option,
              "param":      Param,
              "temp":       Temp,
              "global":     Global,
              "subckt":     SubcktDef,
              "A":          None,
              "B":          None,
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
              "O":          None,
              "P":          None,
              "Q":          Bjt,
              "R":          Resistor,
              "S":          None,
              "T":          None,
              "U":          None,
              "V":          Vsource,
              "W":          None,
              "X":          Subckt,
              "XC":         Capacitor,
              "XM":         Mosfet,
              "Y":          None,
              "Z":          None}


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
    elif identifier in [".temp"]:
        return "temp"
    elif identifier in [".option"]:
        return "option"
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
