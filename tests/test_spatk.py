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

import pytest
import spatk as sp

cases = { 

"default": 
{
    "line"      : "A Default Line",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Default,
    "instance"  : None,
    "type"      : "default",
    "value"     : None,
    "ports"     : dict(),
},
"component": 
{
    "line"      : "R1 neta netb 1e3",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Component,
    "instance"  : "R1",
    "type"      : "component",
    "value"     : None,
    "ports"     : dict(),
},
"component_2t": 
{
    "line"      : "R1 neta netb 1e3",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Component_2T,
    "instance"  : "R1",
    "type"      : "component_2t",
    "value"     : "1e3",
    "ports"     : {"n0": "neta", "n1": "netb"},
},
"component_3t": 
{
    "line"      : "X1 neta netb netc model_3t",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Component_3T,
    "instance"  : "X1",
    "type"      : "component_3t",
    "value"     : "model_3t",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
},
"component_4t":
{
    "line"      : "X1 neta netb netc netd model_4t",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Component_4T,
    "instance"  : "X1",
    "type"      : "component_4t",
    "value"     : "model_4t",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc", "n3": "netd"},
},
"statement":
{
    "line"      : ".include mylib.spice",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Statement,
    "instance"  : None,
    "type"      : "statement",
    "value"     : None,
    "ports"     : dict()
},
"commment":
{
    "line"      : "* A test comment",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Comment,
    "instance"  : None,
    "type"      : "comment",
    "value"     : None,
    "ports"     : dict()
},
"model":
{
    "line"      : ".model mymodel model",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Model,
    "instance"  : None,
    "type"      : "model",
    "value"     : None,
    "ports"     : dict()
},
"model":
{
    "line"      : ".include mylib.spice",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Include,
    "instance"  : None,
    "type"      : "include",
    "value"     : None,
    "ports"     : dict()
},
"library":
{
    "line"      : ".lib lib.spice module",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Library,
    "instance"  : None,
    "type"      : "library",
    "value"     : None,
    "ports"     : dict(),
    "filename"  : "lib.spice",
    "libname"    : "module",
},
"option":
{
    "line"      : ".option setting=value",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Option,
    "instance"  : None,
    "type"      : "option",
    "value"     : None,
    "ports"     : dict(),
},
"function":
{
    "line"      : ".func myfunc='expression'",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Function,
    "instance"  : None,
    "type"      : "function",
    "value"     : None,
    "ports"     : dict(),
},
"param":
{
    "line"      : ".param mypar='value'",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Param,
    "instance"  : None,
    "type"      : "param",
    "value"     : "'value'",
    "ports"     : dict(),
    "name"      : "mypar",
},
"global":
{
    "line"      : ".global vss vdd",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Global,
    "instance"  : None,
    "type"      : "global",
    "value"     : None,
    "ports"     : dict(),
},
"capacitor":
{
    "line"        : "C1 neta netb 10e-12",
    "loc"         : "root",
    "n"           : 1,
    "uid"         : "testuid",
    "mod"         : sp.Capacitor,
    "instance"    : "C1",
    "type"        : "capacitor",
    "value"       : "10e-12",
    "ports"       : {"n0": "neta", "n1": "netb"},
    "capacitance" : "10e-12",
},
"diode":
{
    "line"      : "D1 neta netb dmod",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Diode,
    "instance"  : "D1",
    "type"      : "diode",
    "value"     : "dmod",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "model"     : "dmod",
},
"cccs":
{
    "line"      : "F1 neta netb vname 1",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Cccs,
    "instance"  : "F1",
    "type"      : "cccs",
    "value"     : "1",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "vname"     : "vname",
},
"ccvs":
{
    "line"      : "H1 neta netb vname 1",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Ccvs,
    "instance"  : "H1",
    "type"      : "ccvs",
    "value"     : "1",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "vname"     : "vname",
},
"isource":
{
    "line"      : "I1 neta netb 1e-3",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Isource,
    "instance"  : "I1",
    "type"      : "isource",
    "value"     : "1e-3",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "current"   : "1e-3",
},
"jfet":
{
    "line"      : "J1 neta netb netc jmodel",
    "loc"       : "root",
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : sp.Jfet,
    "instance"  : "J1",
    "type"      : "jfet",
    "value"     : "jmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
    "model"     : "jmodel"
},






}



def create_module(case):
    module = case["mod"]
    line = case["line"]
    loc = case["loc"]
    n = case["n"]
    uid = case["uid"]
    return module(line, loc, n, uid)



def test_modules_common():

    for k in cases.keys():

        case = cases[k]

        mod = create_module(case)

        assert(isinstance(mod.line,     str))
        assert(isinstance(mod.location, str))
        assert(isinstance(mod.uid,      str))
        assert(isinstance(mod.ports,    dict))
        assert(isinstance(mod.n,        int))

        assert(str(mod)     == case["line"])
        assert(mod.line     == case["line"])
        assert(mod.location == case["loc"])
        assert(mod.uid      == case["uid"])
        assert(mod.n        == case["n"])
        assert(mod.instance == case["instance"])
        assert(mod.type     == case["type"])
        assert(mod.value    == case["value"])
        assert(mod.ports    == case["ports"])



def test_module_library():
    case = cases["library"]
    mod = create_module(case)
    assert(mod.libname  == case["libname"])
    assert(mod.filename == case["filename"])
    mod.libname = "myname"
    assert(mod.libname == "myname")
    mod.filename = "myfile"
    assert(mod.filename == "myfile")


def test_module_param():
    case = cases["param"]
    mod = create_module(case)
    assert(mod.name  == case["name"])
    mod.name = "myname"
    assert(mod.name == "myname")
    mod.value = "myvalue"
    assert(mod.value == "myvalue")


def test_module_capacitance():
    case = cases["capacitor"]
    mod = create_module(case)
    assert(mod.capacitance  == case["capacitance"])
    mod.capacitance = "myval"
    assert(mod.capacitance == "myval")


def test_module_diode():
    case = cases["diode"]
    mod = create_module(case)

    assert(mod.model == case["model"])
    mod.model = "mymod"
    assert(mod.model == "mymod")


def test_module_cccs():
    case = cases["cccs"]
    mod = create_module(case)

    assert(mod.vname == case["vname"])
    mod.vname = "myname"
    assert(mod.vname == "myname")
    mod.value = "myval"
    assert(mod.value == "myval")


def test_module_ccvs():
    case = cases["ccvs"]
    mod = create_module(case)

    assert(mod.vname == case["vname"])
    mod.vname = "myname"
    assert(mod.vname == "myname")
    mod.value = "myval"
    assert(mod.value == "myval")


def test_module_isource():
    case = cases["isource"]
    mod = create_module(case)

    assert(mod.current == case["current"])
    mod.current = "mycur"
    assert(mod.current == "mycur")


def test_module_jfet():
    case = cases["jfet"]
    mod = create_module(case)

    assert(mod.model == case["model"])

    mod.model = "testmod"
    assert(mod.model == "testmod")


# def test_module_xspice():
#     pass


# def test_module_behavioral_source():
#     pass


# def test_module_vcvs():
#     pass


# def test_module_vccs():
#     pass






# def test_module_inductor():
#     line = "L1 neta netb 1e-6"
#     loc  = "root"
#     n    = 1
#     uid  = "testuid"
#     mod  = sp.Inductor(line, loc, n, uid)

#     assert(mod.line == line)
#     assert(mod.location == loc)
#     assert(mod.uid == uid)
#     assert(mod.n == n)
#     assert(mod.instance == "L1")
#     assert(mod.type == "inductor")
#     assert(isinstance(mod.ports, dict))
#     assert(mod.value == "1e-6")
#     assert(str(mod) == line)
#     assert(mod.elements == ["L1", "neta", "netb", "1e-6"])
#     assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
#     assert(mod.inductance == "1e-6")

#     mod.inductance = "1e-9"
#     assert(mod.inductance == "1e-9")

# def test_module_mosfet():
#     line = "M1 neta netb netc netd mosmodel"
#     loc  = "root"
#     n    = 1
#     uid  = "testuid"
#     mod  = sp.Mosfet(line, loc, n, uid)

#     assert(mod.line == line)
#     assert(mod.location == loc)
#     assert(mod.uid == uid)
#     assert(mod.n == n)
#     assert(mod.instance == "M1")
#     assert(mod.type == "mosfet")
#     assert(isinstance(mod.ports, dict))
#     assert(mod.value == "mosmodel")
#     assert(str(mod) == line)
#     assert(mod.elements == ["M1", "neta", "netb", "netc", "netd", "mosmodel"])
#     assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc"), ("n3", "netd")])
#     assert(mod.model == "mosmodel")

#     mod.model = "test"
#     assert(mod.model == "test")


# def test_module_numerical_device_gss():
#     pass


# def test_module_lossy_transmission_line():
#     pass

# def test_module_bjt_3t():
#     line = "Q1 neta netb netc bjtmodel"
#     loc  = "root"
#     n    = 1
#     uid  = "testuid"
#     mod  = sp.Bjt(line, loc, n, uid)

#     assert(mod.line == line)
#     assert(mod.location == loc)
#     assert(mod.uid == uid)
#     assert(mod.n == n)
#     assert(mod.instance == "Q1")
#     assert(mod.type == "bjt")
#     assert(isinstance(mod.ports, dict))
#     assert(mod.value == "bjtmodel")
#     assert(str(mod) == line)
#     assert(mod.elements == ["Q1", "neta", "netb", "netc", "bjtmodel"])
#     assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc") ])
#     assert(mod.model == "bjtmodel")

#     mod.model = "test"
#     assert(mod.model == "test")


# def test_module_bjt_4t():
#     line = "Q1 neta netb netc netd bjtmodel"
#     loc  = "root"
#     n    = 1
#     uid  = "testuid"
#     mod  = sp.Bjt(line, loc, n, uid)

#     assert(mod.line == line)
#     assert(mod.location == loc)
#     assert(mod.uid == uid)
#     assert(mod.n == n)
#     assert(mod.instance == "Q1")
#     assert(mod.type == "bjt")
#     assert(isinstance(mod.ports, dict))
#     assert(mod.value == "bjtmodel")
#     assert(str(mod) == line)
#     assert(mod.elements == ["Q1", "neta", "netb", "netc", "netd", "bjtmodel"])
#     assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc"), ("n3", "netd") ])
#     assert(mod.model == "bjtmodel")

#     mod.model = "test"
#     assert(mod.model == "test")


# def test_module_resistor():
#     line = "R1 neta netb 1e3"
#     loc  = "root"
#     n    = 1
#     uid  = "testuid"
#     mod  = sp.Resistor(line, loc, n, uid)

#     assert(mod.line == line)
#     assert(mod.location == loc)
#     assert(mod.uid == uid)
#     assert(mod.n == n)
#     assert(mod.instance == "R1")
#     assert(mod.type == "resistor")
#     assert(isinstance(mod.ports, dict))
#     assert(mod.value == "1e3")
#     assert(str(mod) == line)
#     assert(mod.elements == ["R1", "neta", "netb", "1e3"])
#     assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
#     assert(mod.resistance == "1e3")

#     mod.resistance = "1e3"
#     assert(mod.resistance == "1e3")


# def test_module_vcsw():
#     pass

# def test_module_lossless_transmission_line():
#     pass

# def test_module_uniformely_distributed_rc_line():
#     pass


# def test_module_vsource():
#     line = "V1 neta netb 1"
#     loc  = "root"
#     n    = 1
#     uid  = "testuid"
#     mod  = sp.Vsource(line, loc, n, uid)

#     assert(mod.line == line)
#     assert(mod.location == loc)
#     assert(mod.uid == uid)
#     assert(mod.n == n)
#     assert(mod.instance == "V1")
#     assert(mod.type == "vsource")
#     assert(isinstance(mod.ports, dict))
#     assert(mod.value == "1")
#     assert(str(mod) == line)
#     assert(mod.elements == ["V1", "neta", "netb", "1"])
#     assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb")])
#     assert(mod.voltage == "1")

#     mod.voltage = "10"
#     assert(mod.voltage == "10")


# def test_module_icsw():
#     pass

# def test_module_subckt():
#     pass

# def test_module_single_lossy_transmission_line():
#     pass


# def test_module_mesfet():
#     line = "Z1 neta netb netc mesmodel"
#     loc  = "root"
#     n    = 1
#     uid  = "testuid"
#     mod  = sp.Mesfet(line, loc, n, uid)

#     assert(mod.line == line)
#     assert(mod.location == loc)
#     assert(mod.uid == uid)
#     assert(mod.n == n)
#     assert(mod.instance == "Z1")
#     assert(mod.type == "mesfet")
#     assert(isinstance(mod.ports, dict))
#     assert(mod.value == "mesmodel")
#     assert(str(mod) == line)
#     assert(mod.elements == ["Z1", "neta", "netb", "netc", "mesmodel"])
#     assert(list(mod.ports.items()) == [("n0", "neta"), ("n1", "netb"), ("n2", "netc")])
#     assert(mod.model == "mesmodel")

#     mod.model = "test"
#     assert(mod.model == "test")



# def test_circuit_init_list():
#     netlist = ["C1 neta netb 1e-12",
#                "R1 neta netb 1e3",
#                "R2 neta netc 10e3"]

#     cir  = sp.Circuit(netlist, is_filename=False)


#     netlist = [x.lower() for x in netlist]
#     netlist = [ "* Netlist\n" ] + netlist + [""]
#     net_in = "\n".join(netlist)

#     net_out = str(cir) 
#     assert(net_in == net_out)


# def test_circuit_init_str():
#     netlist = ["C1 neta netb 1e-12",
#                "R1 neta netb 1e3",
#                "R2 neta netc 10e3"]

#     netlist = "\n".join(netlist)

#     cir  = sp.Circuit(netlist, is_filename=False)


#     net_in = "* Netlist\n\n" + netlist.lower() + "\n"

#     net_out = str(cir) 

#     print(net_in)
#     print(net_out)
#     assert(net_in == net_out)
