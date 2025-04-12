import pygame, math

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

def animation_list(frames, width, height, image, length=0):
    img_list = []

    for i in range(frames):
        if length != 0:
            y = math.floor((i * width) / (length * width))*height
            offset = math.floor(y/height)*width*length
            #print(f"({-i * width + offset}, {y}), offset: {offset}")
            img_list.append(pygame.surface.Surface((width, height), flags=pygame.SRCALPHA))
            img_list[i].blit(image, ((-i * width) + offset, -y))
        else:
            img_list.append(pygame.surface.Surface((width, height), flags=pygame.SRCALPHA))
            img_list[i].blit(image, (-i * width, 0))
            #print(f"f: {-i * width}, {i}")

    return img_list

#load images
icon = pygame.image.load("media/icon.png").convert_alpha()
bunny_spritesheet = pygame.image.load("media/BunnyParts-Sheet.png").convert_alpha()
bunny_hit_spritesheet = pygame.image.load("media/BunnyHit-Sheet.png").convert_alpha()
carrot_spritesheet = pygame.image.load("media/Carrot-Sheet.png").convert_alpha()
life_spritesheet = pygame.image.load("media/life-Sheet.png").convert_alpha()

carrot_img_list = animation_list(7, 28, 56, carrot_spritesheet)
life_img_list = animation_list(12, 64, 64,life_spritesheet)

#Backgrounds
background1_img = pygame.image.load("media/Background1-Sheet.png").convert_alpha()
background2_img = pygame.image.load("media/Background2-Sheet.png").convert()
background1_list = animation_list(86, 1024, 768, background1_img, 10)
background2_list = animation_list(1, 1024, 768, background2_img)

#Overlays
overlay1_img = pygame.image.load("media/Overlay1.png").convert_alpha()
overlay2_img = pygame.image.load("media/Overlay2-Sheet.png").convert_alpha()
overlay2_list = animation_list(536, 420, 304, overlay2_img, 20)