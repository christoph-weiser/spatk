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

from spatk import SYNTAX

from spatk.genelems import (Args, Default, Component,
                            Component_2T, Component_3T,
                            Component_4T, Statement,
                            Comment, Subckt, SubcktDef, 
                            Include, Library)


if SYNTAX == "generic":
    from spatk.flavours.generic import elementmap
    from spatk.flavours.generic import (Model, Option, Param,
                                        Global, Behavioral_source,
                                        Capacitor, Diode, Vcvs, Cccs,
                                        Vccs, Ccvs, Isource, Jfet,
                                        Inductor, Mosfet,
                                        Lossy_transmission_line, Bjt,
                                        Resistor, Vcsw, Lossless_transmission_line,
                                        Uniformely_distributed_rc_line,
                                        Vsource, Icsw, Mesfet)

elif SYNTAX == "ngspice":
    from spatk.flavours.ngspice import elementmap
    from spatk.flavours.ngspice import (Model, Option, Function, Temp, Param,
                                        Global, Xspice, Behavioral_source,
                                        Capacitor, Diode, Vcvs, Cccs,
                                        Vccs, Ccvs, Isource, Jfet,
                                        Inductor, Mosfet, Numerical_device_gss,
                                        Lossy_transmission_line, Bjt,
                                        Resistor, Vcsw, Lossless_transmission_line,
                                        Uniformely_distributed_rc_line,
                                        Vsource, Icsw,
                                        Single_lossy_transmission_line, Mesfet)

elif SYNTAX == "hspice":
    from spatk.flavours.hspice import elementmap
    from spatk.flavours.hspice import (Model, Option, Temp, Param, Global,
                                       Capacitor, Diode, Vcvs, Cccs,
                                       Vccs, Ccvs, Isource, Jfet,
                                       Inductor, Mosfet, Bjt,
                                       Resistor, Vsource )

elif SYNTAX == "xyce":
    from spatk.flavours.xyce import elementmap
    from spatk.flavours.xyce import (Model, Option, Function, Param,
                                     Global, Behavioral_source,
                                     Capacitor, Diode, Vcvs, Cccs,
                                     Vccs, Ccvs, Isource, Jfet,
                                     Inductor, Mosfet,
                                     Lossy_transmission_line, Bjt,
                                     Resistor, Vcsw, Lossless_transmission_line,
                                     Vsource, Icsw, Mesfet)

else:
    raise Exception("The choosen syntax format is not supported!")
