from core import *


class Paint(Object):
    def init(self):
        self.draw_list = []
        self.drawing = False
        self.current_pt = None
        self.draw_size = 1
        self.draw_color = BLACK
        self.drawing_board = pygame.Surface((display_get_width(), display_get_height()))
        self.drawing_board.fill(WHITE)

    def update(self):

        #drawing
        surface.blit(self.drawing_board, (0, 0))

        if mouse_released(M_LEFT):
            self.drawing = False

        if mouse_pressed(M_LEFT):
            self.drawing = True
            self.current_pt = None

        if self.drawing is True:
            point = instance_create(Point, mouse_x(), mouse_y())
            point.p1 = self.current_pt
            point.p2 = point
            point.size = self.draw_size
            point.color = self.draw_color
            point.surface = self.drawing_board
            point.draw_on_surface()
            self.current_pt = point

        if keyboard_pressed(K_UP):
            self.draw_size += 5
        if keyboard_pressed(K_DOWN):
            self.draw_size -= 5
        if keyboard_pressed(K_RETURN):
            print self.draw_list
            print sum([len(x) for x in self.draw_list])
            self.draw_list = []


class Point(Object):
    def init(self):
        self.size = 1
        self.color = BLACK
        self.p1 = None
        self.p2 = None
        self.surface = None
        pass

    def draw_on_surface(self):
        p2_pos = (self.p2.x, self.p2.y)
        pygame.draw.circle(self.surface, self.color, p2_pos, max(0, self.size/2 - 1))

        if self.p1 != None:
            p1_pos = (self.p1.x, self.p1.y)
            pygame.draw.line(self.surface, self.color, p1_pos, p2_pos, self.size)


class Fill(Object):
    def init(self):
        pass

    def update(self):
        pass

def game_init():
    instance_create(Paint)

game_start(game_init)
