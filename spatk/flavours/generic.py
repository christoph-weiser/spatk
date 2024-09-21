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
                            Statement, 
                            Behavioral_source,
                            Bjt,
                            Capacitor,
                            Cccs,
                            Ccvs, 
                            Diode, 
                            Global, 
                            Icsw,
                            Include, 
                            Inductor,
                            Isource,
                            Jfet,
                            Library, 
                            Lossless_transmission_line,
                            Lossy_transmission_line,
                            Mesfet,
                            Model,
                            Mosfet,
                            Option,
                            Param,
                            Resistor, 
                            Subckt,
                            SubcktDef, 
                            Uniformely_distributed_rc_line,
                            Vccs,
                            Vcsw,
                            Vcvs, 
                            Vsource)



#----------------------------------------------------------------------
# Generic SPICE3 Element Mapping
#----------------------------------------------------------------------

elementmap = {"*":          Comment,
              ".":          Statement,
              ".MODEL":     Model,
              ".SUBCKT":    SubcktDef,
              ".INC":       Include,
              ".INCLUDE":   Include,
              ".LIB":       Library,
              ".LIBRARY":   Library,
              ".OPTION":    Option,
              ".PARAM":     Param,
              ".GLOBAL":    Global,
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
              "U":          Uniformely_distributed_rc_line,
              "V":          Vsource,
              "W":          Icsw,
              "X":          Subckt,
              "Y":          None,
              "Z":          Mesfet}
