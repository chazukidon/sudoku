import numpy as np
import pyxel

class Sudoku:
    def __init__(self):
        self.sudoku=np.zeros((9,9),dtype=int)
        self.sudoku_size=18
        self.solving=True


    def output_number_info(self,sch_idx):
   
        block=[i for i in [self.sudoku[y,x]  for x in  range(sch_idx[1]//3*3,sch_idx[1]//3*3+3)  for y in range(sch_idx[0]//3*3,sch_idx[0]//3*3+3)] if i!=0]
        row=[i for i in self.sudoku[sch_idx[0]] if i!=0]
        column=[i for i in self.sudoku[:,sch_idx[1]] if i!=0]
        return block,row,column
    
    def put_number(self):
        x=pyxel.mouse_x//self.sudoku_size
        y=pyxel.mouse_y//self.sudoku_size

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.sudoku[y,x]==9:
                self.sudoku[y,x]=0
            else:
                self.sudoku[y,x]+=1
                
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            if self.sudoku[y,x]==0:
                self.sudoku[y,x]=9
            else:
                self.sudoku[y,x]-=1
          

    def solve_judge(self):
        for x in range(9):
            for y in range(9):
                block,row,column=self.output_number_info(np.array([y,x]))
                if np.size(np.unique(block))!=np.size(block) or np.size(np.unique(row))!=np.size(row) or np.size(np.unique(column))!=np.size(column):
                    return False
        return True

    def solve(self,sch_idx):

        block,row,column=self.output_number_info(sch_idx)
        candidate=np.array([i for i in range(1,10) if i not in np.concatenate([block,row,column])])
        zero_idx=np.array(np.where(self.sudoku==0)).T
        for i in candidate:
            if self.solving:
                self.sudoku[tuple(sch_idx)]=i
                if np.count_nonzero(self.sudoku)==81:
                    self.solving=False
                else:
                    self.solve([zero_idx[i+1] for i in range(np.size(zero_idx)//2) if all(zero_idx[i]==sch_idx)][0])
                    if self.solving:
                        self.sudoku[tuple(sch_idx)]=0


    def draw_sudoku(self):
            
            for i in range(10):
                pyxel.line(0,i*self.sudoku_size,pyxel.width,i*self.sudoku_size,6)
                pyxel.line(i*self.sudoku_size,0,i*self.sudoku_size,pyxel.height,6)
            for i in range(3,9,3):
                pyxel.line(0,i*self.sudoku_size,pyxel.width,i*self.sudoku_size,5)
                pyxel.line(i*self.sudoku_size,0,i*self.sudoku_size,pyxel.height,5)   
            for x in range(9):
                for y in range(9):
                    if self.sudoku[y,x]!=0:
                        pyxel.text(self.sudoku_size//2-1+x*self.sudoku_size,self.sudoku_size//2-2+y*self.sudoku_size,str(self.sudoku[y,x]),0)
class Run(Sudoku):
    def __init__(self):
        Sudoku.__init__(self)
        pyxel.init(self.sudoku_size*9+1,self.sudoku_size*9+1,fps=60,title='sudoku solver')
        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)
        
    def update(self):
        if np.count_nonzero(self.sudoku)!=81:
            self.put_number()
          
        if pyxel.btnp(pyxel.MOUSE_BUTTON_MIDDLE) and self.solve_judge():
            if np.count_nonzero(self.sudoku)!=81:
                self.solve(np.array(np.array(np.where(self.sudoku==0)).T[0]))
            else:
                Sudoku.__init__(self)
    def draw(self):
        pyxel.cls(7)
        self.draw_sudoku()
Run()
