import Util
import math

canDraw = False
seeingTo = 90  # hacia donde está viendo la tortuga en grados
xBound = 935
yBound = 500


def avanza(canvas, turtle, distance, xTurtle, yTurtle):
    distanceX = distance * math.cos(Util.gradesToRadians(seeingTo))  # Distancia total a mover en el eje X
    distanceY = distance * -math.sin(Util.gradesToRadians(seeingTo))  # Distancia total a mover en el eje Y

    directionX = distanceX / abs(distanceX)  # Para saber si debe restar o sumarle a la cantidad
    directionY = distanceY / abs(distanceY)

    traveledX = 0  # Distancia recorrida
    traveledY = 0

    if abs(distanceX) > abs(distanceY):  # En caso de que sea mayor el desplazamiento en X
        proportion = abs(distanceX) / abs(
            distanceY)  # cantidad de unidades que se debe mover X por unidad recorrida en Y
        if seeingTo == 360 or seeingTo == 180:  # Puede dar numeros por e-15, para que no haya division por cero
            proportion = 1
        while abs(traveledX) < abs(distanceX) and 15 < yTurtle < yBound - 15 and 15 < xTurtle < xBound - 15:
            traveledX = traveledX + directionX * proportion  # Define cuando se debe mover y se lo suma a la
            # distancia recorrida
            toMoveX = directionX * proportion
            toMoveY = 0  # Es cero de base en caso que no deba recorrer distancia en Y
            if abs(traveledY) < abs(distanceY):  # En caso de que deba seguirse moviendo en Y
                traveledY = traveledY + directionY
                toMoveY = directionY

            if canDraw:  # Dibuja la linea en caso de que el lapiz este bajo
                canvas.create_line(xTurtle, yTurtle, xTurtle + toMoveX, yTurtle + toMoveY)
            xTurtle = xTurtle + toMoveX
            yTurtle = yTurtle + toMoveY
            canvas.move(turtle, toMoveX, toMoveY)  # Mueve la figura
            canvas.update()  # Actualiza el canvas
            canvas.after(20)  # Define la velocidad del movimiento

    if abs(distanceX) < abs(distanceY):  # En caso de que sea mayor el desplazamiento en Y
        proportion = abs(distanceY) / abs(
            distanceX)  # cantidad de unidades que se debe mover X por unidad recorrida en Y
        if seeingTo == 90 or seeingTo == 270:  # Puede dar numeros por e-15, para que no haya division por cero
            proportion = 1
        while abs(traveledY) < abs(distanceY) and 15 < xTurtle < xBound - 15 and 15 < yTurtle < yBound - 15:
            traveledY = traveledY + directionY * proportion  # Define cuando se debe mover y se lo suma a la distancia recorrida
            toMoveY = directionY * proportion
            toMoveX = 0  # Es cero de base en caso que no deba recorrer distancia en Y
            if abs(traveledX) < abs(distanceX):  # En caso de que deba seguirse moviendo en Y
                traveledX = traveledX + directionX
                toMoveX = directionX

            if canDraw:
                canvas.create_line(xTurtle, yTurtle, xTurtle + toMoveX, yTurtle + toMoveY)
            xTurtle = xTurtle + toMoveX
            yTurtle = yTurtle + toMoveY
            canvas.move(turtle, toMoveX, toMoveY)  # Mueve la figura
            canvas.update()  # Actualiza el canvas
            canvas.after(20)  # Define la velocidad del movimiento
    return [xTurtle, yTurtle]

def setSeeingTo(grades):
    global seeingTo
    whereTo = grades - seeingTo
    seeingTo = grades
    if seeingTo == 0:
        seeingTo = 360
    if seeingTo > 360:
        seeingTo = seeingTo - 360
    print(seeingTo)
    return whereTo


def setCanDraw(state):
    global canDraw
    canDraw = state
