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

def create_module(case):
    """ Helper function for create modules. """
    module = case["mod"]
    line = case["line"]
    loc = case["loc"]
    lib = case["lib"]
    n = case["n"]
    uid = case["uid"]
    return module(line, loc, lib, n, uid)


def input_netlist(filename, name=None):
    """ helper function to create equivalent input netlist """
    with open(filename, "r") as ifile:
        if name:
            net_in = "* {}\n\n".format(name) + (ifile.read()).lower()
        else:
            net_in = "* {}\n\n".format(filename) + (ifile.read()).lower()
    return net_in
