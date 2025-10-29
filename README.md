# SPATK - Spice Analysis ToolKit

Tools for handling and analyzing Spice netlists

* Provides an easy interface to netlist manipulation.
* Uses Python standard library only.
* Easy to extend.

### Installation

```shell
pip intall spatk
```

### Example 

```spice
* mynetlist.spice

vdd vdd vss 1
vss vss 0   0
r1  vdd n1  1k
r2  n1  vss 2k
x1  vdd vss sr

.subckt sr n1 n2
r3  n1  n2  3k
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
