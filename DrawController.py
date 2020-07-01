import Util
import math
from tkinter import PhotoImage
from PIL import Image
from PIL import ImageTk


seeingTo = 260  # hacia donde está viendo la tortuga en grados
xBound = 935
yBound = 500


def avanza(canvas, turtle, distance):
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
        while abs(traveledX) < abs(distanceX):
            traveledX = traveledX + directionX * proportion  # Define cuando se debe mover y se lo suma a la
            # distancia recorrida
            toMoveX = directionX * proportion
            toMoveY = 0  # Es cero de base en caso que no deba recorrer distancia en Y
            if abs(traveledY) < abs(distanceY):  # En caso de que deba seguirse moviendo en Y
                traveledY = traveledY + directionY
                toMoveY = directionY
            canvas.move(turtle, toMoveX, toMoveY)  # Mueve la figura
            canvas.update()  # Actualiza el canvas
            canvas.after(20)  # Define la velocidad del movimiento

    if abs(distanceX) < abs(distanceY):  # En caso de que sea mayor el desplazamiento en Y
        proportion = abs(distanceY) / abs(
            distanceX)  # cantidad de unidades que se debe mover X por unidad recorrida en Y
        if seeingTo == 90 or seeingTo == 270:  # Puede dar numeros por e-15, para que no haya division por cero
            proportion = 1
        while abs(traveledY) < abs(distanceY):
            traveledY = traveledY + directionY * proportion  # Define cuando se debe mover y se lo suma a la distancia recorrida
            toMoveY = directionY * proportion
            toMoveX = 0  # Es cero de base en caso que no deba recorrer distancia en Y
            if abs(traveledX) < abs(distanceX):  # En caso de que deba seguirse moviendo en Y
                traveledX = traveledX + directionX
                toMoveX = directionX
            canvas.move(turtle, toMoveX, toMoveY)  # Mueve la figura
            canvas.update()  # Actualiza el canvas
            canvas.after(20)  # Define la velocidad del movimiento


def ImageRotated(path, grades):
    global seeingTo
    seeingTo = grades
    return PhotoImage(Image.open(path).rotate(grades))
