import pygame
import math
import numpy as np
import pygame
import random

def ball_ball_collision(ball1, ball2):
    if ball1 == ball2:
        return False
    r1 = ball1.rect.width/2
    r2 = ball2.rect.width/2

    x1, y1 = ball1.rect.center
    x2, y2 = ball2.rect.center

    if math.sqrt((x2 - x1)**2 + (y2 - y1)**2) < r1 + r2:
        return True
    return False

def elastic_collision(ball1, ball2, damping = 0.95):
    m1 = ball1.mass
    m2 = ball2.mass
    v1 = np.array(ball1.v)
    v2 = np.array(ball2.v)
    x1 = np.array(ball1.rect.center)
    x2 = np.array(ball2.rect.center)

    u1 = ((m1-m2)/(m1+m2)) * v1 + ((2 * m2)/(m1+m2)) * v2
    u2 = ((2 * m1)/(m1+m2)) * v1 + ((m2-m1)/(m1+m2)) * v2


    nv = pygame.Vector2(ball2.rect.center) - pygame.Vector2(ball1.rect.center)

    


    u1 = v1 - ((2 * m2)/(m1+m2)) * (np.dot(v1 - v2, x1 - x2)/np.dot(x1 - x2, x1 - x2)) * (x1 - x2)
    u2 = v2 - ((2 * m1)/(m1+m2)) * (np.dot(v2 - v1, x2 - x1)/np.dot(x2 - x1, x2 - x1)) * (x2 - x1)

    r1 = ball1.radius
    r2 = ball2.radius

    dist = r1 + r2 - np.linalg.norm(x1 - x2)
    direction = (x1 - x2)/np.linalg.norm(x1 - x2)
    v1_in_dir = np.dot(v1, direction)
    v2_in_dir = np.dot(v2, direction)

    ball1.rect.center = x1 + direction * dist * abs(v1_in_dir)/(abs(v1_in_dir) + abs(v2_in_dir))
    ball2.rect.center = x2 - direction * dist * abs(v2_in_dir)/(abs(v1_in_dir) + abs(v2_in_dir))


    #ball1.debug_vector = u1
    #ball2.debug_vector = u2

    ball1.v = u1 * damping
    ball2.v = u2 * damping


def inelastic_collision(ball1, ball2):
    pass

def mixed_collision(ball1, ball2, cr=0.5):
    pass


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, world, pos=(0, 0), v=(0,0)):
        self.tag = ""
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image = pygame.surface.Surface((2*radius, 2*radius))
        self.image.fill((0, 0, 0))
        if random.randint(0, 100) < 10:
            random_bright = (255, 76, 54)
            random_tint = (random.randint(-20,20), random.randint(-20,20), random.randint(-20,20))
            color = [min(random_bright[0] + random_tint[0], 255), min(random_bright[1] + random_tint[1], 255), min(random_bright[2] + random_tint[2], 255)]

            self.tag = "enemy"
            
        pygame.draw.ellipse(self.image, color, self.image.get_rect())
        pygame.draw.ellipse(self.image, (255, 255, 255), self.image.get_rect(), 1)
        self.image.set_colorkey((0,0,0))

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.v = np.array(v)
        self.mass = math.pi*radius*radius

        self.world = world

        self.debug_vector = [0, 0]



        

    def draw_debug(self):
        pygame.draw.line(self.world.screen, (0, 255, 0), (self.rect.center[0], self.rect.center[1]), 
        (self.rect.x + self.debug_vector[0] * 3, self.rect.y + self.debug_vector[1] * 3), 2)

    def update(self, bounds):


        self.rect.x += self.v[0]
        self.rect.y += self.v[1]

        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            self.v[0] *= -1
        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            self.v[1] *= -1
        if self.rect.right > bounds.right:
            self.rect.right = bounds.right
            self.v[0] *= -1
        if self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self.v[1] *= -1

        if self.world.gravitating:
            x1 = np.array(self.rect.center, dtype=np.dtype('float64'))
            x2 = np.array(pygame.mouse.get_pos(), dtype=np.dtype('float64'))    
            dif = (x2 - x1)
            dif_n = (dif) / np.dot(dif, dif)
            v = np.array(self.v, dtype=np.dtype('float64'))
            self.v = self.v + dif_n * 10
            self.debug_vector = dif_n
        if (self.tag == 'enemy'):
            if (random.randint(0, 5000) <= 4):
                self.world.add_bomb(self.rect.center, True)
                self.kill()
                del self
        #self.draw_debug()