import pygame
import random

class Lore():
    def __init__(self, x, y, screen, enemy = False):
        self.x = x
        self.y = y
        self.screen = screen
        all_words = open('all_the_fricken_words.txt', 'r')
        word_list = all_words.readlines()

        self.lifetime = random.randint(100, random.randint(100, random.randint(100, random.randint(100, 2000))))

        self.word = random.choice(word_list)[:-1]

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        self.font = pygame.font.SysFont("monospace", 40)

        # R = amount it will divide and then multiply by to use the fact that integers are whole numbers
        #     to make it on a grid
        r = 1

        text_color = (255, 255, 255)

        if enemy:
            text_color = (255, 50, 50)

        self.text = self.font.render(self.word, True, text_color, (0, 0, 100))
        
        self.textRect = self.text.get_rect()


        ry = random.randint(self.textRect.width,  int(screen_width - self.textRect.width / 2))
        rx = random.randint(self.textRect.height, max(int(screen_height - self.textRect.height / 2), self.textRect.height))
        rx = int(rx)
        ry = int(ry)

        self.textRect.center = (ry,
                            rx
                            )


    def draw(self, screen):
        if self.lifetime > 0:

            self.screen.blit(self.text, self.textRect)
    
    def update(self):
        self.lifetime -= 1