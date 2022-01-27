import pygame as pg
import sys
from pygame.locals import *

# LEFT OFF AT VIDEO 2

# The basic window stuff
pg.init()
clock = pg.time.Clock()
pg.display.set_caption('Dafluffy Potato Series')
WINDOW_SIZE = (400, 400)
screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)


# Game loop
while True:

    # Event Loop
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        pg.display.update()
        clock.tick(60)