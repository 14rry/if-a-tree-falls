import pyxel

# util functions
def dist(x1,y1,x2,y2):
    return (x2-x1)**2 + (y2-y1)**2

class Ai:
    def __init__(self,x,y):
        self.x = x*8
        self.y = y*8
        self.target = None
        self.tile = [1,0]
        self.speed = .7
        self.is_chopping = False
        self.chop_timer = None
        self.y_off = 0

    def move_toward_target(self):
        dir = [0,0]
        if self.x > self.target.x:
            dir[0] = -1
        elif self.x < self.target.x:
            dir[0] = 1

        if self.y > self.target.y:
            dir[1] = -1
        elif self.y < self.target.y:
            dir[1] = 1

        self.x = self.x + self.speed*dir[0]
        self.y = self.y + self.speed*dir[1]

    def update(self):
        self.y_off = (pyxel.frame_count%60) / 60

        if self.target == None:
            return

        if dist(self.x,self.y,self.target.x,self.target.y) > 64:
            self.move_toward_target()
            
        elif not self.is_chopping and self.target.health > 0:
            self.is_chopping = True
            self.chop_timer = self.target.start_timer()
            return self.chop_timer

        elif self.chop_timer is not None:
            if self.chop_timer.is_done:
                self.is_chopping = False
                if self.chop_timer.good:
                    self.target.health -= 1


    def draw(self):
        pyxel.blt(self.x,self.y+self.y_off,0,self.tile[0]*8,self.tile[1]*8,8,8,0)
