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

from spatk import SYNTAX

from spatk.genelems import (Args, Default, Component,
                            Component_2T, Component_3T,
                            Component_4T, Statement,
                            Comment)

if SYNTAX == "ngspice":

    from spatk.ngelems import elementmap
    from spatk.ngelems import process_statement, identify_linetype
    from spatk.ngelems import (Model, Include, Library,
                               Option, Function, Param,
                               Global, Xspice, Behavioral_source,
                               Capacitor, Diode, Vcvs, Cccs,
                               Vccs, Ccvs, Isource, Jfet,
                               Inductor, Mosfet, Numerical_device_gss,
                               Lossy_transmission_line, Bjt,
                               Resistor, Vcsw, Lossless_transmission_line,
                               Uniformely_distributed_rc_line,
                               Vsource, Icsw, Subckt,
                               Single_lossy_transmission_line, Mesfet)

elif SYNTAX == "hspice":
    from spatk.helems import elementmap
    from spatk.helems import process_statement, identify_linetype
    from spatk.helems import (Model, Include, Library,
                               Option, Function, Param,
                               Global, Xspice, Behavioral_source,
                               Capacitor, Diode, Vcvs, Cccs,
                               Vccs, Ccvs, Isource, Jfet,
                               Inductor, Mosfet, Numerical_device_gss,
                               Lossy_transmission_line, Bjt,
                               Resistor, Vcsw, Lossless_transmission_line,
                               Uniformely_distributed_rc_line,
                               Vsource, Icsw, Subckt,
                               Single_lossy_transmission_line, Mesfet)

else:
    raise Exception("The choosen syntax format is not supported!")
