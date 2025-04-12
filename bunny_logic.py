import random
from display import *

#Break apart sprite sheet into different frames in a list
bunny_jump_frames = []
bunny_hit_frames = []
bunny_parts = []

for i in range(9):
    bunny_jump_frames.append(pygame.surface.Surface((70,70), flags=pygame.SRCALPHA))
    bunny_jump_frames[i].blit(bunny_spritesheet, (-i*70,0))
for i in range(18):
    bunny_hit_frames.append(pygame.surface.Surface((70, 70), flags=pygame.SRCALPHA))
    bunny_hit_frames[i].blit(bunny_hit_spritesheet, (-i * 70, 0))
for i in range(3):
    bunny_parts.append(pygame.surface.Surface((70, 70), flags=pygame.SRCALPHA))
    bunny_parts[i].blit(bunny_spritesheet, (-i * 70, 0))

class Bunny():
    def __init__(self,position, force = (0,0), delay = 0):
        #Handle image info
        scale = 1

        #Bunny itself
        self.head_img = bunny_parts[0]
        self.body_img = bunny_parts[1]
        self.tail_img = bunny_parts[2]
        self.head_img = pygame.transform.scale_by(self.head_img,scale)
        self.body_img = pygame.transform.scale_by(self.body_img, scale)
        self.tail_img = pygame.transform.scale_by(self.tail_img, scale)


        #Hit animation
        self.hit_frames = bunny_hit_frames
        for i in range(len(self.hit_frames)):
            self.hit_frames[i] = pygame.transform.scale_by(self.hit_frames[i], scale)

        #Handle rect info
        self.rect = self.body_img.get_frect()
        self.hitbox = pygame.Rect(position, (30, 25))
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
            self.hitbox.topleft = (self.rect.x+20, self.rect.y+35)

            #Caught Animation
            if self.caught >= 18:
                if pygame.time.get_ticks() - self.time >= 200:
                    self.time = pygame.time.get_ticks()
                    self.caught = random.randint(1,3)
                    self.caught *= 3
                    self.caught += 15
            if 0 < self.caught <= 18:
                self.caught += 1

            #Caught bounce off walls
            if self.rect.x+40 >= screen_width-21 or self.rect.x+30 <= 21:
                self.xaccel *= -0.9

            #print(f"{self.rect.x}, {self.rect.y}")

            self.lasty = self.rect.y


    def hit(self):
        if self.caught == 0:
            self.xaccel = random.randint(-4,4)
            self.yaccel = -10
            self.caught = 1
            return 1
        return 0

    def draw(self, screen):
        if self.caught != 0:
            screen.blit(self.hit_frames[math.floor(self.caught/3)], (self.rect.x, self.rect.y))
            screen.blit(self.tail_img, (self.rect.x - (self.xaccel/100)*10, self.rect.y - (self.yaccel/100)*10))
            screen.blit(self.body_img, (self.rect.x, self.rect.y))
            screen.blit(self.head_img, (self.rect.x-(self.xaccel/100)*10, self.rect.y-(self.yaccel/100)*10))
            screen.blit(self.hit_frames[math.floor(self.caught/3)], (self.rect.x, self.rect.y))
        else:
            screen.blit(self.tail_img, (self.rect.x - self.xaccel * 0.5, self.rect.y - self.yaccel * 0.5))
            screen.blit(self.body_img, (self.rect.x, self.rect.y))
            screen.blit(self.head_img, (self.rect.x - self.xaccel * 0.5, self.rect.y - self.yaccel * 0.5))