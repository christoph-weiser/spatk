# SPATK - Spice Analysis ToolKit

Tools for handling and analyzing Spice netlist

* Provides easy pythonic interface to netlist manipulation
* Parses Complete SKY130 and GF180MCU PDK.
* Uses Python standard library only.
* Easy to Extend. 

### Example 

```spice
* mynetlist.spice
C1 vdd vss 1n
R1 net1 net2 1k
XM1 out in vdd vdd pmos_3p3 L=1u W=1u nf=1
XM2 out in vss vss nmos_3p3 L=1u W=1u nf=1
```

```python
import spatk

cir = spatk.Circuit("mynetlist.spice")

devs = cir.filter("type", "mosfet")

for k in devs:
    print(cir[k].type, cir[k].model)
``` 

```
mosfet pmos_3p3
mosfet nmos_3p3
```
