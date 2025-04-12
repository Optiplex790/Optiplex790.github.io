import random
from display import *

class Carrot():
    def __init__(self,position, force = (0,0), delay = 0):
        #Handle image info
        scale = random.uniform(1.3, 1.6)

        #Bunny itself
        self.image_list = []
        for i in range(len(carrot_img_list)):
            self.image_list.append(pygame.transform.scale_by(carrot_img_list[i], scale))

        #Handle rect info
        self.rect = self.image_list[0].get_frect()
        self.rect.scale_by(0.6, 0.6)
        self.rect.x = position[0]
        self.rect.y = position[1]

        #Handle other variables
        self.delay = delay
        self.xaccel = force[0]
        self.yaccel = force[1]
        self.caught = 0
        self.time = pygame.time.get_ticks()
        self.lasty = 0

    def update(self):
        if self.delay != 0:
            self.delay -= 1
        else:
            #Physics
            self.yaccel += 0.3
            self.xaccel *= 0.995
            self.yaccel *= 0.995

            self.rect.x += self.xaccel
            self.rect.y += self.yaccel

            #Caught Animation
            if 0 < self.caught <= 18:
                self.caught += 1

            #Caught bounce off walls
            if self.rect.x+40 >= screen_width -21 or self.rect.x+10 <= 21:
                self.xaccel *= -0.9

            #print(f"{self.rect.x}, {self.rect.y}")

            self.lasty = self.rect.y


    def hit(self):
        if self.caught == 0:
            self.xaccel = random.randint(-4,4)
            self.yaccel = -10
            self.caught = 1
            return 1
        else:
            return 0

    def draw(self, screen):
        screen.blit(self.image_list[math.floor(self.caught/3)], (self.rect.x, self.rect.y))