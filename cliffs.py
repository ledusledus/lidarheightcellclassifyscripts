import unittest
from itertools import imap
from operator import add

NO_CLIFF=1
HAS_CLIFF=2

class TestBuildCliff(unittest.TestCase):
    def setUp(self):
        pass
    def testBuild_Cliff(self):
        altitudes={(10,10):2,(10,11):4,(11,11):4,(11,10):2,(12,10):2,(12,11):4}
        key=(10,10)
        start_cliff=1
        end_cliff=99
        cliff=build_cliff(altitudes,key, start_cliff,end_cliff)
        self.assertEqual(cliff,[(10.0,10.5),(11.0,10.5)])
        key=(11,10)
        cliff=build_cliff(altitudes,key, start_cliff,end_cliff)
        self.assertEqual(cliff,[(11.0,10.5),(12.0,10.5)])

    def testBuildFullCliff(self):
        altitudes={(10,10):2,(10,11):4,(11,11):4,(11,10):2,}
        key=(10,10)
        start_cliff=1
        end_cliff=99
        cliff=build_cliff(altitudes,key, start_cliff,end_cliff)
        self.assertEqual(cliff,[(10.0,10.5),(11.0,10.5)])
        cells={}
        res=build_full_cliff(cells,altitudes,key, start_cliff,end_cliff)
        self.assertEqual(res, [[(10.0,10.5),(11.0,10.5)]])
        cells={}
        altitudes={(10,10):2,(10,11):4,(11,11):4,(11,10):2,(12,10):2,(12,11):4}
        res=build_full_cliff(cells,altitudes,key, start_cliff,end_cliff)
        self.assertEqual(res, [[(10.0,10.5),(11.0,10.5)],[(11.0,10.5),(12.0,10.5)]])

def divide_by_scalar(vector,scalar):
    return tuple(i/scalar for i in vector)

def build_cliff( altitudes, key, start_cliff, end_cliff ):
    keys = [key, (key[0]+1,key[1]), (key[0]+1,key[1]+1), (key[0],key[1]+1)]
    alts = []
    for k in keys:
        # we need to have a full cell and there is none
        if not altitudes.has_key(k):
            return None
        alts.append(altitudes[k])
    deltas=[(abs(alts[(i+1)%4]-alts[i]),i) for i in range(len(alts))]
    good_deltas = filter(lambda x: x[0]>=start_cliff and x[0]<end_cliff, deltas)
    if len(good_deltas)>2:
        print "special case good deltas"
    if len(good_deltas) < 2: # no cliffs found
        # 1 means we are at the end. In that case it should be found from another cliff.
        return None   
    good_deltas.sort(reverse=True)

    idx1=good_deltas[0][1]
    idx2=good_deltas[1][1]
    if alts[idx1]<alts[(idx1+1)%4]:
        idx1,idx2=idx2,idx1

    cliff_line=[divide_by_scalar(imap(add, keys[idx1],keys[(idx1+1)%4]),2.0), 
                divide_by_scalar(imap(add, keys[idx2],keys[(idx2+1)%4]),2.0),]
    return cliff_line

def next_key(key, point):
    if point[0]==key[0]:
        return (key[0]-1,key[1])
    if point[0]==key[0]+1:
        return (key[0]+1,key[1])
    if point[1]==key[1]:
        return (key[0],key[1]-1)
    return key[0],key[1]+1

def build_full_cliff(cells, altitudes, key, start_cliff, end_cliff ):
    cliff_line = build_cliff(altitudes, key, start_cliff, end_cliff )
    if cliff_line == None:
        cells[key]=NO_CLIFF
        return
    else:
        cells[key]=HAS_CLIFF
    curkey=key
    full_cliff_lines=[cliff_line]
    curpoint=full_cliff_lines[-1][1]
    # now we need to grow right:
    while True:       
        curkey=next_key(curkey, curpoint)
        if cells.has_key(curkey):
            # has been visited already
            break
        print curkey
        cliff_line=build_cliff(altitudes, curkey, start_cliff, end_cliff )
        print cliff_line
        if cliff_line==None:
            cells[curkey]=NO_CLIFF
            break
        if cliff_line[0]!=full_cliff_lines[-1][1]:
            # this is not our cliff
            break
        cells[curkey]=HAS_CLIFF
        full_cliff_lines.append(cliff_line)
        print full_cliff_lines
        curpoint=full_cliff_lines[-1][1]
    # todo: then we need to grow left
    return full_cliff_lines

if __name__ == '__main__':
    unittest.main()
