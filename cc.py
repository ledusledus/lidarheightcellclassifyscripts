from constants import *

class CellContainer:
    cells = {}
    def __init__(self,cell_size):
        self.cell_size = cell_size
    def idx(self, point):
        return (int(point[0])/self.cell_size, int(point[1])/self.cell_size)
    def add_all_points(self,point,arr):
        idx = self.idx(point)
        self.cells[idx]=arr
    def add_point(self, point):
        idx = self.idx(point)
        if not self.cells.has_key(idx):
            self.cells[idx] = [0,0,0]
        i = 0
        if point[2] > FOREST_BEGIN_HEIGHT:
            i = 2
        elif point[2] > OPEN_MAX_HEIGHT:
            i = 1
        self.cells[idx][i]+=1
    def cell_keys(self):
        return self.cells.keys()
    def cell(self, key):
        return self.cells[key]

#http://stackoverflow.com/questions/1518522/python-most-common-element-in-a-list
def most_common(lst):
    return max(set(lst), key=lst.count)

class CellTypeContainer(CellContainer):
    def __init__(self, classifier):
        self.cell_size = 1
        self.classify = classifier
    def add_all_points(self,point,arr):
        idx = self.idx(point)
        self.cells[idx]=self.classify(arr)
    def update_type(self,point,symbol):
        idx = self.idx(point)
        self.cells[idx]=symbol
    def neighbour_types(self, idx):
        types=[]
        for i in range(-1,2):
            for j in range(-1,2):
                if j == 0 and i == 0: continue
                _tidx = (idx[0]+self.cell_size*i,idx[1]+self.cell_size*j)
                if self.cells.has_key(_tidx):
                    types.append(self.cells[_tidx])
        return types       
    def remove_one_offs(self):
        for idx in self.cells.keys():
            types=self.neighbour_types(idx)
            if len(types)==0: continue
            for t in types:
                if t != types[0]: break
            if t==types[0]:
                self.cells[idx] = t
    def remove_those_with_no_brothers(self):
        for idx in self.cells.keys():
            types=self.neighbour_types(idx)
            selftype=self.cells[idx]
            if len(types) != 8: continue
            for t in types:
                if t == selftype:
                    break
            if t == selftype: continue
            self.cells[idx]= most_common(types)
        