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
os.environ["SPICE_SYNTAX"] = "ngspice"

import pytest
import spatk as sp
import spatk.elements as spe

from helpers import create_module


element_function = {
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
    }

element_temp = {
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
    }

@pytest.fixture(params=[element_function, element_temp])
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

def test_module_xspice():
    pass


def test_module_numerical_device_gss():
    pass


def test_module_single_lossy_transmission_line():
    pass
