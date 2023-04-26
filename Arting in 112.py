#Name: Desmond Ng
#ID: dyng

from cmu_graphics import *
import math
from PIL import Image
from button import Button 

#Referenced Image Module from Pillow website and in-class demos on image manipulation
def onAppStart(app):
    #Make white canvas paramters
    app.imgWidth, app.imgHeight = 600, 750
    app.Wcanvas = Image.new('RGBA', (app.imgWidth, app.imgHeight), 'white')
    
    app.brushSize = 4
    app.oldX = None
    app.oldY = None
    app.newX = None
    app.newY = None
    app.dotLocation = None
    app.fillIns = set()

    #Buttons
    app.mainButtons = makeButtons(app)

    #Color
    app.blackVal = 0
    app.color = (0, 0, 0)

    #Initialize pixel
    initVal = 3
    app.size = initVal
    app.block = Image.new('RGBA', (app.size, app.size), app.color)
    app.oldCoor = []
    app.stepsPerSecond = 60
    app.mouseIsPressed = False
    app.userMode = "brush"

##### Referenced from https://github.com/olliearrison/112-project/blob/main/v1/main.py
##### to make code cleaner with buttons ########################################
def makeButtons(app):
    buttonList = []
    undo = Button(app, 50, 20, 40, 20, "Undo", 211, 211, 211, False, "undo")
    redo = Button(app, 150, 20, 40, 20, "Redo", 211, 211, 211, False, "redo")
    eraser = Button(app, 200, 20, 40, 20, "Eraser", 211, 211, 211, False, "eraser")
    red = Button(app, 50, 450, 70, 70, "Red", 255, 0, 0, False, "red")
    green = Button(app, 130, 450, 70, 70, "Green", 0, 255, 0, False, "green")
    blue = Button(app, 210, 450, 70, 70, "Blue", 0, 0, 255, False, "blue")
    purple = Button(app, 50, 550, 70, 70, "Purple", 160, 32, 240, False, "purple")
    yellow = Button(app, 130, 550, 70, 70, "Yellow", 255, 255, 0, False, "yellow")
    orange = Button(app, 210, 550, 70, 70, "Orange", 255, 165, 0, False, "orange")
    black = Button(app, 130, 650, 70, 70, "Black", 0, 0, 0, False, "black")
    buttonList.extend([undo, redo, eraser, red, green, blue, purple, yellow, orange, black])
    return buttonList

def drawButtons(app):
    for button in app.mainButtons:
        button.draw(app)

def checkButtonClicked(app, mX, mY):
    for button in app.mainButtons:
        if button.isClicked(app, mX, mY):
            changeMode(app, button.mode)
            return True

def changeMode(app, mode):
    app.userMode = mode
    for button in app.mainButtons:
        if button.mode == mode:
            button.active = True
        else:
            button.active = False
################################################################################

def eraserMode(app):
    if app.userMode == "eraser":
        app.color = (255, 255, 255)
def redMode(app):
    app.color = (255, 0, 0)
    changeMode(app, "red")

def greenMode(app):
    changeMode(app, "green")

def blueMode(app):
    changeMode(app, "blue")

def purpleMode(app):
    changeMode(app, "purple")

def yellowMode(app):
    changeMode(app, "yellow")

def orangeMode(app):
    changeMode(app, "orange")

def blackMode(app):
    changeMode(app, "black")

def drawBackground(app):
    drawRect(0, 0, app.width, app.height, fill = 'dimGray')

def distance(x0, y0, x1, y1):
    distance = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    return distance 

#Referenced Ollie Arrison's code from brush.py: https://github.com/olliearrison/112-project/blob/main/v1/brush.py
def addPixel(app, x, y):
    block = app.block
    app.Wcanvas.alpha_composite(block, dest=(int(x - app.width//3.5), int(y - app.height//10)))


def pixelMidPoints(app, x1, y1, x2, y2):
    maxDistance = min(app.brushSize//10, 20) + 1
    dist = distance(x1, y1, x2, y2)
    numPixels = int(dist/maxDistance) + 1
    dx = (x2- x1)/ numPixels
    dy = (y2- y1) / numPixels
    for i in range(numPixels):
        pX = int(x1 + dx * i)
        pY = int(y1 + dy * i)
        pixelCoor = (pX, pY)
        app.fillIns.add(pixelCoor)

def drawLine(app, x1, y1, x2, y2):
    addPixel(app, x2, y2)
    pixelMidPoints(app, x1, y1, x2, y2)
#################################################################################

def onKeyPress(app, key):
    if key == '+':
        app.size += 1
    elif key == '-' and app.size > 3:
        app.size -= 1
    if key == 'r':
        app.color = (255, 0, 0)  
    elif key == 'g':
        app.color = (0, 255, 0)
    elif key == 'b':
        app.color = (0, 0, 255)
    elif key == 'p':
        app.color = (160, 32, 240)
    elif key == 'y':
        app.color = (255, 255, 0)
    elif key == 'o':
        app.color = (255, 165, 0)
    elif key == 'B':
        app.color = (0, 0, 0)
    
    app.block = Image.new('RGBA', (app.size, app.size), app.color)

def onMousePress(app, mouseX, mouseY):
    if ((app.width//3.5 <= mouseX <= app.width//3.5 + app.imgWidth) and 
        (app.height//10 <= mouseY <= app.height//10 + app.imgHeight)):
        if len(app.oldCoor) == 0:
            app.oldCoor.append((mouseX, mouseY))
        else:
            app.oldCoor[-1] = (mouseX, mouseY)
        # check if the current pixel is inside the canvas's boundary
        app.dotLocation = (mouseX, mouseY)
        app.Wcanvas.alpha_composite(app.block, dest=(int(app.oldCoor[-1][0]-app.width//3.5), int(app.oldCoor[-1][1]-app.height//10)))
    checkButtonClicked(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    app.dotLocation = (mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    if ((app.width//3.5 <= mouseX <= app.width//3.5 + app.imgWidth) and 
        (app.height//10 <= mouseY <= app.height//10 + app.imgHeight)):
        if app.oldCoor == []:
            app.oldCoor.append((mouseX, mouseY))
            addPixel(app, mouseX, mouseY)
            # print(addPixel)
        else:
            app.oldX = app.oldCoor[-1][0]
            app.oldY = app.oldCoor[-1][1]
            app.newX = mouseX
            app.newY = mouseY
            drawLine(app, app.oldX, app.oldY, app.newX, app.newY)
            app.oldCoor[-1] = (app.newX, app.newY)
        app.dotLocation = (mouseX, mouseY)


def onMouseRelease(app, mouseX, mouseY):
    app.dotLocation = (mouseX, mouseY)
    app.oldCoor = []

# def onStep(app):
#     x, y = app.oldX, app.oldY
#     newX, newY = app.newX, app.newY
#     dx = abs(newX - x)
#     dy = abs(newY - y)
#     if dx >= 3 or dy >= 3:
#         addPixel(app, newX, newY)
#         print(addPixel(app, newX, newY))
#     newX, newY = app.oldX, app.oldY

def redrawAll(app):
    drawBackground(app)
    drawButtons(app)
    drawImage(CMUImage(app.Wcanvas), app.width//3.5, app.height//10)
    if app.dotLocation != None:
        cx, cy = app.dotLocation
        if ((app.width//3.5 <= cx <= app.width//3.5 + app.imgWidth) and 
        (app.height//10 <= cy <= app.height//10 + app.imgHeight)):
            drawCircle(cx, cy, app.brushSize, border='black', borderWidth = 1, fill = None)

    if app.oldCoor != []:
        x, y = app.oldCoor[-1][0], app.oldCoor[-1][1]
        drawImage(CMUImage(app.block), x, y)

    # app.Wcanvas.thumbnail((500, 500), resample = Resampling.LANCZOS)


    #Create buttons
    # app.undoButton.draw(app)
    # app.redoButton.draw(app)

runApp(width = 1440, height = 800)