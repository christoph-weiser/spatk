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
os.environ["SPICE_SYNTAX"] = "xyce"

import pytest
import spatk as sp
import spatk.elements as spe

from helpers import create_module

CASES = {
"option":
{
    "line"      : ".option pkg setting=value",
    "loc"       : "root",
    "lib"       : None,
    "n"         : 1,
    "uid"       : "testuid",
    "mod"       : spe.Option,
    "instance"  : None,
    "pkg"       : "bla",
    "type"      : "option",
    "name"      : "setting",
    "value"     : "value",
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



def test_module_option():
    """ Test option module specific properties """
    case = CASES["option"]
    mod = create_module(case)

    assert(mod.pkg == "pkg")
    mod.pkg = "mypkg"
    assert(mod.pkg == "mypkg")

    assert(mod.name == "setting")
    mod.pkg = "mysetting"
    assert(mod.pkg == "mysetting")

    assert(mod.value == "value")
    mod.value = "myvalue"
    assert(mod.value == "myvalue")


