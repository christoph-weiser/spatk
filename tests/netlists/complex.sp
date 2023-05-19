xmod 1 2 3 4 module
.subckt module 1 2 3 4
b1 1 2 i=1
c1 1 2 1e-12
d1 1 2 dmod
e1 1 2 3 4 1
f1 1 2 vsrc 1
g1 1 2 3 4 1
h1 1 2 vsrc 1
i1 1 2 1
j1 1 2 3 jmod
l1 1 2 1e-6
m1 1 2 3 4 mmod
q1 1 2 3 qmod
r1 1 2 1e3
v1 1 2 1
vsrc 1 2 1
x1 1 2 submodule
z1 1 2 3 zmod
.subckt submodule 1 2
rs1 1 2 1e3
.ends
.param mypar=1
.model dmod d is=1e-9
.model qmod npn is=1e-15 bf=1e3
.model jmod pjf is=15e-12 beta=300e-6 vto=-1
.model mmod nmos l=2e-6 w=10e-6 kp=200e-6 level=1
.model zmod nmf level=1
.ends
.lib mylib
.model libmod d is=1e-9
.endl
