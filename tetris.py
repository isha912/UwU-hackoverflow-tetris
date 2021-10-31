

import pygame
import random
 

 
pygame.font.init()
 
# GLOBALS VARS
sWidth = 800
sHeight = 700
playWidth = 300  
playHeight = 600 
sizeBlock = 30
 
topLeftX = (sWidth - playWidth) // 2
topLeftY = sHeight - playHeight
 
 
# SHAPE FORMATS
 
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['....',
  '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.00.',
    '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

 
 
class tetrisPiece(object):
    rows = 30  
    columns = 15  
 
    def __init__(variable, column, row, shape):
        variable.x = column
        variable.y = row
        variable.shape = shape
        variable.color = shape_colors[shapes.index(shape)]
        variable.rotation = 0  
 
def tetrisDrawGrid(surface, row, col):
    t_X = topLeftX
    t_Y = topLeftY
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (t_X, t_Y+ i*30), (t_X + playWidth, t_Y + i * 30)) 
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (t_X + j * 30, t_Y), (t_X + j * 30, t_Y + playHeight))  
 
def tetrisGridCreate(position={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in position:
                c = position[(j,i)]
                grid[i][j] = c
    return grid
 

 
def valid_space(s, grid):
    tetrisPosition = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    tetrisPosition = [j for sub in tetrisPosition for j in sub]
    tetrisFormated = tetrisShapeFormat(s)
 
    for pos in tetrisFormated:
        if pos not in tetrisPosition:
            if pos[1] > -1:
                return False
 
    return True
 
 
 
 
def tetrisGetShape():
    global shapes, shape_colors
 
    return tetrisPiece(5, 0, random.choice(shapes))
 
  
def tetrisDrawWindow(backDrop):
    backDrop.fill((200,20,20))
    # Tetris Title
    tetrisFont = pygame.font.SysFont('comicsans', 60)
    tetrisLabel = tetrisFont.render('TETRIS', 1, (100,255,255))
 
    backDrop.blit(tetrisLabel, (topLeftX + playWidth / 2 - (tetrisLabel.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(backDrop, grid[i][j], (topLeftX + j* 30, topLeftY + i * 30, 30, 30), 0)
 
  
    tetrisDrawGrid(backDrop, 20, 10)
    pygame.draw.rect(backDrop, (100 , 100, 100), (topLeftX, topLeftY, playWidth, playHeight), 5)

def tetrisDrawTextMiddle(text, size, color, surface):
    font = pygame.font.SysFont('arial', size, bold=True)
    label = font.render(text, 1, color)
 
    surface.blit(label, (topLeftX + playWidth/2 - (label.get_width() / 2), topLeftY + playHeight/2 - label.get_height()/2))
 
  
def tetrisShapeFormat(s):
    position = []
    format = s.shape[s.rotation % len(s.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                position.append((s.x + j, s.y + i))
 
    for i, pos in enumerate(position):
        position[i] = (pos[0] - 2, pos[1] - 4)
 
    return position
 
 
 
def tetrisClearRow(grid, locked):
 
    count = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            count += 1
           
            inc = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if count > 0:
        for ptr in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = ptr
            if y < inc:
                newKey = (x, y + count)
                locked[newKey] = locked.pop(ptr)
 
 
def terisNextShape(shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255,255,255))
 
    t_x = topLeftX + playWidth + 50
    t_y = topLeftY + playHeight/2 - 100
    TetrisFormat = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(TetrisFormat):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (t_x + j*30, t_y + i*30, 30, 30), 0)
 
    surface.blit(label, (t_x + 10, t_y- 30))
 

    
def tetrisLost(place):
    for position in place:
        x, y = position
        if y < 1:
            return True
    return False
 
 
def tetrisMain():
    global grid
 
    locked_positions = {}  
    grid = tetrisGridCreate(locked_positions)
 
    change_piece = False
    startt = True
 
    time = pygame.time.Clock()
    fall_time = 0
    tetrisCur = tetrisGetShape()
    tetrisNext = tetrisGetShape()
    while startt:
        fall_speed = 0.34
 
        grid = tetrisGridCreate(locked_positions)
        fall_time += time.get_rawtime()
        time.tick()
 
        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            tetrisCur.y += 1
            if not (valid_space(tetrisCur, grid)) and tetrisCur.y > 0:
                tetrisCur.y -= 1
                change_piece = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                startt = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetrisCur.x -= 1
                    if not valid_space(tetrisCur, grid):
                        tetrisCur.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    tetrisCur.x += 1
                    if not valid_space(tetrisCur, grid):
                        tetrisCur.x -= 1
                elif event.key == pygame.K_UP:
                    
                    tetrisCur.rotation = tetrisCur.rotation + 1 % len(tetrisCur.shape)
                    if not valid_space(tetrisCur, grid):
                        tetrisCur.rotation = tetrisCur.rotation - 1 % len(tetrisCur.shape)
 
                if event.key == pygame.K_DOWN:
                    # move shape down
                    tetrisCur.y += 1
                    if not valid_space(tetrisCur, grid):
                        tetrisCur.y -= 1
 
             
 
        shape_pos = tetrisShapeFormat(tetrisCur)
 
        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = tetrisCur.color
 
        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = tetrisCur.color
            tetrisCur = tetrisNext
            tetrisNext = tetrisGetShape()
            change_piece = False
 
            # call four times to check for multiple clear rows
            tetrisClearRow(grid, locked_positions)
 
        tetrisDrawWindow(win)
        terisNextShape(tetrisNext, win)
        pygame.display.update()
 
        # Check if user lost
        if tetrisLost(locked_positions):
            startt = False
 
    tetrisDrawTextMiddle("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)
 
 
def tetris():
    run = True
    while run:
        win.fill((0,0,0))
        tetrisDrawTextMiddle('Press any key to begin.', 60, (25, 55, 25), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                tetrisMain()
    pygame.quit()
 
 
win = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption('Tetris')
 

tetris()  
