import sys
from constants import *
from dxfwrite import DXFEngine
import dxfwrite

in_file = file(sys.argv[1], "rt")
multiplier = int(sys.argv[2])
drawing = DXFEngine.drawing(sys.argv[3])

for i in range(len(CELL_TYPES)):
    drawing.add_layer(CELL_TYPES[i], color=2+i)

#TYPE0="green"
#TYPE1="open"
#TYPE2="open_slow"
#TYPE3="open_slowest"
#TYPE4="open_forest"
#TYPE5="open_forest_slow"
#TYPE6="open_forest_slowest"
#CELL_TYPES=[TYPE0,TYPE1,TYPE2,TYPE3,TYPE4,TYPE5,TYPE6,]

for cell in in_file.readlines():
    line=cell.split()
    (x,y,_type)=float(line[0]),float(line[1]),int(line[2])
    x*=multiplier
    y*=multiplier
    points = [(x,y)]
    points.append((x,y+5))
    points.append((x+5,y+5))
    points.append((x+5,y))
    points.append((x,y))
    drawing.add(DXFEngine.polyline(points, layer=CELL_TYPES[_type]))
drawing.save()

print "DONE!"
