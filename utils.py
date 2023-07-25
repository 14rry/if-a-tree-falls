import pyxel

class JitterPos:
    def __init__(self,x,y,duration,start=False):
        self.rand_x_off = []
        self.rand_y_off = []
        self.x = x
        self.y = y
        self.x_off = x
        self.y_off = y
        if start:
            self.idx = 0
        else:
            self.idx = duration
        self.duration = duration

    def update(self):
        if self.idx > self.duration:
            return

        self.x_off = self.x + pyxel.rndi(-2,2)
        self.y_off = self.y + pyxel.rndi(-2,2)
        self.idx += 1

        if self.idx > self.duration:
            self.x_off = self.x
            self.y_off = self.y

    def start(self):
        self.idx = 0

