import time
import pygame.font
from levels import *
from carrot_logic import *
import asyncio


pygame.init()
start = time.time()
clock = pygame.time.Clock()
pygame.display.set_icon(icon)
pygame.display.set_caption("Bunny Jumper")
score_font = pygame.font.Font("media/Tiny5-Regular.ttf", 32)

score = 0
score_position = (0,0)
lives = [0,0,0]
skip_intro = 0
level_transition = 0
level_timer = 0
level_animation = 0
current_frame = 0
endless_timer = 0
bunny_limit = 0
carrot_limit = 0
life_offset = (random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5))
game_over = False

bunny_group, special_logic, background_image = level1()
carrot_group = []

async def main():
    global carrot_group, background_image,special_logic, bunny_group, game_over, life_offset, carrot_limit, bunny_limit, endless_timer, current_frame, score, score_position, lives, skip_intro,level_animation, level_timer, level_transition, screen_height, screen, start, clock

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        dt = time.time() - start
        start = time.time()
        if endless_timer != 0:
            endless_timer += 1

        #Special level logic, if special is equal to -1 there is no special logic

        if special_logic != -1:
            # Endless mode
            if special_logic == 3:

                if endless_timer == 0:
                    endless_timer += 1

                if endless_timer < 20*7:
                    for i in range(len(lives)):
                        lives[i] = math.floor((endless_timer/20))

                if endless_timer < 60*15:
                    bunny_limit = 1
                    carrot_limit = 3

                if 60*15 < endless_timer < 60*30:
                    bunny_limit = 2
                    carrot_limit = 5

                if 60*30 < endless_timer < 60*45:
                    bunny_limit = 4
                    carrot_limit = 5

                if 60*60 < endless_timer < 60*75:
                    bunny_limit = 6
                    carrot_limit = 4

                if 60*75 < endless_timer < 60*90:
                    bunny_limit = 8
                    carrot_limit = 4

                if 60*90 < endless_timer < 60*120:
                    bunny_limit = 12
                    carrot_limit = 4

                if 60*120 < endless_timer < 60*240:
                    bunny_limit = 16
                    carrot_limit = 4

                if 60*240 < endless_timer < 60*420:
                    bunny_limit = 24
                    carrot_limit = 3

                if 60*420 < endless_timer < 60*540:
                    bunny_limit = 28
                    carrot_limit = 2

                if 60*540 < endless_timer < 60*660:
                    bunny_limit = 30
                    carrot_limit = 1

                if 60*660 < endless_timer < 60*720:
                    bunny_limit = 40
                    carrot_limit = 1

                if game_over:
                    bunny_limit = -1
                    carrot_limit = -1


                if len(carrot_group) < carrot_limit:
                    carrot_group.append(Carrot((random.randint(200, 600), 768), (random.randint(-4, 4), random.uniform(-23, -15)), random.randint(0, 10)))
                if len(bunny_group) < bunny_limit:
                    bunny_group.append(Bunny((random.randint(201, 601), 768), (random.randint(-4, 4), random.uniform(-23, -15)), random.randint(0, 10)))

            if special_logic == 1:
                if pygame.mouse.get_pressed()[0]:
                    level_transition = 1
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    skip_intro = 1
                    level_transition = 1
            if special_logic == 2:
                level_animation = 1


        if level_transition != 0:
            #Draw level transitions
            #Level 0 to 1 transition
            if level_transition == 1:
                #Level timer should be animation frames * 3 - 1
                level_timer += 1
                current_frame = math.floor(level_timer/3)
                screen.blit(background1_list[current_frame], (0,0))

                if current_frame == 85:
                    bunny_group, special_logic, background_image = level2()
                    level_timer = 0
                    level_transition = 0
                    current_frame = 0

        elif level_animation != 0 :
            #Level 1's (tutorial) animation
            if level_animation == 1 and skip_intro != 1:
                screen.blit(background_image[0], (0,0))
                current_frame += 1/3
                screen.blit(overlay2_list[math.floor(current_frame)], (240, 256))

                if math.floor(current_frame) == 51:
                    current_frame = 51
                    if pygame.mouse.get_pressed()[0]:
                        current_frame = 52

                if math.floor(current_frame) == 90:
                    current_frame = 90
                    if pygame.mouse.get_pressed()[0]:
                        current_frame = 91

                if math.floor(current_frame) == 153:
                    current_frame = 153
                    if score > 0:
                        current_frame = 154
                    else:
                        if not carrot_group:
                            carrot_group.append(Carrot((random.randint(200, 600), 768), (random.randint(-4,4),-20)))

                if math.floor(current_frame) == 199:
                    current_frame = 199
                    if pygame.mouse.get_pressed()[0]:
                        current_frame = 200

                if math.floor(current_frame) == 252:
                    current_frame = 252
                    if pygame.mouse.get_pressed()[0]:
                        current_frame = 253

                if math.floor(current_frame) == 307:
                    current_frame = 307
                    if pygame.mouse.get_pressed()[0]:
                        current_frame = 308

                if math.floor(current_frame) == 367:
                    current_frame = 367
                    if pygame.mouse.get_pressed()[0]:
                        current_frame = 368

                if math.floor(current_frame) == 451:
                    current_frame = 451
                    if pygame.mouse.get_pressed()[0]:
                        current_frame = 452

                if math.floor(current_frame) == 535:
                    current_frame = 0
                    level_animation = 0
                    endless_timer = 1
                    special_logic = 3
            elif skip_intro == 1:
                current_frame = 0
                level_animation = 0
                endless_timer = 1
                special_logic = 3

        else:
            # fill background if not in a transition state
            screen.blit(background_image[current_frame], (0, 0))

        #Bunny logic
        if pygame.mouse.get_pressed()[0]:
            mousepos = pygame.mouse.get_pos()
            for bunny in bunny_group:
                if bunny.hitbox.collidepoint(mousepos):
                    if lives[2] <= 6:
                        lives[2] += bunny.hit()
                    elif lives[1] <= 6:
                        lives[1] += bunny.hit()
                    else:
                        lives[0] += bunny.hit()
                    if lives[0] > 6 and lives[1] > 6 and lives[2] > 6:
                        game_over = True
            for carrot in carrot_group:
                if carrot.rect.collidepoint(mousepos):
                    score += carrot.hit()

        for carrot in carrot_group:
            carrot.update()
            carrot.draw(screen)
            if carrot.rect.y > screen_height+100:
                carrot_group.remove(carrot)
        for bunny in bunny_group:
            bunny.update()
            bunny.draw(screen)
            if bunny.rect.y > screen_height+100:
                bunny_group.remove(bunny)

        if endless_timer % 30 == 0:
            life_offset = (random.randint(-4, 4), random.randint(-4, 4), random.randint(-4, 4))
        #Draw overlay
        if endless_timer != 0:
            score_img = score_font.render(f"Score: {score}", False,"#e7ffb7")
            score_position = (-31 + life_offset[2] + 1024 - score_img.get_width(), 31 + life_offset[1])
            if game_over:
                pass
                score_position = (512-score_img.get_width()/2, 384-score_img.get_height()/2)
            screen.blit(score_img, score_position)
            for i in range(3):
                if 6 < lives[i] < 9:
                    lives[i] += 1/20
                if 9 <= lives[i] <  13:
                    lives[i] += 1/20
                    if math.floor(lives[i]) == 12:
                        lives[i] = 9
                screen.blit(life_img_list[math.floor(lives[i])], (31+i*54+life_offset[-i], 31+life_offset[i]))
        screen.blit(overlay1_img, (0,0))
        #pygame.draw.circle(screen, (255,0,0), (512, 384), 3)

        await asyncio.sleep(0)
        pygame.display.flip()
        clock.tick(60)

asyncio.run(main())
