"""
Framework Example - Tic Tac Toe
Author - Hosung Lee (runway3207@hanmail.net)
"""

from core import *
from random import randint


def check_board(board):
    check = 0
    while check <= 1:
        i = 0
        cross_count = 0
        reversed_cross_count = 0
        while i < 3:
            j = 0
            hor_count = 0
            ver_count = 0
            while j < 3:
                if board[i][j] == check:
                    hor_count += 1
                if board[j][i] == check:
                    ver_count += 1
                j += 1
            if hor_count == 3 or ver_count == 3:
                return check

            if board[i][i] == check:
                cross_count += 1
            if board[i][2-i] == check:
                reversed_cross_count += 1
            i += 1
        if cross_count == 3 or reversed_cross_count == 3:
            return check
        check += 1
    return -1


def computer_pick_smart(board):
    check = 1
    found_spot = False
    while check >= 0:
        i = 0
        cross_count = 0
        reversed_cross_count = 0
        while i < 3:
            j = 0
            hor_count = 0
            ver_count = 0
            while j < 3:
                if board[i][j] == check:
                    ver_count += 1
                if board[j][i] == check:
                    hor_count += 1
                j += 1
            if hor_count == 2 and not found_spot:
                print "hor"
                move = 0
                while move < 3:
                    if board[move][i] == -1:
                        print "on", move, i
                        board[move][i] = 1
                        found_spot = True
                    move += 1
            if ver_count == 2 and not found_spot:
                print "ver"
                move = 0
                while move < 3:
                    if board[i][move] == -1:
                        print "on", i, move
                        board[i][move] = 1
                        found_spot = True
                    move += 1

            if board[i][i] == check:
                cross_count += 1
            if board[i][2-i] == check:
                reversed_cross_count += 1
            if cross_count == 2 and not found_spot:
                print "cross"
                move = 0
                while move < 3:
                    if board[move][move] == -1:
                        print "on", move, move
                        board[move][move] = 1
                        found_spot = True
                    move += 1
            if reversed_cross_count == 2 and not found_spot:
                print "cross"
                move = 0
                while move < 3:
                    if board[move][2-move] == -1:
                        print "on", 2-move, move
                        board[move][2-move] = 1
                        found_spot = True
                    move += 1
            i += 1
        if found_spot:
            break
        check -= 1
    return found_spot


def computer_pick_stupid(board):
    n = 0
    selection = []
    for i in board:
        for j in i:
            if j == -1:
                selection.append(n)
            n += 1
    if len(selection) > 0:
        computer_selection = selection[randint(0, len(selection)-1)]
        board[computer_selection/3][computer_selection % 3] = 1


def board_init():
    return [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]


class TicTacToe(Object):
    def init(self):
        self.board = board_init()
        self.game_over = False
        self.state = -1
        self.difficulty = 9
        self.board_x = 10
        self.board_y = 10
        self.board_w = 120
        self.board_h = 120
        self.board_surf = pygame.Surface((self.board_w*3, self.board_h*3), pygame.SRCALPHA, 32)
        self.player_win_count = 0
        self.computer_win_count = 0
        self.ox_font = pygame.font.SysFont("Arial", 120)
        self.score_font = pygame.font.SysFont("Arial", 20)
        for xx in range(2):
            draw_x = (xx + 1) * self.board_w
            pygame.draw.line(self.board_surf, BLACK, (draw_x, 0), (draw_x, self.board_h*3), 1)
        for yy in range(2):
            draw_y = (yy + 1) * self.board_h
            pygame.draw.line(self.board_surf, BLACK, (0, draw_y), (self.board_w*3, draw_y), 1)

    def update(self):
        self.difficulty = max(1,min(10,int(self.player_win_count-self.computer_win_count)/2))
        # Draw board
        surface.blit(self.board_surf, (self.board_x, self.board_y))

        # Draw O and X
        draw_set_font(self.ox_font)
        for xx in range(len(self.board)):
            for yy in range(len(self.board[xx])):
                if self.board[xx][yy] == 0:
                    draw_text(self.board_x+xx*self.board_w, self.board_y+yy*self.board_h, "O")
                if self.board[xx][yy] == 1:
                    draw_text(self.board_x+xx*self.board_w, self.board_y+yy*self.board_h, "X")

        # Check for left click
        if mouse_pressed(M_LEFT) and not self.game_over:
            # Check if mouse's position is in the board
            if self.board_x < mouse_x() < self.board_x + self.board_w * 3:
                if self.board_y < mouse_y() < self.board_y + self.board_h * 3:
                    # Get mouse's position on the board
                    mouse_sel = ((mouse_x()-self.board_x)/self.board_w, (mouse_y()-self.board_y)/self.board_h)
                    # Check if the selected position of board is empty
                    if self.board[mouse_sel[0]][mouse_sel[1]] == -1:
                        # if so, place O, which is player's
                        self.board[mouse_sel[0]][mouse_sel[1]] = 0
                        if randint(1, 10) >= 10-int(max(1,min(10,self.difficulty))):
                            # Computer picks random position and places X
                            if not computer_pick_smart(self.board):
                                if self.board[1][1] == -1:
                                    self.board[1][1] = 1
                                else:
                                    computer_pick_stupid(self.board)
                        else:
                            computer_pick_stupid(self.board)
                        # Check for winner (if there is no three-in-a-row, it returns -1)
                        winner = check_board(self.board)
                        # if winner variable is greater than -1, it checks for winner
                        if winner > -1:
                            if winner == 0:
                                # if player wins (winner is 0), increase player win count
                                self.player_win_count += 1
                                self.state = 0
                            else:
                                # if computer wins (winner is 1), increase computer win count
                                self.computer_win_count += 1
                                self.state = 1
                            # restart game by clearing board
                            self.game_over = True
        draw_set_font(self.score_font)
        draw_text(self.board_x+self.board_w*3,self.board_y, "difficulty : "+str(self.difficulty), BLUE)
        draw_text(self.board_x+self.board_w*3,self.board_y+30, "player win : "+str(self.player_win_count))
        draw_text(self.board_x+self.board_w*3,self.board_y+60, "computer win : "+str(self.computer_win_count))
        n = 0
        for i in self.board:
            for j in i:
                if j == -1:
                    n += 1
        if n == 0:
            self.game_over = True
        if self.game_over:
            if self.state == 1:
                draw_text(150,180, "X wins", RED)
            if self.state == 0:
                draw_text(150,180, "O wins", RED)
            if self.state == -1:
                draw_text(150,180, "Draws", RED)
            draw_text(100, 200, "Press R to Restart", RED)
        if keyboard_pressed(ord('r')):
            self.board = board_init()
            self.game_over = False
            self.state = -1


def game_init():
    display_resize(640, 480)
    game = instance_create(TicTacToe)
    # Game difficulty 1 ~ 10
    game.difficulty = 8

game_start(game_init)
