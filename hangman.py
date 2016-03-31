from core import *

def replace_char(a_string,index,a_char):
    output = ''

    for i in range(index):
        output = output+a_string[i]

    output = output+a_char

    for i in range(index+1,len(a_string),1):
        output = output+a_string[i]

    return output

class HangMan(Object):
    def init(self):
        self.state = 0
        self.x, self.y, self.head_r, self.body_length = (570, 100, 20, 50)
        self.arm_angle, self.leg_angle = (45, 30)
        self.arm_length, self.leg_length = (30, 40)
        self.arm_pos = (int(math.cos(math.radians(90-self.arm_angle))*self.arm_length),
                        int(math.sin(math.radians(90-self.arm_angle))*self.arm_length))
        self.leg_pos = (int(math.cos(math.radians(90-self.leg_angle))*self.leg_length),
                        int(math.sin(math.radians(90-self.leg_angle))*self.leg_length))
        self.rope_length, self.hanger_dist, self.hanger_length = (20, 40, 200)
        self.ground_length = 80
        self.ground_pos = (self.x+20, self.y-self.head_r+self.hanger_length)

    def update(self):
        # Draw Hanger
        pygame.draw.lines(surface, BLACK, False, [(self.x, self.y-self.head_r),
                                                  (self.x, self.y-self.head_r-self.rope_length),
                                                  (self.x+self.hanger_dist, self.y-self.head_r-self.rope_length),
                                                  (self.x+self.hanger_dist, self.y-self.head_r+self.hanger_length)], 2)

        pygame.draw.lines(surface, BLACK, False, [(self.ground_pos[0]-self.ground_length/2, self.ground_pos[1]),
                                                  (self.ground_pos[0]+self.ground_length/2, self.ground_pos[1])], 2)

        # Draw Head
        if self.state > 0:
            pygame.draw.circle(surface, BLACK, (self.x, self.y), self.head_r, 2)

        # Draw Body
        if self.state > 1:
            pygame.draw.lines(surface, BLACK, False, [(self.x, self.y+self.head_r),(self.x, self.y+self.head_r+self.body_length)], 2)

        # Draw Left Arm
        if self.state > 2:
            pygame.draw.lines(surface, BLACK, False, [(self.x, self.y+self.head_r),(self.x-self.arm_pos[0], self.y+self.head_r+self.arm_pos[1])], 2)

        # Draw Right Arm
        if self.state > 3:
            pygame.draw.lines(surface, BLACK, False, [(self.x, self.y+self.head_r),(self.x+self.arm_pos[0], self.y+self.head_r+self.arm_pos[1])], 2)

        # Draw Left Leg
        if self.state > 4:
            pygame.draw.lines(surface, BLACK, False, [(self.x, self.y+self.head_r+self.body_length),(self.x-self.leg_pos[0], self.y+self.head_r+self.body_length+self.leg_pos[1])], 2)

        # Draw Right Leg
        if self.state > 5:
            pygame.draw.lines(surface, BLACK, False, [(self.x, self.y+self.head_r+self.body_length),(self.x+self.leg_pos[0], self.y+self.head_r+self.body_length+self.leg_pos[1])], 2)


class UI(Object):
    def init(self):
        self.word = "KimJungIl".upper()
        self.alpha = [chr(i) for i in range(65, 91)]
        self.word_bank_pos = (50, 300)
        self.word_font = pygame.font.SysFont("Arial", 30)
        self.word_size = 40
        self.word_blank = ""
        self.man = None
        self.blank_pos = (20,200)
        for i in range(len(self.word)):
            if self.word[i] == ' ':
                self.word_blank += ' '
            else:
                self.word_blank += '_'
        draw_set_font(self.word_font)

    def update(self):
        # Draw letters
        for i in range(len(self.alpha)):
            draw_text(self.word_bank_pos[0]+(i % 10)*self.word_size, self.word_bank_pos[1]+(i/10)*self.word_size, self.alpha[i])

        # Draw Blanks
        draw_text(self.blank_pos[0], self.blank_pos[1], ' '.join(self.word_blank))

        # Check for mouse left button
        if mouse_pressed(M_LEFT):
            if self.word_bank_pos[0] <= mouse_x() <= self.word_bank_pos[0] + self.word_size*10 and \
                                    self.word_bank_pos[1] <= mouse_y() <= self.word_bank_pos[1] + self.word_size*3:
                xi, yi = ((mouse_x()-self.word_bank_pos[0])/self.word_size, (mouse_y()-self.word_bank_pos[1])/self.word_size)
                if 0 <= xi+yi*10 <= 25:
                    right = False
                    for i in range(len(self.word)):
                        if self.word[i] == self.alpha[xi+yi*10]:
                            self.word_blank =  replace_char(self.word_blank, i, self.alpha[xi+yi*10])
                            right = True
                    if not right:
                        self.man.state += 1



def game_init():
    display_resize(640, 480)
    man = instance_create(HangMan)
    game_ui = instance_create(UI)
    game_ui.man = man
    # Game difficulty 1 ~ 10

game_start(game_init)
