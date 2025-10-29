j# SPATK - Spice Analysis ToolKit

Tools for handling and analyzing Spice netlists

* Provides an easy interface to netlist manipulation.
* Uses Python standard library only.
* Easy to extend. 

### Example 

```spice
* mynetlist.spice
VDD vdd vss 1
VSS vss 0   0
R1  vdd n1  1k
R2  n1  vss 2k
X1  vdd vss sr

.subckt sr n1 n2
R3  n1  n2  3k
.ends
```

```python
import spatk

cir = spatk.Circuit("mynetlist.spice")

for res in cir.resistors:
    print(res.instance, res.resistance, res.location)
``` 

```
r1 1k /
r2 2k /
r3 3k /sr
```

### Installation

```shell
pip intall spatk
```
