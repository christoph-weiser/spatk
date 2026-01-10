# SPATK - Spice Analysis ToolKit
# Copyright (C) 2026 Christoph Weiser
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
import spatk.flavours.xyce as spe

from helpers import create_module

element_option = {
    "line"      : ".option pkg setting=value",
    "loc"       : "/",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Option,
    "instance"  : None,
    "type"      : "option",
    "value"     : "value",
    "ports"     : dict(),
    }

element_print = {
    "line"      : '.print tran format="csv" file="file.csv" v(n1) v(n2) v(n3)',
    "loc"       : "/",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Print,
    "instance"  : None,
    "type"      : "print",
    "value"     : "v(n1) v(n2) v(n3)",
    "ports"     : dict(),
    }


@pytest.fixture(params=[element_option, element_print])
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


def test_module_option_pkg():
    case = element_option
    mod = create_module(case)
    assert(mod.pkg == "pkg")


def test_module_option_pkg_set():
    case = element_option
    mod = create_module(case)
    mod.pkg = "mypkg"
    assert(mod.pkg == "mypkg")


def test_module_option_setting():
    case = element_option
    mod = create_module(case)
    assert(mod.name == "setting")


def test_module_option_setting_set():
    case = element_option
    mod = create_module(case)
    mod.pkg = "mysetting"
    assert(mod.pkg == "mysetting")


def test_module_option_value():
    case = element_option
    mod = create_module(case)
    assert(mod.value == "value")


def test_module_option_value_set():
    case = element_option
    mod = create_module(case)
    mod.value = "myvalue"
    assert(mod.value == "myvalue")


def test_module_print_value_set():
    case = element_print
    mod = create_module(case)
    mod.value = "myvalue"
    assert(mod.value == "myvalue")


def test_module_print_value_set_list():
    case = element_print
    mod = create_module(case)
    mod.value = ["1", "2", "3"]
    assert(mod.value == "1 2 3")


def test_module_print_args():
    case = element_print
    mod = create_module(case)
    assert(mod.args == {"format": '"csv"', "file": '"file.csv"'} )


def test_module_print_args_set():
    case = element_print
    mod = create_module(case)
    mod.args["format"] = "test"
    assert(mod.args["format"] == "test")
    assert(mod.args["file"] == '"file.csv"')
