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

import spatk.elements as spe

CASES = {
"default":
{
    "line"      : "A Default Line",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Default,
    "instance"  : None,
    "type"      : "default",
    "value"     : None,
    "ports"     : dict(),
},
"component":
{
    "line"      : "R1 neta netb 1e3",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Component,
    "instance"  : "R1",
    "type"      : "component",
    "value"     : None,
    "ports"     : dict(),
},
"component_2t":
{
    "line"      : "R1 neta netb 1e3",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Component_2T,
    "instance"  : "R1",
    "type"      : "component_2t",
    "value"     : "1e3",
    "ports"     : {"n0": "neta", "n1": "netb"},
},
"component_3t":
{
    "line"      : "X1 neta netb netc model_3t",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Component_3T,
    "instance"  : "X1",
    "type"      : "component_3t",
    "value"     : "model_3t",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
},
"component_4t":
{
    "line"      : "X1 neta netb netc netd model_4t",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Component_4T,
    "instance"  : "X1",
    "type"      : "component_4t",
    "value"     : "model_4t",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc", "n3": "netd"},
},
"statement":
{
    "line"      : ".include mylib.spice",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Statement,
    "instance"  : None,
    "type"      : "statement",
    "value"     : None,
    "ports"     : dict()
},
"commment":
{
    "line"      : "* A test comment",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Comment,
    "instance"  : None,
    "type"      : "comment",
    "value"     : None,
    "ports"     : dict()
},
"model":
{
    "line"      : ".model mymodel model",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Model,
    "instance"  : None,
    "type"      : "model",
    "value"     : None,
    "ports"     : dict()
},
"include":
{
    "line"      : ".include mylib.spice",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Include,
    "instance"  : None,
    "type"      : "include",
    "value"     : None,
    "ports"     : dict()
},
"library":
{
    "line"      : ".lib lib.spice module",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Library,
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
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Option,
    "instance"  : None,
    "type"      : "option",
    "value"     : None,
    "ports"     : dict(),
},
"function":
{
    "line"      : ".func myfunc='expression'",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Function,
    "instance"  : None,
    "type"      : "function",
    "value"     : None,
    "ports"     : dict(),
},
"temp":
{
    "line"      : ".temp 20",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Temp,
    "instance"  : None,
    "type"      : "temp",
    "value"     : "20",
    "ports"     : dict(),
},
"param":
{
    "line"      : ".param mypar='value'",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Param,
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
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Global,
    "instance"  : None,
    "type"      : "global",
    "value"     : None,
    "ports"     : dict(),
},
"subckt":
{
    "line"        : "X1 neta netb netc mysubckt",
    "loc"         : "root",
    "lib"         : None,
    "n"           : 1,
    "uid"         : "testuid",
    "mod"         : spe.Subckt,
    "instance"    : "X1",
    "type"        : "subckt",
    "value"       : "mysubckt",
    "ports"       : dict(),
},
"subcktdef":
{
    "line"        : ".subckt mysubckt neta netb ",
    "loc"         : "root",
    "lib"         : None,
    "n"           : 1,
    "uid"         : "testuid",
    "mod"         : spe.SubcktDef,
    "instance"    : None,
    "type"        : "subcktdef",
    "value"       : "mysubckt",
    "ports"       : dict(),
},
"capacitor":
{
    "line"        : "C1 neta netb 10e-12",
    "loc"         : "root",
    "lib"         : None,
    "n"           : 1,
    "uid"         : "testuid",
    "mod"         : spe.Capacitor,
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
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Diode,
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
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Cccs,
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
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Ccvs,
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
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Isource,
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
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Jfet,
    "instance"  : "J1",
    "type"      : "jfet",
    "value"     : "jmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
    "model"     : "jmodel"
},
"inductor":
{
    "line"       : "L1 neta netb 1e-6",
    "loc"        : "root",
    "lib"       : None,
    "n"          : 1,
    "uid"        : "testuid",
    "mod"        : spe.Inductor,
    "instance"   : "L1",
    "type"       : "inductor",
    "value"      : "1e-6",
    "ports"      : {"n0": "neta", "n1": "netb"},
    "inductance" : "1e-6"
},
"mosfet":
{
    "line"      : "M1 neta netb netc netd mosmodel",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Mosfet,
    "instance"  : "M1",
    "type"      : "mosfet",
    "value"     : "mosmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc", "n3": "netd"},
    "model"     : "mosmodel"
},
"bjt_3t":
{
    "line"      : "Q1 neta netb netc bjtmodel",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Bjt,
    "instance"  : "Q1",
    "type"      : "bjt",
    "value"     : "bjtmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
    "model"     : "bjtmodel"
},
"bjt_4t":
{
    "line"      : "Q1 neta netb netc netd bjtmodel",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Bjt,
    "instance"  : "Q1",
    "type"      : "bjt",
    "value"     : "bjtmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc", "n3": "netd"},
    "model"     : "bjtmodel"
},
"resistor":
{
    "line"       : "R1 neta netb 1e3",
    "loc"        : "root",
    "lib"       : None,
    "n"          : 1,
    "uid"        : "testuid",
    "mod"        : spe.Resistor,
    "instance"   : "R1",
    "type"       : "resistor",
    "value"      : "1e3",
    "ports"      : {"n0": "neta", "n1": "netb"},
    "resistance" : "1e3"
},
"vsource":
{
    "line"      : "V1 neta netb 1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Vsource,
    "instance"  : "V1",
    "type"      : "vsource",
    "value"     : "1",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "voltage"   : "1"
},
"mesfet":
{
    "line"      : "Z1 neta netb netc mesmodel",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Mesfet,
    "instance"  : "Z1",
    "type"      : "mesfet",
    "value"     : "mesmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
    "model"     : "mesmodel"
},
"component__args":
{
    "line"      : "R1 neta netb 1e3 myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Component,
    "instance"  : "R1",
    "type"      : "component",
    "value"     : None,
    "ports"     : dict(),
},
"component_2t__args":
{
    "line"      : "R1 neta netb 1e3 myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Component_2T,
    "instance"  : "R1",
    "type"      : "component_2t",
    "value"     : "1e3",
    "ports"     : {"n0": "neta", "n1": "netb"},
},
"component_3t__args":
{
    "line"      : "X1 neta netb netc model_3t myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Component_3T,
    "instance"  : "X1",
    "type"      : "component_3t",
    "value"     : "model_3t",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
},
"component_4t__args":
{
    "line"      : "X1 neta netb netc netd model_4t myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Component_4T,
    "instance"  : "X1",
    "type"      : "component_4t",
    "value"     : "model_4t",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc", "n3": "netd"},
},
"capacitor__args":
{
    "line"        : "C1 neta netb 10e-12 myarg=1",
    "loc"         : "root",
    "lib"         : None,
    "n"           : 1,
    "uid"         : "testuid",
    "mod"         : spe.Capacitor,
    "instance"    : "C1",
    "type"        : "capacitor",
    "value"       : "10e-12",
    "ports"       : {"n0": "neta", "n1": "netb"},
    "capacitance" : "10e-12",
},
"diode__args":
{
    "line"      : "D1 neta netb dmod myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Diode,
    "instance"  : "D1",
    "type"      : "diode",
    "value"     : "dmod",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "model"     : "dmod",
},
"cccs__args":
{
    "line"      : "F1 neta netb vname 1 myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Cccs,
    "instance"  : "F1",
    "type"      : "cccs",
    "value"     : "1",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "vname"     : "vname",
},
"ccvs__args":
{
    "line"      : "H1 neta netb vname 1 myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Ccvs,
    "instance"  : "H1",
    "type"      : "ccvs",
    "value"     : "1",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "vname"     : "vname",
},
"isource__args":
{
    "line"      : "I1 neta netb 1e-3 myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Isource,
    "instance"  : "I1",
    "type"      : "isource",
    "value"     : "1e-3",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "current"   : "1e-3",
},
"jfet__args":
{
    "line"      : "J1 neta netb netc jmodel myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Jfet,
    "instance"  : "J1",
    "type"      : "jfet",
    "value"     : "jmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
    "model"     : "jmodel"
},
"inductor__args":
{
    "line"       : "L1 neta netb 1e-6 myarg=1",
    "loc"        : "root",
    "lib"        : None,
    "n"          : 1,
    "uid"        : "testuid",
    "mod"        : spe.Inductor,
    "instance"   : "L1",
    "type"       : "inductor",
    "value"      : "1e-6",
    "ports"      : {"n0": "neta", "n1": "netb"},
    "inductance" : "1e-6"
},
"mosfet__args":
{
    "line"      : "M1 neta netb netc netd mosmodel myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Mosfet,
    "instance"  : "M1",
    "type"      : "mosfet",
    "value"     : "mosmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc", "n3": "netd"},
    "model"     : "mosmodel"
},
"bjt_3t__args":
{
    "line"      : "Q1 neta netb netc bjtmodel myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Bjt,
    "instance"  : "Q1",
    "type"      : "bjt",
    "value"     : "bjtmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
    "model"     : "bjtmodel"
},
"bjt_4t__args":
{
    "line"      : "Q1 neta netb netc netd bjtmodel myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Bjt,
    "instance"  : "Q1",
    "type"      : "bjt",
    "value"     : "bjtmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc", "n3": "netd"},
    "model"     : "bjtmodel"
},
"resistor__args":
{
    "line"       : "R1 neta netb 1e3 myarg=1",
    "loc"        : "root",
    "lib"        : None,
    "n"          : 1,
    "uid"        : "testuid",
    "mod"        : spe.Resistor,
    "instance"   : "R1",
    "type"       : "resistor",
    "value"      : "1e3",
    "ports"      : {"n0": "neta", "n1": "netb"},
    "resistance" : "1e3"
},
"vsource__args":
{
    "line"      : "V1 neta netb 1 myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Vsource,
    "instance"  : "V1",
    "type"      : "vsource",
    "value"     : "1",
    "ports"     : {"n0": "neta", "n1": "netb"},
    "voltage"   : "1"
},
"mesfet__args":
{
    "line"      : "Z1 neta netb netc mesmodel myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Mesfet,
    "instance"  : "Z1",
    "type"      : "mesfet",
    "value"     : "mesmodel",
    "ports"     : {"n0": "neta", "n1": "netb", "n2": "netc"},
    "model"     : "mesmodel"
},
}


def create_module(case):
    """ Helper function for create modules. """
    module = case["mod"]
    line = case["line"]
    loc = case["loc"]
    lib = case["lib"]
    n = case["n"]
    uid = case["uid"]
    return module(line, loc, lib, n, uid)


def test_modules_common():
    """ Test common module properties.

    Module classes have common properties which
    are tested all in the same run.

    These are all adressed in CASES dictionary
    defined above.
    """
    for k in CASES.keys():

        case = CASES[k]

        mod = create_module(case)

        assert(isinstance(mod.line,     str))
        assert(isinstance(mod.location, str))
        assert(isinstance(mod.uid,      str))
        assert(isinstance(mod.ports,    dict))
        assert(isinstance(mod.n,        int))

        assert(str(mod)     == case["line"])
        assert(mod.line     == case["line"])
        assert(mod.location == case["loc"])
        assert(mod.lib      == case["lib"])
        assert(mod.uid      == case["uid"])
        assert(mod.n        == case["n"])
        assert(mod.instance == case["instance"])
        assert(mod.type     == case["type"])
        assert(mod.value    == case["value"])
        assert(mod.ports    == case["ports"])



def test_module_library():
    """ Test library module specific properties """
    case = CASES["library"]
    mod = create_module(case)
    assert(mod.libname  == case["libname"])
    assert(mod.filename == case["filename"])
    mod.libname = "myname"
    assert(mod.libname == "myname")
    mod.filename = "myfile"
    assert(mod.filename == "myfile")


def test_module_param():
    """ Test param module specific properties """
    case = CASES["param"]
    mod = create_module(case)
    assert(mod.name  == case["name"])
    mod.name = "myname"
    assert(mod.name == "myname")
    mod.value = "myvalue"
    assert(mod.value == "myvalue")


def test_module_capacitor():
    """ Test capacitor module specific properties """
    case = CASES["capacitor"]
    mod = create_module(case)
    assert(mod.capacitance  == case["capacitance"])
    mod.capacitance = "myval"
    assert(mod.capacitance == "myval")


def test_module_diode():
    """ Test diode module specific properties """
    case = CASES["diode"]
    mod = create_module(case)

    assert(mod.model == case["model"])
    mod.model = "mymod"
    assert(mod.model == "mymod")


def test_module_cccs():
    """ Test cccs module specific properties """
    case = CASES["cccs"]
    mod = create_module(case)

    assert(mod.vname == case["vname"])
    mod.vname = "myname"
    assert(mod.vname == "myname")
    mod.value = "myval"
    assert(mod.value == "myval")


def test_module_ccvs():
    """ Test ccvs module specific properties """
    case = CASES["ccvs"]
    mod = create_module(case)

    assert(mod.vname == case["vname"])
    mod.vname = "myname"
    assert(mod.vname == "myname")
    mod.value = "myval"
    assert(mod.value == "myval")


def test_module_isource():
    """ Test isource module specific properties """
    case = CASES["isource"]
    mod = create_module(case)

    assert(mod.current == case["current"])
    mod.current = "mycur"
    assert(mod.current == "mycur")


def test_module_jfet():
    """ Test jfet module specific properties """
    case = CASES["jfet"]
    mod = create_module(case)

    assert(mod.model == case["model"])
    mod.model = "testmod"
    assert(mod.model == "testmod")


def test_module_inductor():
    """ Test inductor module specific properties """
    case = CASES["inductor"]
    mod = create_module(case)

    assert(mod.inductance == case["inductance"])
    mod.inductance = "myval"
    assert(mod.inductance == "myval")


def test_module_mosfet():
    """ Test mosfet module specific properties """
    case = CASES["mosfet"]
    mod = create_module(case)

    assert(mod.model == "mosmodel")
    mod.model = "testmod"
    assert(mod.model == "testmod")


def test_module_bjt_3t():
    """ Test bjt_3t module specific properties """
    case = CASES["bjt_3t"]
    mod = create_module(case)

    assert(mod.model == case["model"])
    mod.model = "testmod"
    assert(mod.model == "testmod")


def test_module_bjt_4t():
    """ Test bjt_4t module specific properties """
    case = CASES["bjt_4t"]
    mod = create_module(case)

    assert(mod.model == case["model"])
    mod.model = "testmod"
    assert(mod.model == "testmod")


def test_module_resistor():
    """ Test resistor module specific properties """
    case = CASES["resistor"]
    mod = create_module(case)

    assert(mod.resistance == case["resistance"])
    mod.resistance = "myval"
    assert(mod.resistance == "myval")


def test_module_vsource():
    """ Test vsourse module specific properties """
    case = CASES["vsource"]
    mod = create_module(case)

    assert(mod.voltage == case["voltage"])
    mod.voltage = "myvar"
    assert(mod.voltage == "myvar")


def test_module_mesfet():
    """ Test mesfet module specific properties """
    case = CASES["mesfet"]
    mod = create_module(case)

    assert(mod.model == "mesmodel")
    mod.model = "testmod"
    assert(mod.model == "testmod")


def test_module_xspice():
    pass


def test_module_behavioral_source():
    pass


def test_module_vcvs():
    pass


def test_module_vccs():
    pass


def test_module_numerical_device_gss():
    pass


def test_module_lossy_transmission_line():
    pass


def test_module_vcsw():
    pass


def test_module_lossless_transmission_line():
    pass


def test_module_uniformely_distributed_rc_line():
    pass


def test_module_icsw():
    pass


def test_module_subckt():
    """ Test subckt module specific properties """
    case = CASES["subckt"]
    mod = create_module(case)

    assert(mod.name == "mysubckt")
    mod.name = "testsubckt"
    assert(mod.name == "testsubckt")


def test_module_subcktdef():
    """ Test subcktdef module specific properties """
    case = CASES["subcktdef"]
    mod = create_module(case)

    assert(mod.name == "mysubckt")
    mod.name = "testsubckt"
    assert(mod.name == "testsubckt")


def test_module_single_lossy_transmission_line():
    pass



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
    net_in = "* Netlist\n\n" + netlist.lower() + "\n"

    cir  = sp.Circuit(netlist, is_filename=False)
    net_out = str(cir)

    assert(net_in == net_out)


def input_netlist(filename):
    """ helper function to create equivalent input netlist """
    with open(filename, "r") as ifile:
        net_in = "* {}\n\n".format(filename) + (ifile.read()).lower()
    return net_in


def test_circuit_init_simple():
    netlist = "netlists/simple.sp"
    net_in = input_netlist(netlist)
    cir  = sp.Circuit(netlist)
    net_out = str(cir)
    assert(net_in == net_out)


def test_circuit_init_simple():
    netlist = "netlists/simple.sp"
    net_in = input_netlist(netlist)
    cir  = sp.Circuit(netlist)
    net_out = str(cir)
    assert(net_in == net_out)


def test_circuit_init_complex():
    netlist = "netlists/complex.sp"
    net_in = input_netlist(netlist)
    cir  = sp.Circuit(netlist)
    net_out = str(cir)
    assert(net_in == net_out)


def test_circuit_hierachy():
    netlist = "netlists/complex.sp"
    cir = sp.Circuit(netlist)
    uid = cir.filter("instance", "r1")[0]
    assert(cir[uid].location == "root/module")
    uid = cir.filter("instance", "rs1")[0]
    assert(cir[uid].location == "root/module/submodule")


def test_circuit_library():
    netlist = "netlists/lib.sp"
    cir = sp.Circuit(netlist)
    uid = cir.filter("instance", "r1")[0]
    assert(cir[uid].lib == "mylib")


def test_circuit_get_args():
    netlist = "netlists/args.sp"
    cir = sp.Circuit(netlist)
    for uid in cir:
        assert(cir[uid].args.l == "1u")
        assert(cir[uid].args.w == "1u")
        assert(cir[uid].args.nf == "1")


def test_circuit_set_args_prop():
    netlist = "netlists/args.sp"
    net_in = input_netlist(netlist)
    cir = sp.Circuit(netlist)
    for uid in cir:
        cir[uid].args.w = "2u"
    net_in = net_in.replace("w=1u", "w=2u")
    assert( str(cir) == net_in )


def test_circuit_set_args_dict():
    netlist = "netlists/args.sp"
    net_in = input_netlist(netlist)
    cir = sp.Circuit(netlist)
    for uid in cir:
        cir[uid].args["w"] = "2u"
    net_in = net_in.replace("w=1u", "w=2u")
    assert( str(cir) == net_in )

