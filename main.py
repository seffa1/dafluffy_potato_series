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
grass_image = pg.image.load('grass_block.png').convert_alpha()
dirt_image = pg.image.load('dirt_block.png').convert_alpha()

# Player info
moving_right = False
moving_left = False
player_y_momentum = 0
air_timer = 0
player_rect = pg.Rect(50, 50, player_image.get_width(), player_image.get_height())

# Camera Scroll
true_scroll = [0, 0]  # The float scroll
scroll = [0, 0]  # The int scroll, for tile movements, to prevent them from being choppy

# World Objects
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
TILE_SIZE = dirt_image.get_width()  # Should be 16
def load_map(path):
    with open(path + '.txt', 'r') as file:
        data = file.read()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map
game_map = load_map('map')


def collision_test(rect: Rect, tiles: list):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}

    # Move on the x axis
    rect.x += movement[0]
    # Check for collisions
    hit_list = collision_test(rect, tiles)
    # Update position based on collisions
    for tile in hit_list:
        # If you are moving right
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        # If you are moving left
        if movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    # Update the y axis position
    rect.y += movement[1]
    # Check for collisions
    hit_list = collision_test(rect, tiles)
    # Update positions
    for tile in hit_list:
        # If you are moving down
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        # If you are moving up
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


# Game loop
while True:
    # Sets the "cameras" position. The divisor adds the lagging behind, smoothing effect
    true_scroll[0] += (player_rect.x - true_scroll[0] - 140)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 80)/20
    scroll = true_scroll.copy()
    # Rounds the float to an int for the drawings not to get choppy
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])



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
            if event.key == pg.K_UP:
                # You can jump if you have been in the air for less than 6 frames
                # Allows you to jump if you just stepped off a ledge, which is nice
                # And also prevents you from jumping more tha once at a time
                if air_timer < 6:
                    player_y_momentum = - 5

        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                moving_right = False
            if event.key == pg.K_LEFT:
                moving_left = False

    # Draw background fill color
    display.fill((146, 244, 255))
    # Draw background object 1
    pg.draw.rect(display, (5, 80, 75), pg.Rect(0, 150, 200, 100))
    # Draw the parallax background objects
    for background_object in background_objects:
        obj_rect = pg.Rect(background_object[1][0]-scroll[0]*background_object[0],
                           background_object[1][1]-scroll[1]*background_object[0],
                           background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pg.draw.rect(display, (14, 222, 150), obj_rect)
        else:
            pg.draw.rect(display, (9, 91, 85), obj_rect)




        # background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]],
        #                       [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]
    # Draw tiles from the game map
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

            # Any tile that's not air, gets tracked as a rect for collisions
            if tile != '0':
                tile_rects.append(pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    # Updates for the player

    # Calc the amount we intend to move the player from user inputs
    # X axis
    player_movement = [0, 0]
    # The amount we intend to move the player on the x-axis
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    # Y axis
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    # Sets a max velocity to fall
    if player_y_momentum > 8:
        player_y_momentum = 8

    # I dont like how this update has to happened after the drawings of the background
    # Update the players location
    # Check for collisions and set the actual position of the player
    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    # Normally, if we set the player's y momentum to 0, then the next update of 0.2 gravity momentum would not
    # Increase the momentum enough to move the player 1 pixel (you need at least .6 to round up), so we wouldn't be registering collisions until the momentum
    # Reached 1, and then reset it. This is why our balls were shaking up and down in the ball game. To fix this make the
    # y_momentum = 1 if theres a bottom collision. The air timer lets us fall slightly off ledges and still get a jump in.
    if collisions['bottom']:
        # print('bottom')
        player_y_momentum = 1
        air_timer = 0
    else:
        # print('NOT')
        air_timer += 1
    if collisions['top']:
        player_y_momentum = 0

    # Draw the player
    display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))  # puts one surface onto another surface

    # Scale the display up to the screen size, and draw it onto the screen
    screen.blit(pg.transform.scale(display, WINDOW_SIZE), (0, 0))
    pg.display.update()
    clock.tick(60)
