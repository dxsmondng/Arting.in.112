from cmu_graphics import *

class Button:
    def __init__(self, app, x, y, width, height, text, r, g, b, active, mode):
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.r = r
        self.g = g
        self.b = b
        self.active = active
        self.mode = mode

    def draw(self, app):
        if self.active:
            drawRect(self.x, self.y, self.width, self.height, fill = rgb(self.r, self.g, self.b), border = 'white', borderWidth = 5)
            drawLabel(self.text, self.x + self.width // 2, self.y + self.height // 2, fill='black', bold = True)
        else:
            drawRect(self.x, self.y, self.width, self.height, fill = rgb(self.r, self.g, self.b))
            drawLabel(self.text, self.x + self.width // 2, self.y + self.height // 2, fill='black')         

    def isClicked(self, app, mX, mY):
        if self.x <= mX <= self.x + self.width and self.y <= mY <= self.y + self.height:
            return True
        else:
            return False

