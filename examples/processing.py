import spatk

netlist = [ "* mynetlist.spice",
            "C1 vdd vss 1n",
            "R1 net1 net2 1k",
            "XM1 out in vdd vdd pmos_3p3 L=1u W=1u nf=1",
            "XM2 out in vss vss nmos_3p3 L=1u W=1u nf=1"]

cir = spatk.Circuit(netlist, syntax="ngspice", is_filename=False)

# Looping through all netlist elements by 
# uid (unique identifier)
for uid in cir:
    print(cir[uid])


# Filter circuit by property
uids = cir.filter("type", "mosfet")
for uid in uids:
    print(cir[uid])
