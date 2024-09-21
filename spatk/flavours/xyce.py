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
# Xyce specific element classes
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
    def name(self):
        return self.elements[2].split("=")[0]

    @name.setter
    def name(self, arg):
        s = self.elements[2].split("=", 1)[1]
        self.elements[2] = "{}={}".format(arg,s)

    @property
    def value(self):
        print(self.elements[2])
        return self.elements[2].split("=")[1]

    @value.setter
    def value(self, arg):
        s = self.elements[2].split("=", 1)[0]
        self.elements[2] = "{}={}".format(s, arg)



#----------------------------------------------------------------------
# Xyce Element Mapping
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
              ".PARAM":     Param,
              ".GLOBAL":    Global,
              ".SUBCKT":    SubcktDef,
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
