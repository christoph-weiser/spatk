# SPATK - Spice Analysis Toolkit.
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

import pytest
import spatk as sp


def test_module_default():
    line = "A Default Line"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Default(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "default")
    assert(isinstance(mod.ports, dict))
    assert(mod._value == None)
    assert(str(mod) == line)
    assert(mod.parse(line) == None)


def test_module_component():
    line = "R1 neta netb 1e3"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Component(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "R1")
    assert(mod.type == "component")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.elements == ["R1", "neta", "netb", "1e3"])


def test_module_component_2t():
    line = "R1 neta netb 1e3"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Component_2T(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "R1")
    assert(mod.type == "component_2t")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "1e3")
    assert(str(mod) == line)
    assert(mod.elements == ["R1", "neta", "netb", "1e3"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])


def test_module_component_3t():
    line = "X1 neta netb netc model_3t"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Component_3T(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "X1")
    assert(mod.type == "component_3t")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "model_3t")
    assert(str(mod) == line)
    assert(mod.elements == ["X1", "neta", "netb", "netc", "model_3t"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc")])


def test_module_component_4t():
    line = "X1 neta netb netc netd model_4t"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Component_4T(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "X1")
    assert(mod.type == "component_4t")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "model_4t")
    assert(str(mod) == line)
    assert(mod.elements == ["X1", "neta", "netb", "netc", "netd", "model_4t"])

    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc"), ("n3", "netd")])


def test_module_statement():
    line = ".include mylib.spice"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Statement(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "statement")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.ports == {})


def test_module_commment():
    line = "* A test comment"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Comment(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "comment")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.ports == {})


def test_module_model():
    line = ".model mymodel model"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Model(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "model")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.ports == {})


def test_module_include():
    line = ".include mylib.spice"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Include(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "include")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.ports == {})


def test_module_library():
    line = ".include lib.spice module"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Library(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "library")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.ports == {})
    assert(mod.filename == "lib.spice")
    assert(mod.libname == "module")
    
    mod.filename == "test.spice"
    assert(mod.filename == "lib.spice")
    mod.libname = "test"
    assert(mod.libname == "test")



def test_module_option():
    line = ".option setting=value"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Option(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "option")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.ports == {})


def test_module_function():
    line = ".func myfunc='expression'"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Function(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "function")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.ports == {})


def test_module_param():
    line = ".param mypar='value'"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Param(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "param")
    assert(isinstance(mod.ports, dict))
    assert(str(mod) == line)
    assert(mod.ports == {})
    assert(mod.value == "'value'")
    assert(mod.name == "mypar")


def test_module_global():
    line = ".global vss vdd"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Global(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == None)
    assert(mod.type == "global")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == None)
    assert(str(mod) == line)
    assert(mod.ports == {})


def test_module_xspice():
    pass


def test_module_behavioral_source():
    pass


def test_module_capacitor():
    line = "C1 neta netb 10e-12"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Capacitor(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "C1")
    assert(mod.type == "capacitor")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "10e-12")
    assert(str(mod) == line)
    assert(mod.elements == ["C1", "neta", "netb", "10e-12"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
    assert(mod.capacitance == "10e-12")

    mod.capacitance = "1e-12"
    assert(mod.capacitance == "1e-12")


def test_module_diode():
    line = "D1 neta netb dmod"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Diode(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "D1")
    assert(mod.type == "diode")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "dmod")
    assert(str(mod) == line)
    assert(mod.elements == ["D1", "neta", "netb", "dmod"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
    assert(mod.model == "dmod")

    mod.model = "dmod_test"
    assert(mod.model == "dmod_test")


def test_module_vcvs():
    pass


def test_module_cccs():
    line = "F1 neta netb vname 1"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Cccs(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "F1")
    assert(mod.type == "cccs")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "1")
    assert(str(mod) == line)
    assert(mod.elements == ["F1", "neta", "netb", "vname", "1"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
    assert(mod.vname == "vname")

    mod.vname = "vname_test"
    assert(mod.vname == "vname_test")

    mod.value = "1000"
    assert(mod.value == "1000")


def test_module_vccs():
    pass


def test_module_ccvs():
    line = "H1 neta netb vname 1"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Ccvs(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "H1")
    assert(mod.type == "ccvs")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "1")
    assert(str(mod) == line)
    assert(mod.elements == ["H1", "neta", "netb", "vname", "1"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
    assert(mod.vname == "vname")

    mod.vname = "vname_test"
    assert(mod.vname == "vname_test")

    mod.value = "1000"
    assert(mod.value == "1000")


def test_module_isource():
    line = "I1 neta netb 1e-3"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Isource(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "I1")
    assert(mod.type == "isource")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "1e-3")
    assert(str(mod) == line)
    assert(mod.elements == ["I1", "neta", "netb", "1e-3"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
    assert(mod.current == "1e-3")

    mod.current = "1e-9"
    assert(mod.current == "1e-9")


def test_module_jfet():
    line = "J1 neta netb netc jmodel"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Jfet(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "J1")
    assert(mod.type == "jfet")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "jmodel")
    assert(str(mod) == line)
    assert(mod.elements == ["J1", "neta", "netb", "netc", "jmodel"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc")])
    assert(mod.model == "jmodel")

    mod.model = "testmod"
    assert(mod.model == "testmod")


def test_module_inductor():
    line = "L1 neta netb 1e-6"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Inductor(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "L1")
    assert(mod.type == "inductor")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "1e-6")
    assert(str(mod) == line)
    assert(mod.elements == ["L1", "neta", "netb", "1e-6"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
    assert(mod.inductance == "1e-6")

    mod.inductance = "1e-9"
    assert(mod.inductance == "1e-9")

def test_module_mosfet():
    line = "M1 neta netb netc netd mosmodel"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Mosfet(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "M1")
    assert(mod.type == "mosfet")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "mosmodel")
    assert(str(mod) == line)
    assert(mod.elements == ["M1", "neta", "netb", "netc", "netd", "mosmodel"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc"), ("n3", "netd")])
    assert(mod.model == "mosmodel")

    mod.model = "test"
    assert(mod.model == "test")


def test_module_numerical_device_gss():
    pass


def test_module_lossy_transmission_line():
    pass

def test_module_bjt_3t():
    line = "Q1 neta netb netc bjtmodel"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Bjt(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "Q1")
    assert(mod.type == "bjt")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "bjtmodel")
    assert(str(mod) == line)
    assert(mod.elements == ["Q1", "neta", "netb", "netc", "bjtmodel"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc") ])
    assert(mod.model == "bjtmodel")

    mod.model = "test"
    assert(mod.model == "test")


def test_module_bjt_4t():
    line = "Q1 neta netb netc netd bjtmodel"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Bjt(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "Q1")
    assert(mod.type == "bjt")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "bjtmodel")
    assert(str(mod) == line)
    assert(mod.elements == ["Q1", "neta", "netb", "netc", "netd", "bjtmodel"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc"), ("n3", "netd") ])
    assert(mod.model == "bjtmodel")

    mod.model = "test"
    assert(mod.model == "test")


def test_module_resistor():
    line = "R1 neta netb 1e3"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Resistor(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "R1")
    assert(mod.type == "resistor")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "1e3")
    assert(str(mod) == line)
    assert(mod.elements == ["R1", "neta", "netb", "1e3"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
    assert(mod.resistance == "1e3")

    mod.resistance = "1e3"
    assert(mod.resistance == "1e3")


def test_module_vcsw():
    pass

def test_module_lossless_transmission_line():
    pass

def test_module_uniformely_distributed_rc_line():
    pass


def test_module_vsource():
    line = "V1 neta netb 1"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Vsource(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "V1")
    assert(mod.type == "vsource")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "1")
    assert(str(mod) == line)
    assert(mod.elements == ["V1", "neta", "netb", "1"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
    assert(mod.voltage == "1")

    mod.voltage = "10"
    assert(mod.voltage == "10")


def test_module_icsw():
    pass

def test_module_subckt():
    pass

def test_module_single_lossy_transmission_line():
    pass


def test_module_mesfet():
    line = "Z1 neta netb netc mesmodel"
    loc  = "root"
    n    = 1
    uid  = "testuid"
    mod  = sp.Mesfet(line, loc, n, uid)

    assert(mod.line == line)
    assert(mod.location == loc)
    assert(mod.uid == uid)
    assert(mod.n == n)
    assert(mod.instance == "Z1")
    assert(mod.type == "mesfet")
    assert(isinstance(mod.ports, dict))
    assert(mod.value == "mesmodel")
    assert(str(mod) == line)
    assert(mod.elements == ["Z1", "neta", "netb", "netc", "mesmodel"])
    assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc")])
    assert(mod.model == "mesmodel")

    mod.model = "test"
    assert(mod.model == "test")



def test_circuit_init_list():
    netlist = ["C1 neta netb 1e-12",
               "R1 neta netb 1e3",
               "R2 neta netc 10e3"]

    cir  = sp.Circuit(netlist, is_filename=False)


    netlist = [x.lower() for x in netlist]
    netlist = [ "* Netlist\n" ] + netlist + [""]
    net_in = "\n".join(netlist)

    net_out = str(cir) 
    assert(net_in == net_out)


def test_circuit_init_str():
    netlist = ["C1 neta netb 1e-12",
               "R1 neta netb 1e3",
               "R2 neta netc 10e3"]

    netlist = "\n".join(netlist)

    cir  = sp.Circuit(netlist, is_filename=False)


    net_in = "* Netlist\n\n" + netlist.lower() + "\n"

    net_out = str(cir) 

    print(net_in)
    print(net_out)
    assert(net_in == net_out)
