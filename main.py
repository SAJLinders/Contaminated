from Game import Game
import pygame, sys
import Config
import Lang
import math
import random

from pygame.locals import *
from Cell import Cell
from Popup import Popup
from Timer import Timer
from Move import Move

# Initialize pygame window
pygame.init()
iconSurface = pygame.image.load("./Sprites/icon.png")
pygame.display.set_icon(iconSurface)
windowSurface = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
pygame.display.set_caption(Lang.GAME_NAME)

# Variables used for navigation
mainMenu = True
inGame = False
inPopup = False
firstGameCycle = False

# Method for updating the statistics in the bottom right corner of the game screen
def updateStats():
    marginBottom = Config.STATISTIC_MARGIN

    wrong = Lang.WRONG + game.getWrongAnswers()
    wrongSize = Config.STATISTIC_FONT.size(wrong)
    wrongPos = (
    Config.WINDOW_WIDTH - wrongSize[0] - Config.STATISTIC_MARGIN, Config.WINDOW_HEIGHT - marginBottom - wrongSize[1])
    marginBottom += wrongSize[1] + Config.STATISTIC_MARGIN

    found = Lang.FOUND + game.getCellsFound()
    foundSize = Config.STATISTIC_FONT.size(found)
    foundPos = (Config.WINDOW_WIDTH - foundSize[0] - Config.STATISTIC_MARGIN, Config.WINDOW_HEIGHT - marginBottom - foundSize[1])
    marginBottom += foundSize[1] + Config.STATISTIC_MARGIN

    playtime = timer.getPlayTime()
    playtimeSize = Config.STATISTIC_FONT.size(playtime)
    playTimePos = (Config.WINDOW_WIDTH - playtimeSize[0] - Config.STATISTIC_MARGIN, Config.WINDOW_HEIGHT - marginBottom - playtimeSize[1])

    windowSurface.blit(Config.STATISTIC_FONT.render(wrong, True, Config.STATISTIC_TEXT_COLOR), wrongPos)
    windowSurface.blit(Config.STATISTIC_FONT.render(found, True, Config.STATISTIC_TEXT_COLOR), foundPos)
    windowSurface.blit(Config.STATISTIC_FONT.render(timer.getPlayTime(), True, Config.STATISTIC_TEXT_COLOR), (playTimePos))

# Method used for handling cell clicks
def eventHandler(msg, x, y):
    try:
        game.playCell(x, y)
    except:
        print(Lang.CELL_ERROR_MSG)
    timer.pause()
    updateStats()
    move.stopMovement()
    popup = Popup(Config.POPUP_CONTENT_FONT, Config.CELL_TEXT_COLOR_VALUE, int(Config.WINDOW_WIDTH * 0.4), int(Config.WINDOW_HEIGHT * 0.4), msg, "Klik om door te gaan")
    windowSurface.blit(popup.content, (int(Config.WINDOW_WIDTH*0.3), int(Config.WINDOW_HEIGHT*0.3)))

# Method used to initialize game etc.
def renderGameField():
    # Create all cells
    for x in game.field:
        col = game.field[x]
        col_offset = x * (Config.CELL_WIDTH + Config.VERTICAL_WHITESPACE) + startPosition[0] + Config.TABLE_MARGIN
        colPosition = (col_offset, startPosition[1]+Config.TABLE_MARGIN)
        cells.append(Cell(windowSurface, col.name, colPosition, Config.HEADER_FONT, Config.CELL_TEXT_COLOR_HEADER,
                     Config.TEXT_MARGIN_LEFT, Config.CELL_BACKGROUND_COLOR_HEADER ,eventHandler, col.message,
                     col.contaminated, x, -1, True))

        for y in col.cells:
            cell = col.cells[y]
            cell_offset = (y+1) * (Config.CELL_HEIGHT + Config.HORIZONTAL_WHITESPACE) + startPosition[1] + Config.TABLE_MARGIN
            cellPosition = (col_offset, cell_offset)
            cells.append(Cell(windowSurface, cell.value, cellPosition, Config.VALUE_FONT, Config.CELL_TEXT_COLOR_VALUE,
                              Config.TEXT_MARGIN_LEFT, Config.CELL_BACKGROUND_COLOR_VALUE, eventHandler, cell.message,
                              cell.contaminated, x, y))

# Method for resetting a game
def resetGame():
    global game
    global cells
    global timer
    global move
    global startPosition

    startPosition = (
    random.randint(glassCenter[0] - tableDimensions[0] + Config.MARGIN_TOP, glassCenter[0] - Config.MARGIN_TOP),
    random.randint(glassCenter[1] - tableDimensions[1] + Config.MARGIN_LEFT, glassCenter[1] - Config.MARGIN_LEFT))

    game = Game(Config.LEVEL)
    cells = []
    timer = Timer()
    renderGameField()
    move = Move(cells, startPosition, tableDimensions, windowSurface, tableSprite, glassCenter)

game = Game(Config.LEVEL)
cells = []
timer = Timer()

# Positions and dimensions used in menu
positionUp = [int(Config.WINDOW_WIDTH*0.32), int(Config.WINDOW_HEIGHT*0.5)]
positionDown = [int(Config.WINDOW_WIDTH*0.32), int(Config.WINDOW_HEIGHT*0.62)]

# Positions and dimensions used in game
tableDimensions = ((game.getColumnCount() * Config.CELL_WIDTH) + ((game.getColumnCount()-1) * Config.HORIZONTAL_WHITESPACE),
                   ((game.getCellCount()+1) * Config.CELL_HEIGHT)  + (game.getCellCount() * Config.VERTICAL_WHITESPACE))
glassRadius = int(Config.WINDOW_HEIGHT * 0.25)
glassCenter = (int(Config.WINDOW_WIDTH * 0.5375), int(Config.WINDOW_HEIGHT*0.26))
startPosition = (random.randint(glassCenter[0] - tableDimensions[0] + Config.MARGIN_TOP, glassCenter[0] - Config.MARGIN_TOP), random.randint(glassCenter[1] - tableDimensions[1] + Config.MARGIN_LEFT, glassCenter[1] - Config.MARGIN_LEFT))

# Surfaces and sprites used in menu
startGameSurface = pygame.Surface((Config.WINDOW_WIDTH, int(Config.WINDOW_HEIGHT*0.6)))
startGameSurface.set_alpha(0)

# Surfaces and sprites used in game
tableSprite = pygame.transform.smoothscale(pygame.image.load("Sprites/Menu/popup.png"), ((tableDimensions[0]+Config.TABLE_MARGIN*2), (tableDimensions[1]+Config.TABLE_MARGIN*2))).convert_alpha()
backgroundSprite = pygame.transform.smoothscale(pygame.image.load("Sprites/Menu/bg.png"), (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)).convert_alpha()
menuSprite = pygame.transform.smoothscale(pygame.image.load("Sprites/Menu/mainmenu.png"), (int(Config.WINDOW_WIDTH*0.5), int(Config.WINDOW_HEIGHT*0.5))).convert_alpha()
selectorSprite = pygame.transform.smoothscale(pygame.image.load("Sprites/Menu/selector.png"), (int(Config.WINDOW_WIDTH*0.05), int(Config.WINDOW_WIDTH*0.05))).convert_alpha()
overlaySprite = pygame.transform.smoothscale(pygame.image.load("Sprites/overlay.png"), (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)).convert_alpha()

# Sounds used in game
clickSound = pygame.mixer.Sound("Sprites/Sounds/click.mp3")

# Variables used in menu
arrowTop = True
lastChangedByKey = False

move = Move(cells, startPosition, tableDimensions, windowSurface, tableSprite, glassCenter)
renderGameField()

while True:
    if mainMenu and not inPopup:
        windowSurface.blit(backgroundSprite, [0, 0])
        windowSurface.blit(menuSprite, [int(Config.WINDOW_WIDTH * 0.25), int(Config.WINDOW_HEIGHT * 0.25)])

        mouseOnTop = startGameSurface.get_rect().collidepoint(pygame.mouse.get_pos())
        if not lastChangedByKey:
            if mouseOnTop:
                arrowTop = True
            else:
                arrowTop = False
        if lastChangedByKey:
            if mouseOnTop and arrowTop:
                lastChangedByKey = False
            elif not mouseOnTop and not arrowTop:
                lastChangedByKey = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    arrowTop = True
                    lastChangedByKey = True
                if event.key == K_DOWN or event.key == ord('s'):
                    arrowTop = False
                    lastChangedByKey = True
                if event.key == K_RETURN:
                    if arrowTop:
                        clickSound.play()
                        inGame = True
                        mainMenu = False
                        firstGameCycle = True
                    else:
                        clickSound.play()
                        pygame.quit()
                        sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if arrowTop:
                    clickSound.play()
                    inGame = True
                    mainMenu = False
                    firstGameCycle = True
                else:
                    clickSound.play()
                    pygame.quit()
                    sys.exit()
        if arrowTop:
            windowSurface.blit(selectorSprite, positionUp)
        else:
            windowSurface.blit(selectorSprite, positionDown)
        windowSurface.blit(startGameSurface, (0, 0))
        pygame.display.update()
    elif inGame and not inPopup:
        if firstGameCycle:
            # Execute this code every time a new game is started
            windowSurface.fill(Config.BACKGROUND_COLOR)
            move.updatePositions()
            for c in cells:
                c.move((0, 0))

            move.startGame()

            windowSurface.blit(overlaySprite, [0, 0])
            inPopup = True
            firstGameCycle = False
            popup = Popup(Config.POPUP_CONTENT_FONT, Config.CELL_TEXT_COLOR_VALUE, int(Config.WINDOW_WIDTH * 0.6),
                          int(Config.WINDOW_HEIGHT * 0.7), Lang.WELCOME, Lang.CLICK_TO_START, Lang.WELCOME_HEADER,
                          Config.POPUP_HEADER_FONT)
            windowSurface.blit(popup.content, (int(Config.WINDOW_WIDTH * 0.22), int(Config.WINDOW_HEIGHT * 0.15)))
        elif game.isFinished():
            inPopup = True
            mainMenu = True
            inGame = False
            content = "Gefeliciteerd, je hebt binnen " + timer.getPlayTime() + " alle vervuilde cellen gevonden. Daarbij heb je "
            if int(game.getWrongAnswers()) == 1:
                content += game.getWrongAnswers() + " verkeerd antwoord gegeven."
            else:
                content += game.getWrongAnswers() + " verkeerde antwoorden gegeven."
            popup = Popup(Config.POPUP_CONTENT_FONT, Config.CELL_TEXT_COLOR_VALUE, int(Config.WINDOW_WIDTH * 0.4),
                          int(Config.WINDOW_HEIGHT * 0.4), content,
                          Lang.CLICK_TO_MENU, Lang.GAME_FINISHED, Config.POPUP_HEADER_FONT)
            windowSurface.blit(popup.content, (int(Config.WINDOW_WIDTH * 0.3), int(Config.WINDOW_HEIGHT * 0.3)))

            resetGame()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Detect the left mouse button going down event
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Calculate distance from the glass center to the mouse click position
                    x1, y1 = event.pos
                    x2, y2 = glassCenter
                    distance = math.hypot(x1 - x2, y1 - y2)
                    # If the distance is smaller than the the radius of the glass, consider it clicked
                    if distance < glassRadius:
                        for c in cells:
                            if c.onClick(event, overlaySprite):
                                clickSound.play()
                                inPopup = True
                                break
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    move.leftPressedDown()
                if event.key == K_RIGHT or event.key == ord('d'):
                    move.rightPressedDown()
                if event.key == K_UP or event.key == ord('w'):
                    move.upPressedDown()
                if event.key == K_DOWN or event.key == ord('s'):
                    move.downPressedDown()
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == ord('a'):
                    move.leftNotPressedDown()
                if event.key == K_RIGHT or event.key == ord('d'):
                    move.rightNotPressedDown()
                if event.key == K_UP or event.key == ord('w'):
                    move.upNotPressedDown()
                if event.key == K_DOWN or event.key == ord('s'):
                    move.downNotPressedDown()
        if not inPopup:
            windowSurface.fill(Config.BACKGROUND_COLOR)
            move.updatePositions()

            windowSurface.blit(overlaySprite, [0, 0])
            if timer.isPaused():
                timer.play()
            updateStats()

            pygame.display.update()
    elif inPopup:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                clickSound.play()
                inPopup = False
        pygame.display.update()