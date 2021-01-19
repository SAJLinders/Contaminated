import time
import Config

class Move:
    def __init__(self, cells, startingPosition, tableDimensions, windowSurface, background, centerPosition):
        self.cells = cells
        self.startingPosition = startingPosition
        self.backgroundPosition = startingPosition
        self.bottomRightCorner = (startingPosition[0] + tableDimensions[0] + Config.TABLE_MARGIN*2, startingPosition[1] + tableDimensions[1] +Config.TABLE_MARGIN*2)
        self.topLeftCorner = startingPosition
        self.tableDimensions = tableDimensions
        self.upPressed = False
        self.leftPressed = False
        self.downPressed = False
        self.rightPressed = False
        self.windowSurface = windowSurface
        self.background = background
        self.lastUpdated = time.time()
        self.centerPosition = centerPosition

    def startGame(self):
        self.lastUpdated = time.time()

    def updatePositions(self):
        # Calculate deltaSpeed
        deltaTime = time.time()-self.lastUpdated
        self.lastUpdated = time.time()
        speed = round(Config.PLAYER_SPEED*deltaTime, 3)

        # Calculate movement vector (x, y) based on deltaSpeed and keys pressed
        movement = (0, 0)
        if self.upPressed:
            movement = (movement[0], movement[1]+speed)
        if self.leftPressed:
            movement = (movement[0]+speed, movement[1] )
        if self.downPressed:
            movement = (movement[0], movement[1]-speed)
        if self.rightPressed:
            movement = (movement[0]-speed, movement[1])

        # Calculate new positions of table and restrict movement if neccesary
        if (self.bottomRightCorner[0] + movement[0] < self.centerPosition[0] and self.rightPressed) or \
           (self.topLeftCorner[0] + movement[0] > self.centerPosition[0] and self.leftPressed):
                movement = (0, movement[1])
        if (self.bottomRightCorner[1] + movement[1] < self.centerPosition[1] and self.downPressed) or \
           (self.topLeftCorner[1] + movement[1] > self.centerPosition[1] and self.upPressed):
                movement = (movement[0], 0)

        # Update corners of table based on restricted movement vector (x, y)
        self.bottomRightCorner = (self.bottomRightCorner[0] + movement[0], self.bottomRightCorner[1] + movement[1])
        self.topLeftCorner = (self.topLeftCorner[0] + movement[0], self.topLeftCorner[1] + movement[1])

        # Move background
        self.backgroundPosition = (self.backgroundPosition[0]+movement[0], self.backgroundPosition[1]+movement[1])
        self.windowSurface.blit(self.background, self.backgroundPosition)

        # Move all cells
        for c in self.cells:
            c.move(movement)

    # <editor-fold desc="Movement updaters">
    def upPressedDown(self):
        self.upPressed = True

    def upNotPressedDown(self):
        self.upPressed = False

    def leftPressedDown(self):
        self.leftPressed = True

    def leftNotPressedDown(self):
        self.leftPressed = False

    def downPressedDown(self):
        self.downPressed = True

    def downNotPressedDown(self):
        self.downPressed = False

    def rightPressedDown(self):
        self.rightPressed = True

    def rightNotPressedDown(self):
        self.rightPressed = False

    def stopMovement(self):
        self.upPressed = False
        self.leftPressed = False
        self.downPressed = False
        self.rightPressed = False
    # </editor-fold>