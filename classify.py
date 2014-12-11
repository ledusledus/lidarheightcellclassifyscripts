import sys
from constants import *
from cc import *
# given an input file of cells, encodes them by type
# for example: 123123 123123 .2 .3 0 0 0 .5 .6 .7 12.2 23 becomes 123123 123123 2

in_file=file(sys.argv[1],"rt")
out_file=file(sys.argv[2],"wt")

FOREST_THRESHOLD = .2
# amount of really short vs amount of bush points, so if really short is small and bush points many then 
VERY_GREEN_THRESHOLD = .2
THRESHOLD2 = 1
THRESHOLD3 = 2

total = 0
def find_cell_type(cell):
    """
    input of cell is a set of altitudes.

    this is the most interesting function for finding some classification
    we should return the following types
    1 open forest - white
    2 green 1 forest 
    3 green 2 forest 
    4 green 3 - most green, does not have to be forest
    5 open clear
    6 open rough

    all, but 4 can be accompanied with undergrowth - 
    7 undergrowth 1
    8 undergrowth 2

    we will simplify:
    it can be 
    1 most green 
    or then either forest or rough open
    rough open is when maximum height is less than 2 meters
    forest when above: maximum height is 5 % more above 2 mentioned meters
    now we look at density of points between OPEN_MAX_HEIGHT and 2 meters vs < 2 meters to figure out whether we need stuffs 
    so we have the ratio of #(points between OPEN_MAX_HEIGHT and 2)/#(points < .2) --> need to experiment on that.

    what is most green? the same classification.
    """
    lessthanMAX_OPEN = cell[0]
    UNDERGROWTH = cell[1]
    morethan2 = cell[2]
    all_points = lessthanMAX_OPEN+UNDERGROWTH+morethan2
    global total
    total += all_points
    ratio = float(lessthanMAX_OPEN+1)/float(1+UNDERGROWTH)
    is_forest = float(morethan2) / float(all_points) > FOREST_THRESHOLD
    return is_forest, ratio

def encoded_cell_type(cell):
    is_forest, ratio = find_cell_type(cell)
    if ratio < VERY_GREEN_THRESHOLD:
        return 0
    idx = 1
    if is_forest:
        idx = 4
    if ratio < THRESHOLD2:
        idx += 2
    elif ratio < THRESHOLD3:
        idx += 1
    else:
        idx += 0
    return idx    

cc=CellTypeContainer(encoded_cell_type)
    
for line in in_file:
    arr=line.split()
    cc.add_all_points((arr[0],arr[1]),[float(i) for i in arr[2:]])

# filter off one-offs
# cc.remove_one_offs()
cc.remove_those_with_no_brothers()

keys = cc.cells.keys()
keys.sort()
for idx in keys:
    res=[idx[0],idx[1],cc.cells[idx]]
    out_file.write(" ".join([str(i) for i in res])+"\n")

print "full point count:", total