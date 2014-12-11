import sys
sys.path.append("c:\\projekti\\writeodll\\python")
from constants import *
from dllwrapper import *

def readline(cell, multiplier):
    line=cell.split()
    (x,y,_type)=float(line[0]),float(line[1]),int(line[2])
    x*=multiplier
    y*=multiplier
    return (x,y,_type)

in_file = file(sys.argv[1], "rt")
multiplier = int(sys.argv[2])
out_filename= sys.argv[3]
offsetx=0
offsety=0
scale=10000

# read only one line if possible
for cell in in_file:
    (x,y,_type) = readline(cell, multiplier)
    offsetx=x
    offsety=y
    break;

#reset file
in_file = file(sys.argv[1], "rt")

h_writer=CreateOcadWriter(c_double(offsetx),c_double(offsety), c_double(scale))

col=AddColor(h_writer, c_char_p("some color"))
_green=4100
AddAreaSymbol(h_writer,c_char_p("green"), _green, col)
_open=4030
AddAreaSymbol(h_writer,c_char_p("open"), _open, col)
_undergrowth=4070
AddAreaSymbol(h_writer,c_char_p("undergrowth"), _undergrowth, col)
_undergrowthBad=4090
AddAreaSymbol(h_writer,c_char_p("undergrowthBad"), _undergrowthBad, col)
_open_forest_slow=4060
AddAreaSymbol(h_writer,c_char_p("open_forest_slow"), _open_forest_slow, col)
_open_forest_slowest=4080
AddAreaSymbol(h_writer,c_char_p("open_forest_slowest"), _open_forest_slowest, col)

CELL_SYMBOLS = {
    "green":[_green],
    "open":[_open],
    "open_slow":[_open,_undergrowth],
    "open_slowest":[_open,_undergrowthBad],
    "open_forest_slow":[_open_forest_slow],
    "open_forest_slowest":[_open_forest_slowest],
    "open_forest":[], # no symbol there
}

#TYPE0="green"
#TYPE1="open"
#TYPE2="open_slow"
#TYPE3="open_slowest"
#TYPE4="open_forest"
#TYPE5="open_forest_slow"
#TYPE6="open_forest_slowest"
#CELL_TYPES=[TYPE0,TYPE1,TYPE2,TYPE3,TYPE4,TYPE5,TYPE6,]

idx = 0
TYPE=(POINT*4)
for cell in in_file:
    (x,y,_type)=readline(cell, multiplier)
    x-=offsetx
    y-=offsety
    points = [(x,y)]
    points.append((x,y+multiplier))
    points.append((x+multiplier,y+multiplier))
    points.append((x+multiplier,y))
    #points.append((x,y))
    t=TYPE()
    i=0
    for point in points:
        t[i].x=int(point[0])
        t[i].y=int(point[1])
        i+=1
    for sym in CELL_SYMBOLS[CELL_TYPES[_type]]:
        #print sym
        ExportArea(h_writer, t, 4, sym)
    #print points
    idx += 1
    if idx == 100000: print idx

WriteOcadFile(h_writer, c_char_p(out_filename))
CleanWriter(h_writer)

print "DONE!"
