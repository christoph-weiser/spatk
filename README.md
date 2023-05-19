# SPATK - Spice Analysis ToolKit

Tools for handling and analyzing Spice netlists

* Provides an easy interface to netlist manipulation.
* Uses Python standard library only.
* Easy to extend. 

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

for mos in cir.mosfets:
    print(mos.model, mos.args.w)
``` 

```
pmos_3p3 1u
nmos_3p3 1u
```

### Installation

```shell
pip intall spatk
```
