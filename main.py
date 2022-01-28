import pygame as pg
import sys
from pygame.locals import *

# LEFT OFF AT VIDEO 3: 14:58, tile physics/collisions

# The basic window stuff
pg.init()
clock = pg.time.Clock()
pg.display.set_caption('Dafluffy Potato Series')
WINDOW_SIZE = (600, 400)
screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)

# We are drawing things to this display surface (which is an image btw)
# And then scaling up the display to the screen size
# This is so we can scale up our pixel art, which is really small
display = pg.Surface((300, 200))

# Images
player_image_temp = pg.image.load('player.png').convert_alpha()
player_image = pg.transform.scale(player_image_temp, (25, 25))
player_image.set_colorkey((255, 255, 255))
grass_image =pg.image.load('grass_block.png').convert_alpha()
dirt_image = pg.image.load('dirt_block.png').convert_alpha()

# Player info
moving_right = False
moving_left = False
player_location = [0, 50]
player_y_momentum = 0
player_rect = pg.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height())

# World Objects
TILE_SIZE = dirt_image.get_width() # Should be 16

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]


# Game loop
while True:
    # Event Loop
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                moving_right = True
            if event.key == pg.K_LEFT:
                moving_left = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                moving_right = False
            if event.key == pg.K_LEFT:
                moving_left = False


    # Updates
    player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if moving_right:
        player_location[0] += 4
    if moving_left:
        player_location[0] -= 4

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]


    # Drawing
    display.fill((146, 244, 255))

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))

            # Any tile that's not air, gets tracked as a rect for collisions
            if tile != '0':
                tile_rects.append(pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    display.blit(player_image, player_location)  # puts one surface onto another surface


    screen.blit(pg.transform.scale(display, WINDOW_SIZE), (0, 0))
    pg.display.update()
    clock.tick(60)
