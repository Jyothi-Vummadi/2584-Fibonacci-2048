import random
import pygame
from pygame.locals import *
from pygame import mixer

mixer.init()
mixer.music.load('background.wav')
mixer.music.play()

pygame.init()
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption('2584')

font = pygame.font.SysFont('oswald', 50)
font1 = pygame.font.SysFont('Architects Daughter', 50)
font2 = pygame.font.SysFont('oswald', 33)
font3 = pygame.font.SysFont('oswald', 50)

score_text = font.render('SCORE:', True, (0, 0, 0))
restart_text = font2.render("Press Space Bar to Restart the Game", True, (0, 0, 0))
start_text = font3.render("Press Tab to Start the Game", True, (0, 0, 0))
or_text = font3.render("Or", True, (0, 0, 0))
quit_text = font3.render("Press Escape to Quit the Game", True, (0, 0, 0))

background_img = pygame.image.load('img.png')
programIcon = pygame.image.load('logo.JPG')
gameover_img = pygame.image.load('game_over.jpg')
start_pic_img = pygame.image.load('start.jpg')
pygame.display.set_icon(programIcon)

'''grid = [[0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0]]'''
lst_score = []
lst = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]


# print(grid)
# grid_new = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]


def position_grid(grid):
    lst1 = []
    for i in range(0, 4):
        for j in range(0, 4):
            if grid[i][j] == 0:
                lst1.append([i, j])
    return lst1


def generate_1(grid, k=2):
    for i in range(0, k):
        if position_grid(grid) == []:
            return grid
        else:
            pos = random.choice(position_grid(grid))
            grid[pos[0]][pos[1]] = 1
    return grid


def reverse(grid):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(grid[i][3 - j])
    return new_mat


def transp(grid):
    new_mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        for j in range(4):
            new_mat[i][j] = grid[j][i]
    return new_mat


def compress(grid):
    new_mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(0, 4):
        pos_new = 0
        for j in range(0, 4):
            if grid[i][j] != 0:
                new_mat[i][pos_new] = grid[i][j]
                pos_new += 1
    return new_mat


def merge(grid):
    for i in range(0, 4):
        for j in range(0, 3):
            if grid[i][j] == 1 and grid[i][j + 1] == 1:
                mixer.music.load('sound.wav')
                mixer.music.play()
                grid[i][j] += grid[i][j + 1]
                lst_score.append(grid[i][j])
                grid[i][j + 1] = 0
            elif grid[i][j] in lst and grid[i][j + 1] == lst[lst.index(grid[i][j]) + 1] or grid[i][j] in lst and \
                    grid[i][j + 1] == lst[lst.index(grid[i][j]) - 1]:
                mixer.music.load('sound.wav')
                mixer.music.play()
                grid[i][j] += grid[i][j + 1]
                grid[i][j + 1] = 0
                lst_score.append(grid[i][j])
    return grid


def moveLeft(grid):
    st0 = compress(grid)
    st1 = merge(st0)
    st2 = compress(st1)
    st3 = generate_1(st2, k=1)
    return st3


def moveRight(grid):
    st0 = reverse(grid)
    st1 = compress(st0)
    st2 = merge(st1)
    st3 = compress(st2)
    st4 = reverse(st3)
    st5 = generate_1(st4, k=1)
    return st5


def moveUp(grid):
    st0 = transp(grid)
    st1 = compress(st0)
    st2 = merge(st1)
    st3 = compress(st2)
    st4 = transp(st3)
    st5 = generate_1(st4, k=1)
    return st5


def moveDown(grid):
    st0 = transp(grid)
    st = reverse(st0)
    st1 = compress(st)
    st2 = merge(st1)
    st3 = compress(st2)
    st3 = reverse(st3)
    st4 = transp(st3)
    st5 = generate_1(st4, k=1)
    return st5


def game_status(grid):
    # if any cell contains 2584 we win

    for i in range(4):
        for j in range(4):
            if grid[i][j] == 2584:
                return 'WON'

    # if at least 1 empty tile is left, game isn't over

    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return 'GAME NOT OVER'

    # if no cell is empty now but if after any move, any two cells gets merged and create an empty cell,game isn't over
    for i in range(4):
        for j in range(3):
            if grid[i][j] == 1 and grid[i][j + 1] == 1:
                return 'GAME NOT OVER'

    for i in range(3):
        for j in range(4):
            if grid[i][j] == 1 and grid[i + 1][j] == 1:
                return 'GAME NOT OVER'

    for i in range(4):
        for j in range(3):
            if (grid[i][j] in lst and grid[i][j + 1] == lst[lst.index(grid[i][j]) + 1] or grid[i][j] in lst and
                    grid[i][j + 1] == lst[lst.index(grid[i][j]) - 1]):
                return 'GAME NOT OVER'

    for i in range(3):
        for j in range(4):
            if (grid[i][j] in lst and grid[i + 1][j] == lst[lst.index(grid[i][j]) + 1] or grid[i][j] in lst and
                    grid[i + 1][j] == lst[lst.index(grid[i][j]) - 1]):
                return 'GAME NOT OVER'

    # else we have lost the game

    return 'LOST'


def restart():
    grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    lst_score.clear()
    return generate_1(grid, k=2)


def rectangle(grid):
    screen.fill((255, 255, 255))
    screen.blit(background_img, (0, 0))
    for i in range(0, 4):
        for j in range(0, 4):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40 + j * 140, 40 + i * 140, 100, 100),
                             border_radius=8)
            if grid[i][j] == 0:
                text_surface = font.render(f'{grid[i][j]}', True, (255, 255, 255))
            else:
                text_surface = font.render(f'{grid[i][j]}', True, (0, 0, 0))
            text_rectangle = text_surface.get_rect(center=((40 + j * 140) + 50, (40 + i * 140) + 50))
            score_surface = font.render(f'{sum(lst_score)}', True, (0, 0, 0))
            score_txt = score_surface.get_rect(center=(200, 635))
            screen.blit(text_surface, text_rectangle)
            screen.blit(score_surface, score_txt)
            screen.blit(score_text, (20, 620))
            screen.blit(restart_text, (10, 10))
    pygame.display.flip()


def keys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'q'
        if event.type == KEYDOWN:
            if event.key == K_TAB:
                return 't'
            elif event.key == K_ESCAPE:
                return 'q'
            elif event.key == K_LEFT:
                return 'l'
            elif event.key == K_RIGHT:
                return 'r'
            elif event.key == K_DOWN:
                return 'd'
            elif event.key == K_UP:
                return 'u'
            elif event.key == K_SPACE:
                return 'space'


def start():
    running = True
    while running:
        screen.blit(start_pic_img, (0, 0))
        screen.blit(start_text, (65, 50))
        screen.blit(or_text, (270, 100))
        screen.blit(quit_text, (45, 150))
        pygame.display.flip()
        choice = keys()
        if choice == 't':
            play([[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]])
        elif choice == 'q':
            pygame.quit()
            exit()
            running = False


def play(grid):
    grid1 = generate_1(grid, k=2)
    running = True
    while running:
        rectangle(grid1)
        pygame.display.flip()
        sta = game_status(grid1)
        if sta == 'LOST':
            screen.blit(gameover_img, (0, 0))
            pygame.display.flip()
            for i in range(0, 425000):
                print(" ")
            pygame.quit()
            exit()
        elif sta == 'WON':
            game_won = font.render('Game Won', True, (0, 0, 0))
            screen.blit(game_won, (200, 620))
            pygame.display.flip()
            running = False
            for i in range(0, 425000):
                print(" ")
        else:
            user_int = keys()
            if user_int == 'q':
                pygame.quit()
                exit()
            elif user_int == 'l':
                grid1 = moveLeft(grid1)
            elif user_int == 'r':
                grid1 = moveRight(grid1)
            elif user_int == 'u':
                grid1 = moveUp(grid1)
            elif user_int == 'd':
                grid1 = moveDown(grid1)
            elif user_int == 'space':
                grid1 = restart()


start()