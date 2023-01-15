# SPATK - Spice Analysis ToolKit

Tools for handling and analyzing Spice netlist

* Provides easy pythonic interface to netlist manipulation
* Parses Complete SKY130 and GF180MCU PDK.
* Easy to Extend. 

### Example 

```spice
* mynetlist.spice
C1 vdd vss 1n
R1 net1 net2 1k
```

```python
import spatk

cir = spatk.Circuit("mynetlist.spice")

for uid in cir:
  print(cir[uid].type, cir[uid].value)
``` 

```
capacitor 1n
resistor 1k
```
