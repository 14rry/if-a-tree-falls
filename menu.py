from enum import Enum
import pyxel

class MenuState(Enum):
    CLOSED = 0
    INTRO = 1
    SETTINGS = 2

class Menu():
    def __init__(self):
        self.menu_state = MenuState.CLOSED
        self.intro_menu_text = ['If a tree falls.. will you hear it?']
        self.settings_menu_text = ['Settings','Music','SFX']

        self.padding = 12
        self.col1 = 3
        self.col2 = 11

        self.cursor_pos = 0
        self.max_cursor_pos = 0

    def update(self):
        # if config.input.btnp('menu'):
        #     global menu_state
        #     if menu_state == MenuState.SETTINGS:
        #         menu_state = MenuState.CLOSED
        #     else:
        #         menu_state = MenuState.SETTINGS

        if self.menu_state != MenuState.CLOSED:
            dir = self.get_directional_input_btnp()

            if dir[1] == 1:
                self.cursor_pos = min(self.cursor_pos+1,self.max_cursor_pos)
            elif dir[1] == -1:
                self.cursor_pos = max(self.cursor_pos-1,0)

            self.update_menu_x(dir[0])

        return menu_state == MenuState.CLOSED

    def update_menu_x(self):

        if self.menu_state == MenuState.INTRO:
            self.current_str = self.intro_menu_text[cursor_pos+1]

            



    def draw():
        if menu_state == MenuState.SETTINGS:
            pyxel.rect(10,10,100,100,col1)
            draw_menu_text(settings_menu_text,cursor_pos)

    def draw_menu_text(txt_str,cursor_pos):

        global max_cursor_pos
        max_cursor_pos = len(txt_str)-2

        x = padding
        y = padding
        for val in txt_str:

            if y//padding == cursor_pos + 2:
                pyxel.text(x-padding/2,y,'>',col2)

            if menu_state == MenuState.SETTINGS and x > padding:
                val = append_sound_levels(val)

            pyxel.text(x,y,val,col2)

            if x == padding:
                x += padding

            y += padding







