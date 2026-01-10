import spatk

netlist = [ "* mynetlist.spice",
            "C1 vdd vss 1n",
            "R1 net1 net2 1k",
            "XM1 out in vdd vdd pmos_3p3 L=1u W=1u nf=1"]

cir = spatk.Circuit(netlist, syntax="ngspice", is_filename=False)

uids = cir.filter("type", "mosfet")

for uid in uids:
    cir[uid].args.w = "2u"

print(cir)
