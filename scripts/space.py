import pygame
import random

class Space(pygame.sprite.Sprite):
    def __init__(self,display):
        super().__init__()
        self.image = pygame.Surface((random.randint(1,3),random.randint(1,3))).convert_alpha()
        self.image.fill("white")
        self.display = display
        self.pos_x = random.randint(self.display.get_width()//2 - 100, self.display.get_width()//2 + 100)
        self.pos_y = random.randint(self.display.get_height()//2 - 100, self.display.get_height()//2 + 100)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x,self.pos_y]
        self.horizontal_speed = random.uniform(-2,2)
        self.vertical_speed = random.uniform(-1,1)

    def update(self):        
        self.pos_x += self.horizontal_speed
        self.pos_y += self.vertical_speed
        if self.pos_x <= 0 or self.pos_x >= self.display.get_width():
            self.kill()
        if self.pos_y <= 0 or self.pos_y >= self.display.get_height():
            self.kill()

        self.rect.topleft = [self.pos_x,self.pos_y]




