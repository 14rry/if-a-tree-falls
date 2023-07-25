import pyxel
from ntimer import NTimer
import sound_lookup
import config

class BGM:
    def __init__(self,music_num):
        self.music_num = music_num
        pyxel.playm(self.music_num,loop=True)
        self.start_tick = pyxel.frame_count
        self.timers = []
        self.health = 0
        self.max_health = 5
        self.is_hurt = False
        self.og_colors = pyxel.colors.to_list()
        self.is_gray = False
        #self.toggle_gray()
        self.offset = 42
        self.active = False
        self.all_muted = True

    def toggle_gray(self):
        if self.is_gray:
            pyxel.colors.from_list(self.og_colors)
            self.is_gray = False
        else:
            new_cols = []
            # https://stackoverflow.com/questions/16858811/how-to-convert-hex-color-to-hex-black-and-white
            for idx,col in enumerate(self.og_colors):
                if idx == 8:
                    new_cols.append(col)
                    continue
                r = col >> 16
                g = (col >> 8) & 0xff
                b = col & 0xff
                bnw = int(r * 0.299 + g * 0.587 + b * 0.114) & 0xff
                new_cols.append((bnw << 16) | (bnw << 8) | bnw)

            pyxel.colors.from_list(new_cols)
            self.is_gray = True

    def set_melody_vol(self,vol_str):
        all_snds = pyxel.music(self.music_num).snds_list
        for val in all_snds[2]:
            print(val)
            pyxel.sound(val).set_volumes(vol_str)
        for val in all_snds[1]:
            print(val)
            pyxel.sound(val).set_volumes(vol_str)

        pyxel.playm(self.music_num,loop=True)

    def mute_melody(self):
        print('muting')
        pyxel.stop(1)
        pyxel.stop(2)
        self.toggle_gray()
        #self.set_melody_vol('0')        

    def unmute_melody(self):
        print('unmuting')
        if self.is_gray:
            self.toggle_gray()

        # brute force resuming at same tick... could be done better with math
        pos = pyxel.play_pos(3)
        new_pos = 0
        test = 0
        while (new_pos != pos[1]):
            pyxel.playm(self.music_num,tick=test,loop=True)
            (_,new_pos) = pyxel.play_pos(3)
            test += 1
            #print(pos,new_pos,test-1)

    # return False if no damage to player
    # return True if damage to player
    def update(self,can_hurt=True):
        damage_player = False

        config.music_tick = (pyxel.frame_count - self.start_tick - self.offset) % 60
        #print(config.music_tick)

        if self.active:
            if config.music_tick == 0:
                self.timers.append(NTimer(pyxel.width - 4*8,pyxel.height - 4*8,30,'^',sound_lookup.none,True,sound_lookup.hurt))

            if self.all_muted:
                self.music_num = 1
                self.unmute_melody()
                self.all_muted = False

            new_timers = []
            for val in self.timers:
                val.update()
                if not val.is_done:
                    new_timers.append(val)
                else:
                    if not val.good: 
                        if can_hurt:
                            self.health -= 1
                            if self.health < 0:
                                damage_player = True
                                self.health = 0
                                if not self.is_hurt:
                                    self.is_hurt = True
                                    #self.mute_melody()
                    else:
                        config.bgm_score += 1
                        self.health += 1
                        if self.health > 2:
                            if self.is_hurt:
                                self.is_hurt = False
                                #self.unmute_melody()
                        if self.health > self.max_health:
                            self.health = self.max_health

            self.timers = new_timers

        return damage_player

    def draw(self):
        if self.active:
            for val in self.timers:
                val.draw()

            pyxel.rect(0,pyxel.height-4,pyxel.width*(self.health/self.max_health),4,2)
            # tw = pyxel.width/self.max_health
            # pyxel.rectb(0,2,tw,3,1)
            # pyxel.rectb(tw,2,tw,3,1)
            # pyxel.rectb(2*tw,2,tw,3,1)
            # pyxel.rectb(3*tw,2,tw,3,1)
            # pyxel.rectb(4*tw,2,tw,3,1)
