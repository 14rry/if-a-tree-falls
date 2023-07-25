import pyxel

state = 0


def draw():
    text = []
    if state == 0:
        text = ['If a tree falls and',
         'no one is there,',
         'does it make a sound?',
         '',
         "Press 'z' when circle", 
         'closes to find out.']
    elif state == 1:
        text = ["Build the DJ booth!",
         'Press the up arrow', 
         'on the beat.']
    elif state == 2:
        text = ["Nice!",
         'All together now.']
    elif state == -2:
        text = ["Paused.",
         'Press P to continue.']
    elif state == -3:
        text = ["Game over.",
         'Thanks for playing!',
         'Feel free to refresh',
         'the page to try again.',
         '(Reset is still WIP).']

    for idx,val in enumerate(text):
        pyxel.rect(15,18+idx*10,pyxel.width-30,8,7)
        pyxel.text(16,20+idx*10,val,0)
        pyxel.rect(15,18+idx*10+8,pyxel.width-30,2,8)

        
