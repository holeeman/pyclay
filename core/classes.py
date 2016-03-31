from constants import *
import os, json


class Object(object):
    # Object class

    def __init__(self, x=0, y=0):
        super(Object, self).__init__()
        self.x = x
        self.y = y

    def init(self):
        pass

    def update(self):
        pass


class Sprite(object):
    # Sprite class

    def __init__(self, file_name, width=0, height=0, alpha=True):
        if alpha:
            self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
        else:
            self.sprite_sheet = pygame.image.load(file_name).convert()
        self.sprite = []
        self.file_name = file_name
        self.sheet_width = self.sprite_sheet.get_size()[0]
        self.sheet_height = self.sprite_sheet.get_size()[1]
        self.image_count = 0
        if width == 0 or height == 0:
            width = self.sheet_width
            height = self.sheet_height
        self.image_width = width
        self.image_height = height
        for yy in range(self.sheet_height/height):
            for xx in range(self.sheet_width/width):
                image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                image.blit(self.sprite_sheet, (0, 0), (xx*width, yy*height, width, height))
                self.sprite.append(image)
                self.image_count += 1

    def get_image(self, index=0):
        try:
            return self.sprite[index]
        except:
            return self.sprite[0]