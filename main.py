import pygame, os, time, sys
from copy import deepcopy
from random import choice, randrange
from button import Button



#! SCREEN ##########################################################################################################

W, H = 10, 21 #space pieces
TILE = 30 #Square - board size
GAME_RES = W * TILE, H * TILE #Game board
RES = 590, 670 #screen resolution
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES) 
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
pygame.init()


#! MEDIA ###########################################################################################################################


bg_menu = pygame.image.load("img/menu.jpg")
bg_opt = pygame.image.load("img/OPT.jpg")
game_bg = pygame.image.load('img/game.jpg').convert()
game_bg2 = pygame.image.load("img/game2.jpg")

#images trnsform
MENU_RES= pygame.transform.scale(bg_menu, RES)
OPT_RES= pygame.transform.scale(bg_opt, RES)
GAME_RES= pygame.transform.scale(game_bg, GAME_RES)
GAME_RES2= pygame.transform.scale(game_bg2, RES)

#ICON
gameIcon = pygame.image.load('img/logo.png')
pygame.display.set_icon(gameIcon)


#FONT
main_font = pygame.font.Font('font/modern-tetris.ttf', 50)
font = pygame.font.Font('font/modern-tetris.ttf', 45)
pygame.display.set_caption('TETRIS - By Javier')
name = pygame.font.Font('font/nintendo-nes-font.ttf', 20)

def get_font(size):
    return pygame.font.Font("font/nintendo-nes-font.ttf", size)

#MUSIC
def menu_music():
    pygame.mixer.music.load("music/MENU.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1000)
    
def main_music():
    pygame.mixer.music.load("music/game.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.20)

#! MENU ###########################################################################################################################
def by():
    title_BY = name.render('BY JAVIER', True, pygame.Color('#296049'))
    sc.blit(title_BY, (390, 650))


option = 60 #Difficulty
menu_music()
def main_menu():

    while True:
            sc.blit(MENU_RES, (0, 0)) #IMAGE BACKGROUND
            MENU_MOUSE_POS = pygame.mouse.get_pos() #MOUSE POSITION

            PLAY_BUTTON = Button(image=None, pos=(295, 470), # PLAY BOTTON
            text_input="PLAY", font=get_font(70), base_color="#296049", hovering_color="White")
            #  SCREEN TEXT      FONT AND SIZE         FONT COLOR       MOVE MOUSE IN THE BOTTON
            
            OPTIONS_BUTTON = Button(image=None, pos=(295, 540), # OPTION BOTON
            text_input="OPTIONS", font=get_font(45), base_color="#296049", hovering_color="White")

            QUIT_BUTTON = Button(image=None, pos=(295, 600), # QUIT BOTTON
            text_input="QUIT", font=get_font(40), base_color="#296049", hovering_color="White")
            
            by()

            
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(sc)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        maingame()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        options()

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
#!###########################################################################################################################
            
            
def options():
    global option
    while True:
        sc.blit(OPT_RES, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        by()

        EASY = Button(image=None, pos=(295, 300),
        text_input="EASY", font=get_font(55), base_color="#296049", hovering_color="White")

        MEDIUM = Button(image=None, pos=(295, 200),
        text_input="MEDIUM", font=get_font(55), base_color="#296049", hovering_color="White")
        
        HARD = Button(image=None, pos=(295, 100),
        text_input="HARD", font=get_font(55), base_color="#296049", hovering_color="White")

        OPTIONS_BACK = Button(image=None, pos=(295, 540),
        text_input="BACK", font=get_font(65), base_color="#296049", hovering_color="White")

            
        for button in [EASY, MEDIUM, HARD, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(sc)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if EASY.checkForInput(OPTIONS_MOUSE_POS):
                    option = 60

                if MEDIUM.checkForInput(OPTIONS_MOUSE_POS):
                    option = 150

                if HARD.checkForInput(OPTIONS_MOUSE_POS):
                    option = 300

        pygame.display.update()
                

#!###########################################################################################################################


def maingame():
    main_music()
    
    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
    figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                [(0, 0), (0, -1), (0, 1), (-1, -1)],
                [(0, 0), (0, -1), (0, 1), (1, -1)],
                [(0, 0), (0, -1), (0, 1), (-1, 0)]]
    
    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    field = [[0 for i in range(W)] for j in range(H)]


    anim_count, anim_speed, anim_limit = 0, option, 2000


    name = pygame.font.Font('font/nintendo-nes-font.ttf', 40)#

    title_tetris = name.render('TETRIS', True, pygame.Color('#413e3f'))
    title_score = name.render('SCORE', True, pygame.Color('#413e3f'))    
    title_record = name.render('RECORD', True, pygame.Color('#413e3f'))

    get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))


    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    color, next_color = get_color(), get_color()

    score, lines = 0, 0
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
    
    
    
    def check_borders():
        if figure[i].x < 0 or figure[i].x > W - 1:
            return False
        elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
            return False
        return True


    def get_record():
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')


    def set_record(record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))


    while True:
        record = get_record()
        dx, rotate = 0, False
        sc.blit(GAME_RES2, (0, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(GAME_RES, (0, 0))
        # delay for full lines
        for i in range(lines):
            pygame.time.wait(200)
        # control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True
                    
        # move x
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
            

        # move y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break

        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
            
        # check lines
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1

#!###########################################################################################################################
        # compute score
        score += scores[lines]
        # draw grid
        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
        
        
        
        # draw figure
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, color, figure_rect)
        # draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)
                        



            # draw next figure
        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 308
            figure_rect.y = next_figure[i].y * TILE + 155
            pygame.draw.rect(sc, next_color, figure_rect)
            
#!###########################################################################################################################
        # draw titles
        sc.blit(title_tetris, (332, 50))
        sc.blit(title_score, (355, 323))
        sc.blit(name.render(str(score), True, pygame.Color('#413e3f')), (439, 390))
        sc.blit(title_record, (341, 479))
        sc.blit(name.render(record, True, pygame.Color('#413e3f')), (403, 550))

        

#!###########################################################################################################################
        # game over
        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)
    
        pygame.display.flip()
        clock.tick(FPS)
main_menu()