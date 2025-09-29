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

import os
os.environ["SPICE_SYNTAX"] = "generic"

import pytest
import spatk as sp
import spatk.elements as spe

from helpers import create_module, input_netlist

element_default = {
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
    }

element_component = {
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
    }

element_component_2t = {
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
    }

element_component_3t = {
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
    }

element_component_4t = {
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
    }

element_statement = {
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
    }

element_comment = {
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
    }

element_model = {
    "line"          : ".model mymodel spice_model",
    "loc"           : "root",
    "lib"           : None,
    "n"             : 1,
    "uid"           : "testuid",
    "mod"           : spe.Model,
    "instance"      : None,
    "type"          : "model",
    "model_type"    : "spice_model",
    "value"         : None,
    "ports"         : dict()
    }

element_include = {
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
    }

element_library = {
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
    }

element_option = {
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
    }

element_param = {
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
    }

element_global = {
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
    }

element_subckt = {
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
    }

element_subcktdef = {
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
    }

element_capacitor = {
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
    }

element_diode = {
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
    }

element_cccs = {
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
    }

element_ccvs = {
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
    }

element_isource = {
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
    }

element_jfet = {
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
    }

element_inductor = {
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
    }

element_mosfet = {
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
    }

element_bjt_3t = {
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
    }

element_bjt_4t = {
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
    }

element_resistor = {
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
    }

element_vsource = {
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
    }

element_mesfet = {
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
    }

element_component__args = {
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
    }

element_component_2t__args = {
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
    }

element_component_3t__args = {
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
    }

element_component_4t__args = {
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
    }

element_capacitor__args = {
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
    }

element_diode__args = {
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
    }

element_cccs__args = {
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
    }

element_ccvs__args = {
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
    }

element_isource__args = {
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
    }

element_jfet__args = {
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
    }

element_inductor__args = {
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
    }

element_mosfet__args = {
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
    }

element_bjt_3t__args = {
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
    }

element_bjt_4t__args = {
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
    }

element_resistor__args = {
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
    }

element_vsource__args = {
    "line"      : "V1 neta netb 1 myarg=1",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Vsource,
    "instance"  : "V1",
    "type"      : "vsource",
    "value"     : ["1", "myarg=1"],
    "ports"     : {"n0": "neta", "n1": "netb"},
    "voltage"   : ["1", "myarg=1"]
    }

element_vsource__pulse = {
    "line"      : "V1 neta netb DC 0 PULSE(0 1 1u 1n 1n 10u 20u)",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Vsource,
    "instance"  : "V1",
    "type"      : "vsource",
    "value"     : ["DC", "0", "PULSE(0", "1", "1u", "1n", "1n", "10u", "20u)"],
    "ports"     : {"n0": "neta", "n1": "netb"},
    "voltage"   : "DC 0 PULSE(0 1 1u 1n 1n 10u 20u)"
    }


element_mesfet__args = {
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
    }


@pytest.fixture(params=[element_default, element_component, element_component_2t,
                        element_component_3t, element_component_4t, element_statement,
                        element_comment, element_model, element_include,
                        element_library, element_option, element_param,
                        element_global, element_subckt, element_subcktdef,
                        element_capacitor, element_diode, element_cccs,
                        element_ccvs, element_isource, element_jfet,
                        element_inductor, element_mosfet, element_bjt_3t,
                        element_bjt_4t, element_resistor, element_vsource,
                        element_mesfet, element_component__args, element_component_2t__args,
                        element_component_3t__args, element_component_4t__args,
                        element_capacitor__args, element_diode__args,
                        element_cccs__args, element_ccvs__args, element_isource__args,
                        element_jfet__args, element_inductor__args, element_mosfet__args,
                        element_bjt_3t__args, element_bjt_4t__args, element_resistor__args,
                        element_vsource__args, element_vsource__pulse,  element_mesfet__args ])
def case(request):
    return request.param


@pytest.fixture
def module(case):
    return create_module(case)


def test_elements_line(case, module):
    assert(isinstance(module.line, str))
    assert(str(module) == case["line"])
    assert(module.line == case["line"])


def test_elements_location(case, module):
    assert(isinstance(module.location, str))
    assert(module.location == case["loc"])


def test_elements_lib(case, module):
    assert(module.lib == case["lib"])


def test_elements_uid(case, module):
    assert(isinstance(module.uid, str))
    assert(module.uid == case["uid"])


def test_elements_n(case, module):
    assert(isinstance(module.n, int))
    assert(module.n == case["n"])


def test_elements_instance(case, module):
    assert(module.instance == case["instance"])


def test_elements_type(case, module):
    assert(module.type == case["type"])


def test_elements_value(case, module):
    assert(module.value == case["value"])


def test_elements_ports(case, module):
    assert(isinstance(module.ports, dict))
    assert(module.ports == case["ports"])


def test_module_library_libname():
    case = element_library
    module = create_module(case)
    assert(module.libname  == case["libname"])
    

def test_module_library_libname_set():
    case = element_library
    module = create_module(case)
    module.libname = "myname"
    assert(module.libname  == "myname")


def test_module_library_filename():
    case = element_library
    module = create_module(case)
    assert(module.filename == case["filename"])


def test_module_library_filename_set():
    case = element_library
    module = create_module(case)
    module.filename = "myfile"
    assert(module.filename == "myfile")


def test_module_param_name():
    case = element_param
    module = create_module(case)
    assert(module.name == case["name"])


def test_module_param_name_set():
    case = element_param
    module = create_module(case)
    module.name = "myname"
    assert(module.name == "myname")


def test_module_param_value():
    case = element_param
    module = create_module(case)
    assert(module.value == case["value"])


def test_module_param_value_set():
    case = element_param
    module = create_module(case)
    module.value = "myvalue"
    assert(module.value == "myvalue")


def test_module_capacitor_capacitance():
    case = element_capacitor
    module = create_module(case)
    assert(module.capacitance  == case["capacitance"])


def test_module_capacitor_capacitance_set():
    case = element_capacitor
    module = create_module(case)
    module.capacitance = "myval"
    assert(module.capacitance == "myval")


def test_module_diode_model():
    case = element_diode
    module = create_module(case)
    assert(module.model == case["model"])


def test_module_diode_model_set():
    case = element_diode
    module = create_module(case)
    module.model = "mymod"
    assert(module.model == "mymod")


def test_module_cccs_vname():
    case = element_cccs
    module = create_module(case)
    assert(module.vname == case["vname"])


def test_module_cccs_vname_set():
    case = element_cccs
    module = create_module(case)
    module.vname = "myname"
    assert(module.vname == "myname")


def test_module_cccs_value():
    case = element_cccs
    module = create_module(case)
    assert(module.value == case["value"])


def test_module_cccs_value_set():
    case = element_cccs
    module = create_module(case)
    module.value = "myval"
    assert(module.value == "myval")


def test_module_ccvs_vname():
    case = element_ccvs
    module = create_module(case)
    assert(module.vname == case["vname"])


def test_module_ccvs_vname_set():
    case = element_ccvs
    module = create_module(case)
    module.vname = "myname"
    assert(module.vname == "myname")


def test_module_ccvs_value():
    case = element_ccvs
    module = create_module(case)
    assert(module.value == case["value"])


def test_module_ccvs_value_set():
    case = element_ccvs
    module = create_module(case)
    module.value = "myval"
    assert(module.value == "myval")


def test_module_isource_current():
    case = element_isource
    module = create_module(case)
    assert(module.current == case["current"])


def test_module_isource_current_set():
    case = element_isource
    module = create_module(case)
    module.current = "mycur"
    assert(module.current == "mycur")


def test_module_jfet_model():
    case = element_jfet
    module = create_module(case)
    assert(module.model == case["model"])


def test_module_jfet_model_set():
    case = element_jfet
    module = create_module(case)
    module.model = "testmod"
    assert(module.model == "testmod")


def test_module_inductor_inductance():
    case = element_inductor
    module = create_module(case)
    assert(module.inductance == case["inductance"])


def test_module_inductor_inductance_set():
    case = element_inductor
    module = create_module(case)
    module.inductance = "myval"
    assert(module.inductance == "myval")


def test_module_mosfet_model():
    case = element_mosfet
    module = create_module(case)
    assert(module.model == "mosmodel")


def test_module_mosfet_model_set():
    case = element_mosfet
    module = create_module(case)
    module.model = "testmod"
    assert(module.model == "testmod")


def test_module_bjt_3t_model():
    case = element_bjt_3t
    module = create_module(case)
    assert(module.model == case["model"])


def test_module_bjt_3t_model_set():
    case = element_bjt_3t
    module = create_module(case)
    module.model = "testmod"
    assert(module.model == "testmod")


def test_module_bjt_4t_model():
    case = element_bjt_4t
    module = create_module(case)
    assert(module.model == case["model"])


def test_module_bjt_4t_model_set():
    case = element_bjt_4t
    module = create_module(case)
    module.model = "testmod"
    assert(module.model == "testmod")


def test_module_resistor_resistance():
    case = element_resistor
    module = create_module(case)
    assert(module.resistance == case["resistance"])


def test_module_resistor_resistance_set():
    case = element_resistor
    module = create_module(case)
    module.resistance = "myval"
    assert(module.resistance == "myval")


def test_module_vsource_voltage():
    case = element_vsource
    module = create_module(case)
    assert(module.voltage == case["voltage"])


def test_module_vsource_voltage_set():
    case = element_vsource
    module = create_module(case)
    module.voltage = "myvar"
    assert(module.voltage == "myvar")


def test_module_mesfet_model():
    case = element_mesfet
    module = create_module(case)
    assert(module.model == "mesmodel")


def test_module_mesfet_model_set():
    case = element_mesfet
    module = create_module(case)
    module.model = "testmod"
    assert(module.model == "testmod")


def test_module_behavioral_source():
    pass


def test_module_vcvs():
    pass


def test_module_vccs():
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


def test_module_subckt_name():
    case = element_subckt
    module = create_module(case)
    assert(module.name == "mysubckt")


def test_module_subckt_name_set():
    case = element_subckt
    module = create_module(case)
    module.name = "testsubckt"
    assert(module.name == "testsubckt")


def test_module_subcktdef_name():
    case = element_subcktdef
    module = create_module(case)
    assert(module.name == "mysubckt")


def test_module_subcktdef_name_set():
    case = element_subcktdef
    module = create_module(case)
    module.name = "testsubckt"
    assert(module.name == "testsubckt")


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



def test_circuit_init_simple():
    netlist = "netlists/generic/simple.sp"
    net_in = input_netlist(netlist)
    cir  = sp.Circuit(netlist)
    net_out = str(cir)
    assert(net_in == net_out)


def test_circuit_init_simple():
    netlist = "netlists/generic/simple.sp"
    net_in = input_netlist(netlist)
    cir  = sp.Circuit(netlist)
    net_out = str(cir)
    assert(net_in == net_out)


def test_circuit_init_complex():
    netlist = "netlists/generic/complex.sp"
    net_in = input_netlist(netlist)
    cir  = sp.Circuit(netlist)
    net_out = str(cir)
    assert(net_in == net_out)


def test_circuit_hierachy():
    netlist = "netlists/generic/complex.sp"
    cir = sp.Circuit(netlist)
    uid = cir.filter("instance", "r1")[0]
    assert(cir[uid].location == "root/module")
    uid = cir.filter("instance", "rs1")[0]
    assert(cir[uid].location == "root/module/submodule")


def test_circuit_hierachy_parent():
    netlist = "netlists/generic/complex.sp"
    cir = sp.Circuit(netlist)
    uid = cir.filter("instance", "xmod")[0]
    assert(cir[uid].parent == None)
    uid = cir.filter("instance", "r1")[0]
    assert(cir[uid].parent == "module")
    uid = cir.filter("instance", "rs1")[0]
    assert(cir[uid].parent == "submodule")


def test_circuit_library():
    netlist = "netlists/generic/lib.sp"
    cir = sp.Circuit(netlist)
    uid = cir.filter("instance", "r1")[0]
    assert(cir[uid].lib == "mylib")


def test_circuit_get_args():
    netlist = "netlists/generic/args.sp"
    cir = sp.Circuit(netlist)
    for uid in cir:
        assert(cir[uid].args.l == "1u")
        assert(cir[uid].args.w == "1u")
        assert(cir[uid].args.nf == "1")


def test_circuit_set_args_prop():
    netlist = "netlists/generic/args.sp"
    net_in = input_netlist(netlist)
    cir = sp.Circuit(netlist)
    for uid in cir:
        cir[uid].args.w = "2u"
    net_in = net_in.replace("w=1u", "w=2u")
    assert( str(cir) == net_in )


def test_circuit_set_args_dict():
    netlist = "netlists/generic/args.sp"
    net_in = input_netlist(netlist)
    cir = sp.Circuit(netlist)
    for uid in cir:
        cir[uid].args["w"] = "2u"
    net_in = net_in.replace("w=1u", "w=2u")
    assert( str(cir) == net_in )


def test_circuit_params():
    netlist_inp  = "netlists/generic/param/input_param.sp"
    netlist_cmp =  "netlists/generic/param/compare_param.sp"
    cir = sp.Circuit(netlist_inp, is_filename=True)
    net_out = str(cir)
    net_cmp = input_netlist(netlist_cmp, netlist_inp)
    print(net_out)
    print(net_cmp)
    assert(net_out == net_cmp)


def test_comment_characters():
    netlist = ["* This  is a comment with double space.",
               "* This is a comment * containing an astrisk.",
               "* This is a comment + containing a plus.",
               "*This is a starting right after asterisk" ]
    cir  = sp.Circuit(netlist, is_filename=False, keep_comments=True)
    netlist = [ "* Netlist\n" ] + netlist + [""]
    net_in = "\n".join(netlist)
    net_out = str(cir)
    assert(net_in == net_out)


def test_comment_inbetween():
    netlist = [".subckt testsubckt neta netb para=1 parb=2",
               "* Commment 1.",
               "* Commment 2.",
                "+ parc=3",
               "* Commment 3.",
                "+ pard=4",
               "* Commment 4.",
                ]
    netlist_target = [".subckt testsubckt neta netb para=1 parb=2 parc=3 pard=4",
               "* Commment 1.",
               "* Commment 2.",
               "* Commment 3.",
               "* Commment 4.",
                ]
    cir  = sp.Circuit(netlist, is_filename=False, keep_comments=True)
    netlist_target = [ "* Netlist\n" ] + netlist_target + [""]
    net_target = "\n".join(netlist_target)
    net_out = str(cir)
    assert(net_target == net_out)

