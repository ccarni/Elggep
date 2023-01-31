from locale import normalize
import pygame
import math
import numpy as np
import pygame
import random
import ball
from player_ball import Player_Ball

class Launcher():
    def __init__(self, x, y, world):
        self.world = world
        self.x = x
        self.y = y
        self.pos = np.array([self.x, self.y], dtype=np.dtype('float64'))
        self.angle = np.array([0, -10], dtype=np.dtype('float64'))

    def draw(self, screen):
        # Draw
        #print(self.angle[0], self.angle[1])
        pygame.draw.aaline(screen, (255, 0, 0), (self.x, self.y), 
        (self.x + self.angle[0], self.y + self.angle[1]), 3)

    def normalize(self, v):
        n =  v / np.sqrt(np.sum(v**2))
        return n

    def update(self):
        self.pos
        x1 = np.array(self.pos, dtype=np.dtype('float64'))
        x2 = np.array(pygame.mouse.get_pos(), dtype=np.dtype('float64'))    
        dif = (x2 - x1)
        dif_n = self.normalize(dif)
        self.angle = dif_n * 30


    def move(self, dir):
        # Move Aimy boi
        self.x += dir[0]
        self.y += dir[1]


    def shoot(self, color, radius):
        self.world.add_player_ball(color, radius, self.pos + self.angle, self.angle)