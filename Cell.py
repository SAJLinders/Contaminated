import pygame
from pygame.locals import *
import Config

class Cell(object):
    def __init__(self, windowSurface, text, startingPosition, font, text_color, text_margin, bg_color, callback_function, msg, contaminated, x, y, isHeader=False):
        self.windowSurface = windowSurface
        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_margin = text_margin
        self.bg_color = bg_color
        self.contaminated = contaminated
        self.callback = callback_function
        self.played = False
        self.msg = msg
        self.position = startingPosition
        self.x = x
        self.y = y
        self.isHeader = isHeader
        self.contaminatedSpriteSize = int(Config.CELL_HEIGHT*0.6)
        if self.isHeader:
            self.contaminatedSpriteSize = int(Config.CELL_HEIGHT * 0.8)
        self.contaminatedSprite = pygame.transform.smoothscale(pygame.image.load("Sprites/Menu/selector.png"), (self.contaminatedSpriteSize, self.contaminatedSpriteSize)).convert_alpha()

        # If the word is too long, trim and and print a warning in the chat
        text_dimensions = self.font.size(self.text)
        if (text_dimensions[0] + self.text_margin) > Config.CELL_WIDTH:
            old = self.text
            self.text = self.trim(old)
            print("WARNING: Cell with text \"" + old + "\" exceeds maximum width of " + str(
                Config.CELL_WIDTH) + " pixels, actual width: " + str(
                text_dimensions[0] + self.text_margin) + " pixels, to prevent clipping the word has been trimmed to: " +
                self.text)

        # Render text in the center of the cell
        self.margin_top = ((Config.CELL_HEIGHT - text_dimensions[1]) / 2)
        self.textSurface = self.font.render(self.text, True, self.text_color)

    def onClick(self, event, overlay):
        green = (12, 114, 49)
        red = (255, 0, 0)
        # Check if a click event falls within this cells boundaries, calls the callback if this is the case
        if self.rect.collidepoint(event.pos):
            if not self.played:
                self.played = True
                if self.contaminated:
                    text_dimensions = self.font.size(self.text)
                    if (text_dimensions[0] + self.text_margin) > (Config.CELL_WIDTH - self.contaminatedSpriteSize - 5):
                        self.text = self.trim(self.text, Config.CELL_WIDTH - self.contaminatedSpriteSize - 5)
                    self.textSurface = self.font.render(self.text, True, green)

                else:
                    self.textSurface = self.font.render(self.text, True, red)
                self.move()
                self.windowSurface.blit(overlay, [0, 0])
                pygame.display.update()
                self.callback(self.msg, self.x, self.y)
                return True
        else:
            return False

    def move(self, movement = (0, 0)):
        self.position = (self.position[0]+movement[0], self.position[1]+movement[1])

        # Draw background of the cell first
        self.rect = pygame.draw.rect(self.windowSurface, self.bg_color, (self.position[0], self.position[1], Config.CELL_WIDTH, Config.CELL_HEIGHT))

        if self.played and self.contaminated:
            textPosition = ((self.position[0] + self.contaminatedSpriteSize + 5), (self.position[1] + 5))
            self.windowSurface.blit(self.contaminatedSprite, self.position)
            self.windowSurface.blit(self.textSurface, textPosition)
        else:
            textPosition = ((self.position[0] + 5), (self.position[1] + 5))
            self.windowSurface.blit(self.textSurface, textPosition)

    # Trim the word to the maximum permitted size
    def trim(self, word, width=Config.CELL_WIDTH):
        result = ""
        for letter in word:
            if (self.font.size(result + letter)[0] + self.text_margin) <= width:
                result += letter
            else:
                return result
