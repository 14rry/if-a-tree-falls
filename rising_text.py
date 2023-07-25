import pyxel

class RisingText:
    def __init__(self,x,y,text="Good",color=3):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.done = False
    
    def update(self):
        if self.y > -8:
            self.y -= 1
        else:
            self.done = True

    def draw(self):
        #pyxel.text(self.x+1,self.y+1,self.text,0)
        pyxel.text(self.x,self.y,self.text,self.color)
