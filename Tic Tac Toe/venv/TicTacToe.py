import copy
import random
import sys

from PygameUI import *

WINDOWWIDTH = 700
WINDOWHEIGHT = 700
BOARDWIDTH = 3
BOARDHEIGHT = 3
BOXSIZE = 100
DIFFICULTY = 7
ROUNDS = 1
BOARDBORDERSIZE = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 126, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 240)

BGCOLOR = WHITE
HLBCOLOR = GREEN
PXCOLOR = RED
POCOLOR = GREEN
BOARDBORDERCOLOR = BLACK

EMPTY = ''
HUMAN = 'HUMAN'
AI = 'AI'

MENU = 'menu'
INIT = 'init'
PLAY = 'play'
GAMEOVER = 'gameover'

PLAYERX = HUMAN
PLAYERO = HUMAN

assert BOARDWIDTH == BOARDHEIGHT, "Boardwidth and boardheight must be equal"
assert WINDOWWIDTH > (BOARDWIDTH * (BOXSIZE + BOARDBORDERSIZE)) and WINDOWHEIGHT > (
        BOARDHEIGHT * (BOXSIZE + BOARDBORDERSIZE)), "Not enough space on window"
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + BOARDBORDERSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + BOARDBORDERSIZE))) / 2)


def main():
    global DISPLAY, MAIN_BOARD, EVENTS, TURN, STATE
    global BGCOLOR, PLAYER
    global SCORE_X, SCORE_O
    global gameIsOver, winner, rounds

    pygame.init()

    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Tic Tac Toe")

    TURN = 'X'
    PLAYER = {'X': PLAYERX, 'O': PLAYERO}

    STATE = None
    MAIN_BOARD = getNewBoard(EMPTY)
    gameIsOver = False
    winner = None
    rounds = 0
    SwitchState(MENU)

    SCORE_X = 0
    SCORE_O = 0

    titleText = Text("TIC TAC TOE", BLACK, int(WINDOWWIDTH / 2), 20, True, font=("Helvetica", 50))
    pxText = Text("PlayerX:", BLACK, int(WINDOWWIDTH / 2) - 100, int(WINDOWHEIGHT / 2) - 40, False,
                  font=("Helvetica", 20))
    winnerText = Text("<WINNNER>", BLACK, int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2), True, font=("Helvetica", 50),
                      bgcolor=RED)
    roundsText = Text("<ROUNDS>", BLACK, int(WINDOWWIDTH / 2), 20, font=("Helvetica", 50))
    pyText = Text("PlayerO:", BLACK, int(WINDOWWIDTH / 2) - 100, int(WINDOWHEIGHT / 2) + 40, False,
                  font=("Helvetica", 20))
    rText = Text("Rounds:", BLACK, int(WINDOWWIDTH / 2) - 100, int(WINDOWHEIGHT / 2), False, font=("Helvetica", 20))

    pxButton = Button(str(PLAYERX), (int(WINDOWWIDTH / 2) - 50, int(WINDOWHEIGHT / 2) - 50, 100, 30), border=(BLACK, 2),
                      padding=(20, 3))
    pxButton.onclick = lambda: SwitchControlType(pxButton)
    pyButton = Button(str(PLAYERO), (int(WINDOWWIDTH / 2) - 50, int(WINDOWHEIGHT / 2) + 30, 100, 30), border=(BLACK, 2),
                      padding=(20, 3))
    pyButton.onclick = lambda: SwitchControlType(pyButton)
    rButton = Button(str(ROUNDS), (int(WINDOWWIDTH / 2) - 50, int(WINDOWHEIGHT / 2) - 10, 50, 30), border=(BLACK, 2),
                     padding=(20, 3))
    upButton = Button("+", (int(WINDOWWIDTH / 2) + 5, int(WINDOWHEIGHT / 2) - 10, 20, 15), fillcolor=GREEN)
    upButton.onclick = lambda: do_stuff(rButton, 'r', 'increase')
    downButton = Button("-", (int(WINDOWWIDTH / 2) + 5, int(WINDOWHEIGHT / 2) + 5, 20, 15), fillcolor=RED)
    downButton.onclick = lambda: do_stuff(rButton, 'r', 'reduce')
    playButton = Button("PLAY", (int(WINDOWWIDTH / 2) - 70, int(WINDOWHEIGHT / 2) + 80, 120, 30), border=(BLACK, 2),
                        padding=(30, 3), font=("Arial", True, False), fillcolor=YELLOW)
    playButton.onclick = lambda: SwitchState(PLAY, True)
    menuButton = Button("GO TO MENU", (WINDOWWIDTH - 200, WINDOWHEIGHT - 90, 150, 30), border=(BLACK, 2),
                        padding=(5, 3), font=("Arial", True, False), fillcolor=YELLOW)
    menuButton.onclick = lambda: main()
    play_againButton = Button("PLAY AGAIN", (WINDOWWIDTH - 200, WINDOWHEIGHT - 50, 150, 30), border=(BLACK, 2),
                              padding=(10, 3), font=("Arial", True, False), fillcolor=YELLOW)
    play_againButton.onclick = lambda: SwitchState(PLAY, True)

    while True:
        EVENTS = pygame.event.get()
        DISPLAY.fill(BGCOLOR)

        if STATE == MENU:
            titleText.display(DISPLAY)
            pxText.display(DISPLAY)
            pyText.display(DISPLAY)
            rText.display(DISPLAY)
            PLAYER['X'] = pxButton.text
            PLAYER['O'] = pyButton.text
            pxButton.display(DISPLAY, EVENTS)
            pyButton.display(DISPLAY, EVENTS)
            playButton.display(DISPLAY, EVENTS)
            rButton.display(DISPLAY, EVENTS)
            upButton.display(DISPLAY, EVENTS)
            downButton.display(DISPLAY, EVENTS)
        elif STATE == PLAY:
            drawBoard(MAIN_BOARD)
            pxText.left, pxText.top = 50, 10
            pyText.left, pyText.top = WINDOWWIDTH - 50, 10
            pxText.text = f"PlayerX: {SCORE_X}"
            pyText.text = f"PlayerO: {SCORE_O}"
            roundsText.text = f"Round: {min(rounds + 1, ROUNDS)}"
            pxText.display(DISPLAY)
            pyText.display(DISPLAY)
            roundsText.display(DISPLAY)
            menuButton.display(DISPLAY, EVENTS)
            play_againButton.display(DISPLAY, EVENTS)

            if winner:
                gameIsOver = True
                if winner == 'X':
                    SCORE_X += 1
                elif winner == 'O':
                    SCORE_O += 1
                SwitchState(PLAY)

            elif isBoardFull(MAIN_BOARD):
                gameIsOver = True
                SwitchState(PLAY)

            if rounds == ROUNDS:
                gameIsOver = True
                winner = None
                hasWon(MAIN_BOARD, True)
                if SCORE_X > SCORE_O:
                    winnerText.text = 'X wins!!!'
                    winnerText.display(DISPLAY)
                elif SCORE_O > SCORE_X:
                    winnerText.text = 'O wins!!!'
                    winnerText.display(DISPLAY)
                else:
                    winnerText.text = 'TIE!!!'
                    winnerText.display(DISPLAY)

            if PLAYER[TURN] == AI and not gameIsOver:
                AIMove(MAIN_BOARD)

        for event in EVENTS:
            if event.type == QUIT:
                terminate()
        pygame.display.update()


def getNewBoard(value):
    board = []
    for _ in range(BOARDHEIGHT):
        board.append([value] * BOARDWIDTH)
    return board


def do_stuff(buttonObj, vname, action):
    global ROUNDS
    if action == "increase":
        if vname == 'r':
            ROUNDS += 1
            buttonObj.text = str(ROUNDS)
    else:
        if vname == 'r':
            ROUNDS = max(ROUNDS - 1, 1)
            buttonObj.text = str(ROUNDS)


def AIMove(board, delay=0):
    global winner
    x, y = getAIMove(board)
    board[y][x] = TURN
    winner = hasWon(board)
    switchTurns()


def SwitchControlType(buttonObj):
    if buttonObj.text == HUMAN:
        buttonObj.text = AI
    else:
        buttonObj.text = HUMAN


def SwitchState(newState, reset=False):
    global BGCOLOR, MAIN_BOARD, STATE
    global SCORE_X, SCORE_O
    global gameIsOver, winner, rounds

    STATE = newState
    if STATE == MENU:
        BGCOLOR = ORANGE
        return
    elif STATE == PLAY:
        if reset:
            rounds = 0
            SCORE_X = 0
            SCORE_O = 0
            reset = False
        else:
            if rounds != ROUNDS: rounds += 1
        BGCOLOR = WHITE
        winner = None
        gameIsOver = False
        if rounds != ROUNDS:
            MAIN_BOARD = getNewBoard(EMPTY)
        return
    else:
        return


def terminate():
    pygame.quit()
    sys.exit()


def getLeftTopCoords(boxx, boxy):
    _left = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * boxx
    _top = YMARGIN + (BOXSIZE + BOARDBORDERSIZE) * boxy
    return _left, _top


def isValidMove(board, x, y):
    if board[y][x] == EMPTY:
        return True
    return False


def switchTurns():
    global TURN
    if TURN == 'X':
        TURN = 'O'
    else:
        TURN = 'X'


def getHumanMove(x, y, board):
    global winner
    if isValidMove(board, x, y):
        board[y][x] = TURN
        winner = hasWon(board)
        switchTurns()


def getComputerMove(board):
    player = True if TURN == 'X' else False
    eval, (x, y) = minimax(board, player, DIFFICULTY, float("-inf"), float("inf"))
    print(eval, x, y)
    return x, y


def getAIMove(board):
    if (PLAYER['X'], PLAYER['O']) == (AI, AI):
        if TURN == 'X':
            return getAI1Move(board)
        else:
            return getAI2Move(board)
    else:
        return getComputerMove(board)


def getAI1Move(board):
    return getComputerMove(board)


def getAI2Move(board):
    # random playing AI
    moves = [(x, y) for y in range(BOARDHEIGHT) for x in range(BOARDWIDTH)]
    validMoves = list(filter(lambda p: isValidMove(board, p[0], p[1]), moves))
    return random.choice(validMoves)

    # smart AI
    # return getComputerMove(board)


def minimax(gameState, maxPlayer, lookAhead, alpha, beta):
    winner = hasWon(gameState)
    if lookAhead == 0 or winner or isBoardFull(gameState):
        return evaluate(winner), (None, None)

    if maxPlayer:
        maxEval, pos = float('-inf'), (None, None)
        for y in range(BOARDHEIGHT):
            for x in range(BOARDWIDTH):
                dupState = copy.deepcopy(gameState)
                if not isValidMove(dupState, x, y):
                    continue
                dupState[y][x] = 'X'
                evaluation = minimax(dupState, False, lookAhead - 1, alpha, beta)
                if evaluation[0] > maxEval:
                    maxEval = evaluation[0]
                    pos = (x, y)
                alpha = max(alpha, evaluation[0])
                if beta <= alpha:
                    break
        return maxEval, pos

    else:
        minEval, pos = float('inf'), (None, None)
        for y in range(BOARDHEIGHT):
            for x in range(BOARDWIDTH):
                dupState = copy.deepcopy(gameState)
                if not isValidMove(dupState, x, y):
                    continue
                dupState[y][x] = 'O'
                evaluation = minimax(dupState, True, lookAhead - 1, alpha, beta)
                if evaluation[0] < minEval:
                    minEval = evaluation[0]
                    pos = (x, y)
                beta = min(beta, evaluation[0])
                if beta <= alpha:
                    break
        return minEval, pos


def evaluate(winPlayer):
    if winPlayer == 'X':
        return 10
    if winPlayer == 'O':
        return -10
    return 0


def isBoardFull(board):
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH):
            if board[y][x] == EMPTY:
                return False
    return True


def hasWon(board, draw=False):
    # Vertical check
    for x in range(BOARDWIDTH):
        list = [board[y][x] for y in range(BOARDHEIGHT)]
        if list in (['X'] * BOARDHEIGHT, ['O'] * BOARDHEIGHT):
            if draw:
                start_pos = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * x + int(BOXSIZE / 2), YMARGIN
                end_pos = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * x + int(BOXSIZE / 2), YMARGIN + (
                        BOXSIZE + BOARDBORDERSIZE) * BOARDHEIGHT
                pygame.draw.line(DISPLAY, BOARDBORDERCOLOR, start_pos, end_pos, BOARDBORDERSIZE + 3)
            return list[0]

    # Horizontal check
    for y in range(BOARDHEIGHT):
        list = [board[y][x] for x in range(BOARDWIDTH)]
        if list in (['X'] * BOARDWIDTH, ['O'] * BOARDWIDTH):
            if draw:
                start_pos = XMARGIN, YMARGIN + (BOXSIZE + BOARDBORDERSIZE) * y + int(BOXSIZE / 2)
                end_pos = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * BOARDWIDTH, YMARGIN + (
                        BOXSIZE + BOARDBORDERSIZE) * y + int(BOXSIZE / 2)
                pygame.draw.line(DISPLAY, BOARDBORDERCOLOR, start_pos, end_pos, BOARDBORDERSIZE + 3)
            return list[0]

    # Right diagonal check
    list = [board[x][x] for x in range(BOARDWIDTH)]
    if list in (['X'] * BOARDHEIGHT, ['O'] * BOARDHEIGHT):
        if draw:
            start_pos = XMARGIN, YMARGIN
            end_pos = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * BOARDWIDTH, YMARGIN + (
                    BOXSIZE + BOARDBORDERSIZE) * BOARDHEIGHT
            pygame.draw.line(DISPLAY, BOARDBORDERCOLOR, start_pos, end_pos, BOARDBORDERSIZE + 3)
        return list[0]

    # Left diagonal check
    list = [board[x][BOARDWIDTH - x - 1] for x in range(BOARDWIDTH)]
    if list in (['X'] * BOARDHEIGHT, ['O'] * BOARDHEIGHT):
        if draw:
            start_pos = XMARGIN, YMARGIN + (BOXSIZE + BOARDBORDERSIZE) * BOARDHEIGHT
            end_pos = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * BOARDWIDTH, YMARGIN
            pygame.draw.line(DISPLAY, BOARDBORDERCOLOR, start_pos, end_pos, BOARDBORDERSIZE + 3)
        return list[0]
    return None


def drawBoard(board):
    # horizontal border lines
    for x in range(1, BOARDWIDTH):
        start_pos = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * x, YMARGIN
        end_pos = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * x, YMARGIN + (BOXSIZE + BOARDBORDERSIZE) * BOARDHEIGHT
        pygame.draw.line(DISPLAY, BOARDBORDERCOLOR, start_pos, end_pos, BOARDBORDERSIZE)

    # vertical border lines
    for y in range(1, BOARDHEIGHT):
        start_pos = XMARGIN, YMARGIN + (BOXSIZE + BOARDBORDERSIZE) * y
        end_pos = XMARGIN + (BOXSIZE + BOARDBORDERSIZE) * BOARDWIDTH, YMARGIN + (BOXSIZE + BOARDBORDERSIZE) * y
        pygame.draw.line(DISPLAY, BOARDBORDERCOLOR, start_pos, end_pos, BOARDBORDERSIZE)

    # display invisible boxes that will contain either an 'X' or 'O'
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH):
            left, top = getLeftTopCoords(x, y)
            box = Button(board[y][x], (left, top, BOXSIZE, BOXSIZE), False, font=("Georgia", False, False),
                         padding=(15, 0), textsize=100)
            box.textcolor = PXCOLOR if board[y][x] == 'X' else POCOLOR
            # box.onhover = lambda: drawHighlightBox(x, y, left, top, board)
            box.onclick = lambda: getHumanMove(x, y, board) if PLAYER[TURN] == HUMAN and not gameIsOver else None
            box.display(DISPLAY, EVENTS)


def drawHighlightBox(x, y, left, top, board):
    if isValidMove(board, x, y) and not gameIsOver:
        pygame.draw.rect(DISPLAY, HLBCOLOR, (left + BOARDBORDERSIZE, top, BOXSIZE, BOXSIZE), BOARDBORDERSIZE + 3)


if __name__ == "__main__":
    main()
