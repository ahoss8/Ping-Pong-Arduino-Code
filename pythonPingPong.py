from vpython import *
import serial
import os

arduinoData = serial.Serial("com3", 115200)   # processing arduino data at given baud rate

scene = canvas(width = 600, height = 600)
title = label(text = "WELCOME TO PYPONG", color=color.white, pos = vector(0, 10, 0), height = 50, font = "monospace", box = False)
scoreLabel = label(text = "SCORE: ", height = 30, box = False, pos = vector(0, -9, 1.5), visible = False)

score = 0
easyDifficulty = 0.025
mediumDifficulty = 0.05
hardDifficulty = 0.075

roomX = 12
roomY = 10
roomZ = 16
wallThickness = 0.5
wallColor = color.white
wallOpacity = 0.8
frontOpacity = 0.1

ballR = 0.5
ballColor = color.white

paddleL = 2.1
paddleH = 1.45
paddleW = wallThickness

# The following code initializes the visualizations for game
myFloor = box(size = vector(roomX, wallThickness, roomZ), pos = vector(0, -roomY / 2, 0), color = wallColor, opacity = wallOpacity)
myCeiling = box(size = vector(roomX, wallThickness, roomZ), pos = vector(0, roomY / 2, 0), color = wallColor, opacity = wallOpacity)
leftWall = box(size = vector(wallThickness, roomY, roomZ), pos = vector(-roomX / 2 + wallThickness / 2, 0, 0), color = wallColor, opacity = wallOpacity)
rightWall = box(size = vector(wallThickness, roomY, roomZ), pos = vector(roomX / 2 - wallThickness / 2, 0, 0), color = wallColor, opacity = wallOpacity)
backWall = box(size = vector(roomX, roomY, wallThickness), pos = vector(0, 0, -roomZ / 2), color = wallColor, opacity = wallOpacity)
frontWall = box(size = vector(roomX, roomY, wallThickness), pos = vector(0, 0, roomZ / 2), color = wallColor, opacity = frontOpacity)
ball = sphere(color = ballColor, radius = ballR)
myPaddle = box(color = color.white, size = vector(paddleL, paddleH, paddleW), pos = vector(0, 0, roomZ / 2), opacity = 0.5)

ballX = 0
deltaX = 0
ballY = 0
deltaY = 0
ballZ = 0
deltaZ = 0

# The following code configures and formats the widgets
scene.append_to_caption("\n")
wtext(text = "CHOOSE DIFFICULTY: ")
def difficulty(evt):
        global deltaX, deltaY, deltaZ
        if evt.index == 0:
            deltaX = easyDifficulty
            deltaY = easyDifficulty
            deltaZ = easyDifficulty
        elif evt.index == 1:
            deltaX = mediumDifficulty
            deltaY = mediumDifficulty
            deltaZ = mediumDifficulty          
        elif evt.index == 2:
            deltaX = hardDifficulty
            deltaY = hardDifficulty
            deltaZ = hardDifficulty

difficultyList = ['EASY', 'MEDIUM', 'HARD']
menu(choices=difficultyList, bind=difficulty)

scene.append_to_caption('   ')
wtext(text="CHOOSE BALL COLOR: ")

def ball_color(evt):
        global ball
        if evt.index == 0:
            ball.color = color.white
        elif evt.index == 1:
            ball.color = color.black        
        elif evt.index == 2:
            ball.color = color.red
        elif evt.index == 3:
            ball.color = color.blue
        elif evt.index == 4:
            ball.color = color.green

colorList = ['WHITE', 'BLACK', 'RED', 'BLUE', 'GREEN']
menu(choices=colorList, bind=ball_color)

scene.append_to_caption('\n\n')
wtext(text="ADJUST PADDLE OPACITY: ")
def paddle_opacity(x):
    paddleOp = x.value
    myPaddle.opacity = paddleOp

slider(bind = paddle_opacity, vertical = False, min = 0.5, max = 1)

play = False
gameOver = False

def reset_game():
    global ballX, ballY, ballZ, score, play, gameOver, lb, cont, finalScoreLabel
    ballX = 0
    ballY = 0
    ballZ = 0
    score = 0
    play = True
    gameOver = False
    lb.visible = False
    cont.visible = False
    finalScoreLabel.visible = False

def update_paddle():
    global paddleX, paddleY, myPaddle
    while arduinoData.inWaiting() == 0:
        pass
    dataPacket = arduinoData.readline()
    dataPacket = str(dataPacket, "utf-8")
    dataPacket.strip("\r\n")
    splitPacket = dataPacket.split(",")

    if len(splitPacket) < 3:
        return

    xDir = float(splitPacket[1])
    yDir = float(splitPacket[2])

    paddleX = (4.75 / 522) * xDir + 4.75 - (4859.25 / 522)
    paddleY = (-4 / 506) * yDir - 4 + (4092 / 506)
    myPaddle.pos = vector(paddleX, paddleY, roomZ / 2)

while True:
    if not play:
        cont = label(text = "CHOOSE DIFFICULTY & PRESS P TO PLAY", pos = vector(0, -9.5, 0), height = 25, box = False)
        while not play:
            update_paddle()
            keys = keysdown()   # Checks keyboard keys that are pressed
            if "p" in keys:
                play = True
                cont.visible = False
                scoreLabel.visible = True
                break
            elif "e" in keys:
                os._exit(0)

    rate(50)
    update_paddle()

    if gameOver:
        keys = keysdown()
        if "p" in keys:
            reset_game()
        elif "e" in keys:
            os._exit(0)
        continue
        
    ballX += deltaX
    ballY += deltaY
    ballZ += deltaZ
    
    if (ballX + ballR) > (roomX / 2 - wallThickness) or (ballX - ballR) < (-roomX / 2 + wallThickness):
        deltaX *= (-1)
        ballX += deltaX

    if (ballY + ballR) > (roomY / 2 - wallThickness / 2) or (ballY - ballR) < (-roomY / 2 + wallThickness / 2):
        deltaY *= (-1)
        ballY += deltaY

    if (ballZ - ballR) < (-roomZ / 2 + wallThickness / 2):
        deltaZ *= (-1)
        ballZ += deltaZ

    if (ballZ + ballR) >= (roomZ / 2 - wallThickness / 2):
        if (ballX > paddleX - paddleL / 2) and (ballX < paddleX + paddleL / 2) and (ballY > paddleY - paddleH / 2) and (ballY < paddleY + paddleH / 2):
            deltaZ *= (-1)
            ballZ += deltaZ
            score += 1
        else:
            lb = label(text = "GAME OVER!", pos = vector(0, 0.1, 0), height = 40, box = False)
            cont = label(text = "PRESS P TO PLAY AGAIN OR E TO EXIT", pos = vector(0, -1.4, 0), height = 20, box = False)
            scoreLabel.text = ""
            finalScoreLabel = label(text = "FINAL SCORE: " + str(score), pos = vector(0, -9, 1.5), height = 30, box = False)
            gameOver = True
            continue

    ball.pos = vector(ballX, ballY, ballZ)
    scoreLabel.text = "SCORE: " + str(score)
