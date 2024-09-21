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
# Hspice specific element classes
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
              ".MODEL":     Model,
              ".INC":       Include,
              ".INCLUDE":   Include,
              ".LIB":       Library,
              ".LIBRARY":   Library,
              ".OPTION":    Option,
              ".PARAM":     Param,
              ".TEMP":      Temp,
              ".GLOBAL":    Global,
              ".SUBCKT":    SubcktDef,
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
