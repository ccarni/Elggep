import pygame
import random
import sys
import ball
import player_ball
from launcher import Launcher
import numpy as np
import lore
from bomb import Bomb

#SCREW HOOKE AND HIS DUMB LAWSSSS
# - JAREN k,.l./l/.;/: speaking for all members of the Elggep™ division of PWNED™ Games™ 

pygame.init()


class World():
    def __init__(self, screen):
        self.screen = screen
        self.grav = [0, 0]
        self.gravitating = False

        self.gravity = 1

        self.words = []

        self.player_exists = False

        self.score = 0

        self.getTicksLastFrame = 0

        self.max_ball_counter = 200
        self.ball_counter = 100

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.launcher = Launcher(screen.get_width()/2, screen.get_height() - 20, self)

        self.balls = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.playerball = pygame.sprite.Group()
        for i in range(10):
            # Color that goes with puce
            puce_good = [150, 217, 159]
            self.add_random_ball(puce_good)

    # Add a ball
    def add_ball(self, color, radius, position, velocity):
        b = ball.Ball(color, radius, self, position, velocity)
        self.balls.add(b)
        
    # Add a player ball
    def add_player_ball(self, color, radius, position, velocity):
        b = player_ball.Player_Ball(color, radius, self, position, velocity)
        self.playerball.add(b) 
        self.player_exists = True

    def add_bomb(self, position, enemy = False):
        b = Bomb((255, 237, 97), random.randint(30,60), self, position)
        if enemy:
            b = Bomb((237, 88, 69), random.randint(40,80), self, position)
        self.bombs.add(b)


    def add_random_ball(self, col = [150, 217, 159]):
        color = [random.randint(0, 255) for j in range(3)]
        
        random_bright = random.randint(50, 200)
        random_bright = col
        random_tint = (random.randint(-20,20), random.randint(-20,20), random.randint(-20,20))
        color = [random_bright[0] + random_tint[0], random_bright[1] + random_tint[1], random_bright[2] + random_tint[2]]
        radius = random.randint(10, 20)
        position = [random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height())]
        velocity = [random.randint(-2, 2) for j in range(2)]
        self.add_ball(color, radius, position, velocity)
    
    # ... it draws stuff
    # yeah
    def draw(self):
        self.screen.fill(background_color)
        self.creature()
        self.creature2()
        self.launcher.draw(self.screen)
        self.balls.draw(self.screen)
        self.bombs.draw(self.screen)
        if self.player_exists:
            self.playerball.draw(self.screen)

        screen_width = screen.get_width()

        font = pygame.font.SysFont("monospace", 40)

        text = font.render("Score is: " + str(self.score), True, (0, 255, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (screen_width - textRect.width / 2 - 10, 30)
        self.screen.blit(text, textRect)

        for i in self.words:
            i.draw(self.screen)

    # It's an update funciton. it updates tstuff
    def update(self):
        
        self.t = self.clock.tick(self.FPS)


        if self.ball_counter > 0:
            self.ball_counter -= 1
        else:
            self.ball_counter = random.randint(30, self.max_ball_counter)
            for i in range(1):
                # Color that goes with puce
                puce_good = [150, 217, 159]
                self.add_random_ball(puce_good)

        

        for i in self.words:
            i.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.player_exists:
                        col1 = [126, 143, 204]
                        col2 = (random.randint(-20,20), random.randint(-20,20), random.randint(-20,20))
                        color = [col1[0] + col2[0], col1[1] + col2[1], col1[2] + col2[2]]
                        self.launcher.shoot(color, 10 + random.randint(-3,8))
                        self.player_exists
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.gravitating = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        keys = pygame.key.get_pressed()

        self.launcher.update()
        self.bombs.update()
        for i in self.bombs:
            i.bomb_update()

        if keys[pygame.K_l]:
            self.score += 1

        if keys[pygame.K_RIGHT]:
            self.launcher.move(np.array([1, 0]))
        if keys[pygame.K_LEFT]:
            self.launcher.move(np.array([-1, 0]))

        self.balls.update(bounds=self.screen.get_rect())
        self.playerball.update(bounds=self.screen.get_rect())


        collided = pygame.sprite.groupcollide(self.balls, self.balls, False, False, ball.ball_ball_collision)
        collided_player = pygame.sprite.groupcollide(self.balls, self.playerball, False, False, ball.ball_ball_collision)


        for collide1 in collided.keys():
            for collide2 in collided[collide1]:
                ball.elastic_collision(collide1, collide2)
                    
                #ball.inelastic_collision(collide1, collide2)
                #ball.mixed_collision(collide1, collide2, 0.9)
                collided[collide2].remove(collide1)


        for collide1 in collided_player.keys():
            for collide2 in collided_player[collide1]:
                ball.elastic_collision(collide1, collide2)

                    
                #ball.inelastic_collision(collide1, collide2)
                #ball.mixed_collision(collide1, collide2, 0.9)
                if collide2.tag == "player":
                    
                    
                    self.player_exists = False
                    self.playerball.remove(collide2)
                    if collide1.tag == "enemy":
                        newlore = lore.Lore(0, 0, self.screen, True)
                        self.words.append(newlore)
                        self.add_bomb(collide2.rect.center, True)
                        self.score -= 8
                    else:
                        newlore = lore.Lore(0, 0, self.screen)
                        self.words.append(newlore)
                        
                        self.add_bomb(collide2.rect.center, False)
                        self.score += 1
                    self.balls.remove(collide1)
                    
                
                


        pygame.display.update()


    def creature(self):
        hue = (255, 255, 255)
        #pygame.draw.rect(screen, (1, 1, 1), pygame.Rect(340, 140, 320, 320), border_radius=50, width=20)
        #pygame.draw.rect(screen, (1, 1, 1), pygame.Rect(390, 390, 70, 520), border_radius=50, width=20)
        #pygame.draw.rect(screen, (1, 1, 1), pygame.Rect(540, 390, 70, 520), border_radius=50, width=20)
        pygame.draw.rect(self.screen, (hue), pygame.Rect(50, 150, 300, 300), border_radius=50)
        pygame.draw.rect(self.screen, (hue), pygame.Rect(100, 400, 50, 500), border_radius=50)
        pygame.draw.rect(self.screen, (hue), pygame.Rect(250, 400, 50, 500), border_radius=50)
        pygame.draw.circle(self.screen, (0, 0, 0), (100, 200), 20)
        pygame.draw.circle(self.screen, (0, 0, 0), (300, 200), 20)
        pygame.draw.line(self.screen, (0, 0, 0),(100, 250), (300, 250))
        
    def creature2(self):
        hue = (255, 255, 255)
        #pygame.draw.rect(self.screen, (1, 1, 1), pygame.Rect(340, 140, 320, 320), border_radius=50, width=20)
        #pygame.draw.rect(self.screen, (1, 1, 1), pygame.Rect(390, 390, 70, 520), border_radius=50, width=20)
        #pygame.draw.rect(self.screen, (1, 1, 1), pygame.Rect(540, 390, 70, 520), border_radius=50, width=20)
        pygame.draw.rect(self.screen, (hue), pygame.Rect(850, 150, 300, 300), border_radius=50)
        pygame.draw.rect(self.screen, (hue), pygame.Rect(900, 400, 50, 500), border_radius=50)
        pygame.draw.rect(self.screen, (hue), pygame.Rect(1050, 400, 50, 500), border_radius=50)
        pygame.draw.circle(self.screen, (0, 0, 0), (900, 200), 20)
        pygame.draw.circle(self.screen, (0, 0, 0), (1100, 200), 20)
        pygame.draw.line(self.screen, (0, 0, 0),(900, 250), (1100, 250))



screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

world = World(screen)
background_color = (204, 136, 153)





while True:
    world.update()
    world.draw()