import pyxel
from rising_text import RisingText
import sound_lookup
from utils import JitterPos
import config

class NTimer:
    def __init__(self,x,y,time,btn_str,end_sound,active=True,bad_sound=sound_lookup.hurt):
        self.pos = JitterPos(x,y,20)
        self.x = self.pos.x_off
        self.y = self.pos.y_off
        self.time = time
        self.btn_str = btn_str
        self.is_done = False
        self.pressed = False
        self.good = False
        self.text = None
        self.done_cooldown = 30
        self.active = active
        self.end_sound = end_sound
        self.bad_sound = bad_sound
        self.is_started = False

    def grade_timing(self):
        if self.pressed:
            return

        if self.time < 20 and self.time > -5:
            self.good = True
            if self.time < 10 and self.time > 0:
                self.text = RisingText(self.x,self.y,text="Great!",color=3)
            else:
                self.text = RisingText(self.x,self.y,text="Good",color=3)
        elif self.time >= 20:
            self.text = RisingText(self.x,self.y,text="Early",color=0)
        else:
            self.text = RisingText(self.x,self.y,text="Late",color=0)

        self.pressed = True
        self.active = False

    def update(self):

        if self.is_started == False:
            # wait for music beat to start
            tick = config.music_tick

            if tick == 0:
                self.is_started = True

            return True

        self.pos.update()
        self.x = self.pos.x_off
        self.y = self.pos.y_off

        if self.text is not None:
            self.text.update()

        if self.time > -10:
            self.time -= 1
        else:
            if self.active:
                self.active = False
            if self.text is None:
                pyxel.play(0,self.bad_sound)
                self.pos.start()
                self.text = RisingText(self.x,self.y,text="Missed",color=0)

            self.done_cooldown -= 1
            if self.done_cooldown < 0:
                self.is_done = True
                if not self.good:
                    return False

        if self.time < 60 and self.get_input():
            self.grade_timing()
            if self.good:
                pyxel.play(0,self.end_sound)
            else:
                self.pos.start()
                pyxel.play(0,self.bad_sound)


        return True

    def get_input(self):
        if not self.active:
            return False

        right_key = []

        if self.btn_str == 'z':
            right_key = [pyxel.KEY_Z, pyxel.GAMEPAD1_BUTTON_A]
        elif self.btn_str == 'x':
            right_key = [pyxel.KEY_X, pyxel.GAMEPAD1_BUTTON_B]
        elif self.btn_str == '^':
            right_key = [pyxel.KEY_UP, pyxel.GAMEPAD1_BUTTON_DPAD_UP]

        for val in right_key:
            if pyxel.btnp(val):
                return True

        return False

    def draw(self):

        if self.text is not None:
            self.text.draw()

        if self.is_done:
            return
        
        if self.time > 0:
            if self.pressed:
                pyxel.circ(self.x,self.y,self.time,8)
            else:
                pyxel.circb(self.x,self.y,self.time,8)

            if self.time < 20:
                pyxel.circb(self.x,self.y,self.time,0)

        if self.time < 60:
            xl = self.x
            yl = self.y
            col = 0
            if self.good:
                pyxel.circ(xl,yl,4,3)
                pyxel.circb(xl,yl,4,0)
            else:
                pyxel.circ(xl,yl,4,0)
            pyxel.text(xl-1.5,yl-2.5,self.btn_str,8)


class MultiTimer(NTimer):
    def __init__(self,timers):
        self.timers = timers
        self.is_done = False
        self.active_idx = 0
        self.good = False
        # for val,idx in enumerate(timers):
        #     if val.active:
        #         self.active_idx = idx

    def update(self):
        all_bad = True
        for timer in self.timers:
            if timer.active:
                ret_val = timer.update()
            else:
                timer.update()

            if timer.good:
                all_bad = False

        if self.active_idx < len(self.timers)-1:
            if not self.timers[self.active_idx].active:
                self.active_idx += 1
                self.timers[self.active_idx].active = True
        else:
            self.is_done = self.timers[self.active_idx].is_done

        if self.is_done:
            if not all_bad:
                self.good = True
            return not all_bad

        return True

    def draw(self):
        for timer in self.timers:
            timer.draw()
