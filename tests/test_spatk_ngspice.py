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

import os
os.environ["SPICE_SYNTAX"] = "ngspice"

import pytest
import spatk as sp
import spatk.elements as spe

from helpers import create_module

CASES = {
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
}


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


def test_module_xspice():
    pass


def test_module_numerical_device_gss():
    pass


def test_module_single_lossy_transmission_line():
    pass
