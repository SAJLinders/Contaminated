import pygame, sys
from pygame.locals import *

class Popup:
    def __init__(self, font, color, width, height, text, bottomText, headerText="", headerFont=None):
        self.font = font
        self.headerFont = headerFont
        self.content = pygame.transform.smoothscale(pygame.image.load("Sprites/Menu/popup.png"), (width, height))
        bottomText_dimensions = self.font.size(bottomText)
        self.content.blit(self.font.render(bottomText, True, color), (int(width*0.03), height-bottomText_dimensions[1]-int(height*0.08)))

        marginLeft = int(width*0.03)
        marginTop = int(height * 0.03)
        if headerFont != None and len(headerText)>0:
            marginTop = int(height*0.1)
            self.textSurface = self.headerFont.render(headerText, True, color)
            self.content.blit(self.textSurface, (marginLeft, marginTop))
            marginTop += self.headerFont.size(headerText)[1]*1.5
        else:
            marginTop = int(height * 0.1)

        for line in self.wrapText(text, int(width*0.9), int(height*0.8)):
            self.textSurface = self.font.render(line, True, color)
            self.content.blit(self.textSurface, (marginLeft, marginTop))
            marginTop += self.font.size(line)[1]

    def wrapText(self, text: str, maxWidth, maxHeight):
        # Get initial dimensions of the text, just in case it is very small or has already been fitted
        dimensions = self.font.size(text)

        # If the text already fits just go ahead and return it right away
        if dimensions[0] < maxWidth and dimensions[1] < maxHeight:
            return [text]
        else:
            result = []
            line = ""
            text.replace("\n", " ")
            for word in text.split(" "):
                wordDimensions = self.font.size(word)
                if wordDimensions[0] > maxWidth or wordDimensions[1] > maxHeight:
                    raise Exception("Popup is too small, can't even fit one word!: " + word)
                else:
                    if len(line) == 0:
                        line += word
                    else:
                        lineDimensions = self.font.size(line + " " + word)
                        if lineDimensions[0] > maxWidth or lineDimensions[1] > maxHeight:
                            result.append(line)
                            line = word
                        else:
                            line += " " + word
            result.append(line)
            return result
