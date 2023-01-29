import spatk

netlist = [ "* mynetlist.spice",
            "C1 vdd vss 1n",
            "R1 net1 net2 1k",
            "XM1 out in vdd vdd pmos_3p3 L=1u W=1u nf=1",
            "XM2 out in vss vss nmos_3p3 L=1u W=1u nf=1"]

cir = spatk.Circuit(netlist, is_filename=False)

for mos in cir.mosfets:
    print(mos.model, mos.w)
