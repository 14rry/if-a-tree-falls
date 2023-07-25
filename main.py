import pyxel
from ntimer import NTimer, MultiTimer
import sound_lookup
from rising_text import RisingText
from bgm import BGM
import basic_menu
from ai import Ai
import config

class Level:
    def __init__(self,x1,y1,w,h):
        self.x1 = x1
        self.y1 = y1
        self.w = w
        self.h = h
        self.index = 0
        self.max_level = 3
        self.ai = []
        self.level_objs = []
        self.build_level_objs()
        self.bgm_active = False
        self.inter_level_message_delay = 5*60
        self.delay_timer = 0

    def build_level_objs(self):

        # # skip level for testing
        # if self.index == 1:
        #     self.index = 2

        if self.index == 0:
            self.ai = [Ai(4,12)]
            self.level_objs = [Tree(12,13,health = 1,make_bad_sound=False)]
        elif self.index == 1:
            self.ai = [Ai(4,4)]
            self.level_objs = [Tree(10,4,health=3), Mine(4,12)]
        elif self.index == 2:
            self.level_objs = [BGM_Obj()]
            self.bgm_active = True
        elif self.index == 3:
            self.level_objs = [Tree(6,6)]
            self.ai = [Ai(4,12)]
        else:
            if pyxel.rndi(0,1) == 0:
                self.level_objs.append(Tree(pyxel.rndi(1,14),pyxel.rndi(1,14)))
            else:
                self.level_objs.append(Mine(pyxel.rndi(1,14),pyxel.rndi(1,14)))

    def next_level(self):
        self.index += 1
        self.build_level_objs() 

    def draw(self):
        pyxel.bltm(0,0,0,self.x1,self.y1,self.w*8,self.h*8)

        if self.bgm_active:
            if config.bgm_score < 8:
                house_height = (config.bgm_score/8)*16
            else:
                house_height = 16
            pyxel.blt(13*8,13*8,0,0,24,16,house_height)

class Tree:
    def __init__(self,x,y,health = 3,make_bad_sound = True):
        self.x = x*8
        self.y = y*8
        self.tile = [0,1]
        self.tiles = [[0,1],[6,0]]
        self.tile_idx = 0
        self.depleted_tile = [0,2]
        self.health = health
        self.alive = True
        self.max_chop_timer = 2*60
        if not make_bad_sound:
            self.fail_sound = sound_lookup.none
        else:
            self.fail_sound = sound_lookup.hurt

    def start_timer(self):
        return NTimer(self.x,self.y,self.max_chop_timer,'z',sound_lookup.tree,True,self.fail_sound)

    def update(self):
        if pyxel.frame_count % 30 == 0:
            self.tile_idx += 1
            if self.tile_idx == 2:
                self.tile_idx = 0

            self.tile = self.tiles[self.tile_idx]

        if self.health <= 0 and self.alive:
            self.alive = False
            return 1
            #return NTimer(self.x+4,self.y+4,1*60,'x',sound_lookup.tree_fall)

    def draw(self):
        if self.alive:
            pyxel.blt(self.x,self.y,0,self.tile[0]*8,self.tile[1]*8,8,8,0)
        else:
            pyxel.blt(self.x,self.y,0,self.depleted_tile[0]*8,self.depleted_tile[1]*8,8,8,0)

class Mine(Tree):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tile = [6,2]
        self.tiles = [[6,2],[6,1]]
        self.depleted_tile = [6,3]
        self.health = 2
        self.offset = 16

    def start_timer(self):
        return MultiTimer([NTimer(self.x,self.y,self.max_chop_timer,'z',sound_lookup.mine),
        NTimer(self.x+8,self.y,self.max_chop_timer+self.offset,'z',sound_lookup.mine,False),
        NTimer(self.x+16,self.y,self.max_chop_timer+2*self.offset,'z',sound_lookup.mine,False)])

class BGM_Obj(Tree):
    def __init__(self):
        super().__init__(13,13)
        # blank tiles on purpose
        self.tile = [11,12]
        self.depleted_tile = [12,12]
        self.health = 4
        self.start_score = 0

    def start_timer(self):
        self.start_score = config.bgm_score
        print('start',self.start_score)
        return
    
    def update(self):
        new = config.bgm_score - self.start_score
        if new > 8 and self.alive:
            self.alive = False
            print('good music')

class App:
    def __init__(self):
        pyxel.init(16*8, 16*8 + 8, fps=60, quit_key=pyxel.KEY_NONE)
        pyxel.load('gmtk.pyxres')
        self.first_start = True
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.level = Level(0,0,16,16)
        self.ai = self.level.ai
        self.level_objs = self.level.level_objs
        self.timers = []
        self.max_health = 10
        self.player_health = 10
        self.game_over = False
        self.tree_score = 0
        self.mine_score = 0
        self.rising_text = []
        self.is_paused = False
        self.prev_menu_state = -1

        if not self.first_start:
            self.bgm = BGM(0)

    def update(self):

        # pausing messes up the music timing
        # if pyxel.btnp(pyxel.KEY_P):
        #     if self.is_paused:
        #         self.is_paused = False
        #         basic_menu.state = self.prev_menu_state
        #     else:
        #         self.is_paused = True
        #         self.prev_menu_state = basic_menu.state
        #         basic_menu.state = -2

        # if self.is_paused:
        #     return

        if self.game_over: # or self.first_start:
            basic_menu.state = -3
            #self.bgm.update(False)

            # if pyxel.btnp(pyxel.KEY_R):
            #     self.reset()
                
            pyxel.stop() # stop music
            return
            #self.bgm.mute

        new_list = []
        for val in self.timers:
            if not val.update():
                #self.rising_text.append(RisingText(4,8,"-1",8))
                self.take_damage()
            if not val.is_done:
                new_list.append(val)

        self.timers = new_list

        for obj in self.ai:
            if isinstance(obj,Ai):
                if obj.target == None or not obj.target.alive:
                    obj.target = self.get_next_tree()

            result = obj.update()
            if result is not None:
                self.timers.append(result)

        num_trees = 0
        for obj in self.level_objs:
            if isinstance(obj,Tree):
                if obj.alive:
                    num_trees += 1
            result = obj.update()
            if result is not None and not self.first_start:
                if isinstance(result,NTimer):
                    self.timers.append(result)
                    self.tree_score += 1
                else:
                    self.mine_score += 1

                self.player_health += 1
                if self.player_health > 1 and self.bgm.is_gray:
                    self.bgm.unmute_melody()

                if self.player_health > self.max_health:
                    self.player_health = self.max_health

        if num_trees == 0:
            if self.first_start:
                self.first_start = False
                self.reset()
                basic_menu.state = -1
            self.level.next_level()
            if self.level.index < 3:
                self.player_health = self.max_health
            if self.level.index == 2:
                basic_menu.state = 1
                self.bgm.toggle_gray()
            elif self.level.index == 3:
                basic_menu.state = 2
            else:
                basic_menu.state = -1
            self.ai = self.level.ai
            self.level_objs = self.level.level_objs
            self.timers = []

            if self.level.bgm_active:
                self.bgm.active = True
            else:
                self.bgm.active = False

        new_text = []
        for val in self.rising_text:
            val.update()
            if not val.done:
                new_text.append(val)

        self.rising_text = new_text

        if not self.first_start:
            if self.bgm.update(self.level.index > 2):
                self.take_damage()

    def take_damage(self):
        if not self.first_start:
            self.player_health -= 1

            if self.player_health < 3 and not self.bgm.is_gray:
                self.bgm.mute_melody()
            elif self.player_health > 3 and self.bgm.is_gray:
                self.bgm.unmute_melody()
            
            if self.player_health < 1:
                if self.level.index > 2: # past tutorial, can lose
                    self.game_over = True
                    return
                else:
                    self.player_health = 1 # don't go below 1 in tutorial


    def get_next_tree(self):
        for obj in self.level_objs:
            if isinstance(obj,Tree): # and not isinstance(obj,Mine):
                if obj.alive:
                    return obj           

    def draw(self):
        pyxel.cls(0)

        self.level.draw()

        for obj in self.level_objs:
            obj.draw()

        for obj in self.ai:
            obj.draw()

        for obj in self.timers:
            obj.draw()

        if not self.first_start:
            self.bgm.draw()

        pyxel.rect(0,pyxel.height-8,pyxel.width*(self.player_health/self.max_health),4,8)
        # tw = pyxel.width/3
        # pyxel.rectb(0,0,tw,3,1)
        # pyxel.rectb(tw,0,tw,3,1)
        # pyxel.rectb(2*tw,0,tw,3,1)


        #pyxel.text(0,pyxel.height - 8, f"T:{self.tree_score}",6)
        pyxel.text(2,pyxel.height - 6, f"Score:{self.mine_score}",6)

        for val in self.rising_text:
            val.draw()

        #if self.first_start:
        basic_menu.draw()
            #pyxel.text(10,10,"Press R To Start",2)

App()

