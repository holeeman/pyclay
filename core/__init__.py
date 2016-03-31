from constants import *
from classes import *
import math

# Setting
pygame.init()

screenResolution = (640, 480)
gameCaption = "pyclay"
gameFont = pygame.font.SysFont("Arial", 12)
gameBackgroundColor = WHITE
FPS = 60

pygame.display.set_caption(gameCaption)
surface = pygame.display.set_mode(screenResolution)
clock = pygame.time.Clock()
keyboardPrev = []
keyboardInput = []
mousePrev = ()
mouseInput = ()
instanceList = []


def game_end():
    # Game End
    pygame.quit()
    quit()


# --- Useful Function ---


def draw_set_font(font):
    global gameFont
    gameFont = font


def draw_text(x, y, text="", color=BLACK):
    # Draws text
    _txt = gameFont.render(text, True, color)
    surface.blit(_txt, (x, y))


def draw_sprite(x, y, sprite, index=0):
    surface.blit(sprite.get_image(index), (x, y))


def display_get_width():
    # Get width of display
    return screenResolution[0]


def display_get_height():
    # Get height of display
    return screenResolution[1]


def display_resize(width, height):
    # Reset the size of display
    global screenResolution
    global surface
    screenResolution = (width, height)
    surface = pygame.display.set_mode(screenResolution)


def display_set_screen(state):
    global surface
    if state:
        surface = pygame.display.set_mode(screenResolution, pygame.FULLSCREEN)
    else:
        surface = pygame.display.set_mode(screenResolution)


def display_set_background_color(color):
    global gameBackgroundColor
    gameBackgroundColor = color


def keyboard_button(key):
    # Check if a keyboard button is on hold
    try:
        if keyboardInput[key]:
            return True
        return False
    except:
        return False


def keyboard_released(key):
    # Check if a keyboard button is released
    try:
        if keyboardPrev[key] and not keyboardInput[key]:
            return True
        return False
    except:
        return False


def keyboard_pressed(key):
    # Check if a keyboard button is pressed
    try:
        if not keyboardPrev[key] and keyboardInput[key]:
            return True
        return False
    except:
        return False


def mouse_button(key):
    # Check if a mouse button is on hold
    try:
        if mouseInput[key]:
            return True
        return False
    except:
        return False


def mouse_released(key):
    # Check if a mouse button is released
    try:
        if mousePrev[key] and not mouseInput[key]:
            return True
        return False
    except:
        return False


def mouse_pressed(key):
    # Check if a mouse button is pressed
    try:
        if not mousePrev[key] and mouseInput[key]:
            return True
        return False
    except:
        return False


def mouse_x():
    # Get x position of mouse
    pos = pygame.mouse.get_pos()
    return pos[0]


def mouse_y():
    # Get y position of mouse
    pos = pygame.mouse.get_pos()
    return pos[1]


def instance_create(obj, x=0, y=0):
    # Create an instance of an Object
    ins = obj(x, y)
    ins.init()
    instanceList.append(ins)
    return ins


def point_distance(x1, y1, x2, y2):
    # Return distance between to points
    return math.sqrt(pow(x2-x1,2) + pow(y2-y1,2))


def point_direction(x1, y1, x2, y2, in_degree=True):
    # Return direction from one point to another
    if in_degree:
        return math.atan2((y2-y1), (x2-x1))*(math.pi/180)
    else:
        return math.atan2((y2-y1), (x2-x1))


def collision_rectangle(box1, box2):
    b1 = list(box1)
    b2 = list(box2)
    if b1[2] < 0:
        b1[0] += b1[2]
        b1[2] *= -1
    if b2[2] < 0:
        b2[0] += b2[2]
        b2[2] *= -1
    # Rectangular collision check
    if b2[0] > b1[0] + b1[2]:
        return False
    if b1[0] > b2[0] + b2[2]:
        return False
    if b1[1] > b2[1] + b2[3]:
        return False
    if b2[1] > b1[1] + b1[3]:
        return False
    return True


# game_control


def game_start(game_init=None):
    # Start game

    if game_init is not None:
        game_init()
    while True:
        # Background
        surface.fill(gameBackgroundColor)

        # Get Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end()
            global keyboardInput, mouseInput
            keyboardInput = pygame.key.get_pressed()
            mouseInput = pygame.mouse.get_pressed()

        # Go through instances
        for instance in instanceList:
            # Executes codes in update
            instance.update()

        global keyboardPrev, mousePrev
        keyboardPrev = keyboardInput
        mousePrev = mouseInput
        pygame.display.update()
        clock.tick(FPS)