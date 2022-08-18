import random, time
import pygame, sys, PygameUI
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
CELLSIZE = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 255, 255)
DEEPBLUE = (11, 27, 50)

BGCOLOR = DEEPBLUE
SNAKECOLOR = GREEN
FOODCOLOR = RED

MENU = "MENU"
PLAY = "PLAY"
GAMEOVER = "GAMEOVER"
RIGHT = "right"
LEFT = "left"
DOWN = "down"
UP = "up"


def main():
    global DISPLAY, EVENTS, STATE, CURRENT_LEVEL
    global Levels, currentLevel, levelsFile
    global WINDOWWIDTH, WINDOWHEIGHT

    pygame.init()

    pygame.display.set_caption("Snakey")

    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FPSCLOCK = pygame.time.Clock()

    levelsFile = open("Levels.txt", "r").readlines()  # The text file that contains all the levels in the game

    STATE = None
    direction = DOWN
    startx, starty = 5, 5  # starting x and y positions
    Levels = getLevels()
    currentLevel = Levels[0]
    CURRENT_LEVEL = getLevelFor(currentLevel)
    snakeCoords = [(startx, starty), (startx - 1, starty), (startx - 2, starty)]

    SwitchState(MENU)
    food = getRandomLocation()

    gameOverText = PygameUI.Text("Game Over!", WHITE, int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2),
                                 font=("Helvetica", 30))
    scoreText = PygameUI.Text("<SCORE>", WHITE, WINDOWWIDTH - 30, 0, font=("Helvetica", 20), anchor="topright")
    titleText = PygameUI.Text("Snakey!", BLACK, int(WINDOWWIDTH/2), 50, font=("Helvetica", 70), bold=True)
    levelText = PygameUI.Text("Level:", BLACK, int(WINDOWWIDTH / 2)-180, int(WINDOWHEIGHT / 2)+20, font=("Georgia", 30),
                              bold=True)
    levelButton = PygameUI.Button("<level>", (int(WINDOWWIDTH / 2)-130, int(WINDOWHEIGHT / 2), 250, 40),
                                  border=((0, 0, 0), 2),
                                  padding=(10, 3), onclick=switchLevel, textsize=40)
    playButton = PygameUI.Button("PLAY", (int(WINDOWWIDTH / 2) - 50, int(WINDOWHEIGHT / 2) + 50, 100, 30),
                                 fillcolor=YELLOW,
                                 textsize=30, onclick=lambda: SwitchState(PLAY))

    while True:
        EVENTS = pygame.event.get()
        checkForQuit()

        if STATE == MENU:
            DISPLAY.fill(BGCOLOR)
            levelButton.text = currentLevel
            levelButton.display(DISPLAY, EVENTS)
            playButton.display(DISPLAY, EVENTS)
            titleText.display(DISPLAY)
            levelText.display(DISPLAY)

        elif STATE == PLAY:
            DISPLAY.fill(BGCOLOR)
            drawGame(CURRENT_LEVEL, food)
            drawSnake(snakeCoords)
            score = len(snakeCoords) - 3
            scoreText.text = f"Score: {score}"
            scoreText.display(DISPLAY)

            for event in EVENTS:
                if event.type == KEYDOWN:
                    if event.key == K_LEFT and direction != RIGHT:
                        direction = LEFT
                    elif event.key == K_RIGHT and direction != LEFT:
                        direction = RIGHT
                    elif event.key == K_UP and direction != DOWN:
                        direction = UP
                    elif event.key == K_DOWN and direction != UP:
                        direction = DOWN

            headx, heady = snakeCoords[0]

            if (headx, heady) == food:
                food = getRandomLocation()
            else:
                del snakeCoords[-1]

            if (headx, heady) in snakeCoords[1:] or CURRENT_LEVEL[heady][headx] == "#":
                # if snake's head touches itself or an obstacle
                SwitchState(GAMEOVER)

            if direction == LEFT:
                if headx - 1 < 0:
                    snakeCoords.insert(0, (int(WINDOWWIDTH / CELLSIZE) - 1, heady))
                else:
                    snakeCoords.insert(0, (headx - 1, heady))
            elif direction == RIGHT:
                if headx + 1 > int(WINDOWWIDTH / CELLSIZE) - 1:
                    snakeCoords.insert(0, (0, heady))
                else:
                    snakeCoords.insert(0, (headx + 1, heady))
            elif direction == UP:
                if heady - 1 < 0:
                    snakeCoords.insert(0, (headx, int(WINDOWHEIGHT / CELLSIZE) - 1))
                else:
                    snakeCoords.insert(0, (headx, heady - 1))
            elif direction == DOWN:
                if heady + 1 > int(WINDOWHEIGHT / CELLSIZE) - 1:
                    snakeCoords.insert(0, (headx, 0))
                else:
                    snakeCoords.insert(0, (headx, heady + 1))

        elif STATE == GAMEOVER:
            gameOverText.display(DISPLAY)

            for event in EVENTS:
                if event.type == KEYUP:
                    main()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    QUIT_KEYS = [K_RSHIFT, K_LSHIFT]
    for event in EVENTS:
        if event.type == QUIT or (event.type == KEYUP and event.key in QUIT_KEYS):
            terminate()


def SwitchState(newState):
    global STATE, BGCOLOR, CURRENT_LEVEL
    STATE = newState
    if newState == MENU:
        BGCOLOR = GREEN
    elif newState == PLAY:
        BGCOLOR = DEEPBLUE
        CURRENT_LEVEL = getLevelFor(currentLevel)


def switchLevel():
    global currentLevel
    currentLevel = Levels[(Levels.index(currentLevel) + 1) % len(Levels)]


def getRandomLocation():
    x = random.randrange(int(WINDOWWIDTH / CELLSIZE))
    y = random.randrange(int(WINDOWHEIGHT / CELLSIZE))
    if CURRENT_LEVEL[y][x] == "#":
        x, y = getRandomLocation()
    return x, y


def drawSnake(coords):
    for left, top in coords:
        left, top = left * CELLSIZE, top * CELLSIZE
        pygame.draw.rect(DISPLAY, SNAKECOLOR, (left, top, CELLSIZE, CELLSIZE))


def drawGame(level, food_pos):
    foodx, foody = food_pos
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                left, top = CELLSIZE * x, CELLSIZE * y
                pygame.draw.rect(DISPLAY, LIGHTBLUE, (left, top, CELLSIZE, CELLSIZE))
                pygame.draw.rect(DISPLAY, WHITE, (left, top, CELLSIZE, CELLSIZE), 1)

    left, top = CELLSIZE * foodx, CELLSIZE * foody
    pygame.draw.rect(DISPLAY, FOODCOLOR, (left, top, CELLSIZE, CELLSIZE))


def getLevels():
    levels = list(filter(lambda x: x[0] == '=', levelsFile))
    if levels:
        levels = list(map(lambda x: x[2:-1], levels))
    else:
        levels = ["Original"]
    return levels


def getLevelFor(level):
    Level = []
    if level == "Original":
        Level = [['.']*20]*20
    else:
        for _ in range(len(levelsFile)):
            if f'=={level}' in levelsFile[_]:
                for i in range(1, 21):
                    Level.append(list(levelsFile[_ + i])[:-1])
                break
    return Level


if __name__ == "__main__":
    main()
