import sys
# given an input file, finds cells, denotes them by 
# x/size y/size followed by a list of point height values.
# for example 123123 123123 .2 .3 0 0 0 .5 .6 .7 12.2 23
from constants import *
from cc import *

out_file=file(sys.argv[1],"wt")
CELL_SIZE=int(sys.argv[2])
in_files=sys.argv[3:]


cc=CellContainer(CELL_SIZE) # five meter cells.
DEBUG=0
c=0

for filename in in_files:
    in_file=file(filename,"rt")
    for line in in_file:
        c+=1
        if DEBUG:
            if c>2: break
        (x,y,z)=[float(i) for i in line.split()[0:3]]
        cc.add_point((x,y,z))
        if c % 1000000 == 0: print c
    
keys = cc.cell_keys()
keys.sort()
for key in keys:
    cell=cc.cell(key)
    res = " ".join([str(i) for i in key])+" "+" ".join([str(i) for i in cell]) + "\n"
    out_file.write(res)
