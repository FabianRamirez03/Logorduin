import Util
import math

canDraw = False
seeingTo = 90  # hacia donde está viendo la tortuga en grados
xBound = 935
yBound = 500
color = "black"
outOfBounds = False
detener = False
speed = 20


def avanza(canvas, turtle, distance, xTurtle, yTurtle, direction, xLabel, yLabel):
    global detener, speed
    distanceX = distance * math.cos(Util.gradesToRadians(seeingTo))  # Distancia total a mover en el eje X
    distanceY = distance * -math.sin(Util.gradesToRadians(seeingTo))  # Distancia total a mover en el eje Y

    if distanceX != 0:
        directionX = distanceX / abs(distanceX)  # Para saber si debe restar o sumarle a la cantidad
    if distanceY != 0:
        directionY = distanceY / abs(distanceY)
    if distanceX == 0:
        directionX = 1
        distanceX = 0.1
    if distanceY == 0:
        distanceY = 0.1
        directionY = 0

    traveledX = 0  # Distancia recorrida
    traveledY = 0

    if abs(distanceX) > abs(distanceY):  # En caso de que sea mayor el desplazamiento en X
        proportion = 1
        if not abs(distanceY) < 1:
            proportion = abs(distanceX) / abs(
                distanceY)  # cantidad de unidades que se debe mover X por unidad recorrida en Y
        if seeingTo == 360 or seeingTo == 180:  # Puede dar numeros por e-15, para que no haya division por cero
            proportion = 1
            traveledY = 1
        while abs(traveledX) < abs(
                distanceX) and 15 < yTurtle < yBound - 15 and 15 < xTurtle < xBound - 15 and not detener:
            traveledX = traveledX + directionX * proportion  # Define cuando se debe mover y se lo suma a la
            # distancia recorrida
            toMoveX = directionX * proportion
            toMoveY = 0  # Es cero de base en caso que no deba recorrer distancia en Y
            if abs(traveledY) < abs(distanceY):  # En caso de que deba seguirse moviendo en Y
                traveledY = traveledY + directionY
                toMoveY = directionY

            if canDraw:  # Dibuja la linea en caso de que el lapiz este bajo
                canvas.create_line(xTurtle, yTurtle, xTurtle + toMoveX * direction, yTurtle + toMoveY * direction,
                                   fill=color)
            xTurtle = xTurtle + toMoveX * direction
            yTurtle = yTurtle + toMoveY * direction
            canvas.move(turtle, toMoveX * direction, toMoveY * direction)  # Mueve la figura
            xLabel.configure(text="X = " + str(int(xTurtle)))
            yLabel.configure(text="Y = " + str(int(yTurtle)))
            canvas.update()  # Actualiza el canvas
            canvas.after(speed)  # Define la velocidad del movimiento

    if abs(distanceX) < abs(distanceY):  # En caso de que sea mayor el desplazamiento en Y
        proportion = 1
        if not abs(distanceX) < 1:
            proportion = abs(distanceY) / abs(
                distanceX)  # cantidad de unidades que se debe mover X por unidad recorrida en Y
        if seeingTo == 90 or seeingTo == 270:  # Puede dar numeros por e-15, para que no haya division por cero
            proportion = 1
            traveledX = 1
        while abs(traveledY) < abs(
                distanceY) and 15 < xTurtle < xBound - 15 and 15 < yTurtle < yBound - 15 and not detener:
            traveledY = traveledY + directionY * proportion  # Define cuando se debe mover y se lo suma a la distancia recorrida
            toMoveY = directionY * proportion
            toMoveX = 0  # Es cero de base en caso que no deba recorrer distancia en Y
            if abs(traveledX) < abs(distanceX):  # En caso de que deba seguirse moviendo en Y
                traveledX = traveledX + directionX
                toMoveX = directionX

            if canDraw:
                canvas.create_line(xTurtle, yTurtle, xTurtle + toMoveX * direction, yTurtle + toMoveY * direction,
                                   fill=color)
            xTurtle = xTurtle + toMoveX * direction
            yTurtle = yTurtle + toMoveY * direction
            canvas.move(turtle, toMoveX * direction, toMoveY * direction)  # Mueve la figura
            xLabel.configure(text="X = " + str(int(xTurtle)))
            yLabel.configure(text="Y = " + str(int(yTurtle)))
            canvas.update()  # Actualiza el canvas
            canvas.after(speed)  # Define la velocidad del movimiento
    if yTurtle <= 15 or yTurtle >= 485 or xTurtle <= 15 or xTurtle >= 920:
        global outOfBounds
        outOfBounds = True
    return [xTurtle, yTurtle]


def setSeeingTo(grades):
    global seeingTo
    whereTo = grades - 90
    seeingTo = grades
    if seeingTo < 0:
        seeingTo +=360
    if seeingTo == 0:
        seeingTo = 360
    if seeingTo > 360:
        seeingTo = seeingTo - 360
    return whereTo


def girar(grades, direction):
    global seeingTo
    seeingTo = seeingTo + grades * direction
    if seeingTo < 0:
        seeingTo = seeingTo + 360
    if seeingTo > 360:
        seeingTo = seeingTo - 360
    return seeingTo


def setCanDraw(state):
    global canDraw
    canDraw = state
