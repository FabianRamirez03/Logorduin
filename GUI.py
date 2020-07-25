import time
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
import DrawController
import compYacc
import sys
from PIL import Image
from PIL import ImageTk
import asyncio

# Constantes Graficas
xCanvas = 935
yCanvas = 500

xCanvasCenter = xCanvas / 2
yCanvasCenter = yCanvas / 2

xTurtle = xCanvas / 2
yTurtle = yCanvas / 2

xEscondite = 1
yEscondite = 1

skin_path = "Imagenes"
turtle_skin = "turtle.png"

colorsDict = [["blanco", "white"], ["azul", "blue"], ["marron", "brown"], ["cafe", "brown"],
              ["gris", "grey"], ["amarillo", "yellow"], ["negro", "black"], ["rojo", "red"], ["verde", "green"],
              ["cian", "cyan"]]

# Constantes logicas
file_path = ""
functionsList = []

global running, showingTurtle
running = False
escondida = False

compYacc.rumbo = 90


# ______________________________Funciones de la interfaz grafica_______________________________________

def doNothing():
    print("Test")


# Abre un archivo de texto en el codigo a compilar
def open_file():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    global file_path
    file_path = filename
    with open(filename, "r") as text_file:
        file_content = text_file.read()
        codeText.delete('1.0', END)
        codeText.insert(INSERT, file_content)


# En caso de que haya un archivo abierto, lo reescribe con la informacion en el texto del codigo
def save_file():
    if file_path != "":
        file_to_write = open(file_path, "w")
        file_to_write.write(codeText.get('1.0', END))
        file_to_write.close()
    else:
        saveAs_file()


def saveAs_file():
    file = asksaveasfile(mode="w", defaultextension=".txt")
    global file_path
    file_path = file.name
    if file is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(codeText.get('1.0', END))  # starts from `1.0`, not `0.0`
    file.write(text2save)
    file.close()  # `()` was missing.


def new_file():
    global file_path
    file_path = ""
    codeText.delete('1.0', END)


def Retroceder(distance):
    global xTurtle, yTurtle, escondida
    if not escondida:
        coords = retrocederAux(distance)
        xTurtle = coords[0]
        yTurtle = coords[1]
    else:
        pass


def retrocederAux(distance):
    return DrawController.avanza(turtle_canvas, turtleImage, distance, xTurtle,
                                 yTurtle, -1, xCoords, yCoords)


def Avanza(distance):
    global xTurtle, yTurtle, escondida
    if not escondida:
        coords = avanzaAux(distance)
        xTurtle = coords[0]
        yTurtle = coords[1]
    else:
        pass


def avanzaAux(distance):
    return DrawController.avanza(turtle_canvas, turtleImage, distance, xTurtle,
                                 yTurtle, 1, xCoords, yCoords)  # El numero final depende de la direccion
    # 1 para avanzar
    # -1 para retroceder


def Ponrumbo(grades):
    global turtle, escondida
    if not escondida:
        gradesToRotate = DrawController.setSeeingTo(grades)  # Cuanto me debo mover para llegar al destino
        path = skin_path + "/" + turtle_skin
        if grades == 90:
            turtle = PhotoImage(file=skin_path + "/" + turtle_skin)
            turtle_canvas.itemconfigure(turtleImage, image=turtle)
            turtle_canvas.update()
        elif gradesToRotate != 0:
            turtle = ImageTk.PhotoImage(image=Image.open(path).rotate(gradesToRotate))
            turtle_canvas.itemconfigure(turtleImage, image=turtle)
            turtle_canvas.update()
    else:
        pass


def ponpos(coords):
    global xTurtle, yTurtle, escondida
    if not escondida:
        turtle_canvas.move(turtleImage, -xTurtle, -yTurtle)
        xTurtle = coords[0]
        yTurtle = coords[1]
        turtle_canvas.move(turtleImage, xTurtle, yTurtle)
        xCoords.configure(text="X = " + str(xTurtle))
        yCoords.configure(text="Y = " + str(yTurtle))
        turtle_canvas.update()
    else:
        pass


def ponx(xCoord):
    global xTurtle, escondida
    if not escondida:
        turtle_canvas.move(turtleImage, -xTurtle, 0)
        xTurtle = xCoord
        turtle_canvas.move(turtleImage, xTurtle, 0)
        xCoords.configure(text="X = " + str(xTurtle))
        turtle_canvas.update()
    else:
        pass


def pony(yCoord):
    global escondida
    if not escondida:
        global yTurtle
        turtle_canvas.move(turtleImage, 0, -yTurtle)
        yTurtle = yCoord
        turtle_canvas.move(turtleImage, 0, yTurtle)
        yCoords.configure(text="Y = " + str(yTurtle))
        turtle_canvas.update()
    else:
        pass


def giraDerecha(grades):
    global escondida
    if not escondida:
        girarAux(DrawController.girar(grades, -1))
    else:
        pass


def giraIzquierda(grades):
    if not escondida:
        girarAux(DrawController.girar(grades, 1))
    else:
        pass


def girarAux(gradesToRotate):
    global turtle
    path = skin_path + "/" + turtle_skin
    turtle = ImageTk.PhotoImage(image=Image.open(path).rotate(gradesToRotate))
    turtle_canvas.itemconfigure(turtleImage, image=turtle)
    turtle_canvas.update()


def BajaLapiz():
    global escondida
    if not escondida:
        DrawController.setCanDraw(True)
    else:
        pass


def subeLapiz():
    global escondida
    if not escondida:
        DrawController.setCanDraw(False)
    else:
        pass


def rumbo():
    compYacc.rumbo = DrawController.seeingTo
    return DrawController.seeingTo


def cuadrado(lado):
    global escondida
    if not escondida:
        grades = DrawController.seeingTo
        cont = 0
        while cont < 4:
            Ponrumbo(grades + 90 * cont)
            Avanza(lado)
            cont = cont + 1
    else:
        pass


def ocultaTortuga():
    global xEscondite, yEscondite, xTurtle, yTurtle, escondida
    if not escondida:
        xEscondite = xTurtle
        yEscondite = yTurtle
        ponpos([2000, 2000])
        escondida = True
    else:
        pass


def apareceTortuga():
    global xEscondite, yEscondite, escondida
    if escondida:
        escondida = False
        ponpos([xEscondite, yEscondite])


def clean_canvas():
    global turtle_canvas, turtleImage
    turtle_canvas.delete("all")
    turtleImage = turtle_canvas.create_image(xTurtle, yTurtle, image=turtle)


def Compila():
    global functionsList, running
    numeroDelinea = 1
    reiniciar()
    if not running:
        running = True
        line_list = codeText.get('1.0', 'end').split('\n')
        for line in line_list:
            if line != "":
                try:
                    if numeroDelinea > 1 and not compYacc.Comentario:
                        compYacc.Error = "No hay Comentario en la primera linea"
                        break
                    compYacc.toDo = ""
                    compYacc.Entrada = line.replace("\n", "")
                    compYacc.parser.parse(compYacc.Entrada)
                    print(compYacc.variables)
                    if not compYacc.Funcion:
                        if isinstance(compYacc.toDo, str) and compYacc.toDo != "":
                            functionsList.append(compYacc.toDo)
                        elif isinstance(compYacc.toDo, list):
                            print(compYacc.toDo)
                            for i in compYacc.toDo:
                                if compYacc.toDo != "":
                                    functionsList.append(i)
                except Exception as e:
                    print(e)
                    print(compYacc.Error)
                    break
            if (compYacc.Error):

                print(compYacc.Error)
                break
            numeroDelinea = numeroDelinea + 1

        consoleText.config(state=NORMAL)
        consoleText.delete('1.0', END)
        if not compYacc.Error:
            consoleText.insert(INSERT, "Compilado correctamente")
        else:
            if compYacc.Comentario:
                consoleText.insert(INSERT, compYacc.Error + " en la linea número " + str(numeroDelinea))
            else:
                consoleText.insert(INSERT, compYacc.Error)
        consoleText.config(state=DISABLED)
        running = False
    else:
        print("Running Procces")


def Ejecuta():
    global functionsList, running
    Compila()
    if not compYacc.Error:
        for fuction in functionsList:
            if fuction is not None and fuction != "Logic" and fuction != "":
                eval(str(fuction))
    else:
        print("no se")

def reiniciar():
    global functionsList
    functionsList = []
    compYacc.reiniciar()
    clean_canvas()
    centro()
    Ponrumbo(90)
    subeLapiz()
    DrawController.color = "black"

def getColor(color):
    global colorsDict
    result = ""
    for i in colorsDict:
        if i[0] == color:
            result = i[1]
            break
    return result


def PonColorLapiz(color):
    colorIngles = getColor(color)
    DrawController.color = colorIngles


def centro():
    coords = [xCanvasCenter, yCanvasCenter]
    ponpos(coords)


def espera(seg):
    result = seg / 60
    time.sleep(result)
    print("listo")


# Logica de las skins___________________________________
def update_skin(name):
    global turtle
    global turtle_skin
    turtle_skin = name
    turtle = PhotoImage(file=skin_path + "/" + name)
    turtle_canvas.itemconfigure(turtleImage, image=turtle)
    turtle_canvas.update()


def defaultAux():
    update_skin("turtle.png")


def shrekAux():
    update_skin("shrek.png")


def pacManAux():
    update_skin("pacman.png")


def arrowAux():
    update_skin("arrow.png")


# ___________________________________-Aplicacion Grafica_____________________________________________

root = Tk()
root.title("Logorduin")
root.geometry("1200x650")
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="Archivo", menu=subMenu)
subMenu.add_command(label="Nuevo Archivo", command=new_file)
subMenu.add_command(label="Abrir Archivo", command=open_file)
subMenu.add_command(label="Guardar", command=save_file)
subMenu.add_command(label="Guardar como", command=saveAs_file)

canvasMenu = Menu(menu)
menu.add_cascade(label="Canvas", menu=canvasMenu)
canvasMenu.add_command(label="Limpiar", command=clean_canvas)

# Menu para cambiar la skin de la tortuga
viewMenu = Menu(menu)
menu.add_cascade(label="Vista", menu=viewMenu)
skinMenu = Menu(viewMenu)
viewMenu.add_cascade(label="Skin", menu=skinMenu)
skinMenu.add_command(label="Default", command=defaultAux)
skinMenu.add_command(label="Shrek", command=shrekAux)
skinMenu.add_command(label="Pacman", command=pacManAux)
skinMenu.add_command(label="Flecha", command=arrowAux)
# ________________________________________Frames para organizar los elementos

# Frame donde se digita el codigo
code_Frame = Frame(root, height=150, width=400, bg="white", bd=2)
code_Frame.pack(fill=Y, side="right")

# Frame que contiene el resto de la interfaz fuera del recuadro del cofigo
left_Frame = Frame(root, width=935, bg="white", borderwidth=2)
left_Frame.pack(fill="both", side="right")

# Frame que contiene el canvas donde la tortuga dibuja
turtle_Frame = Frame(left_Frame, width=935, height=500, bg="white", bd=2)
turtle_Frame.pack()

# Frame que inferior izquierdo
left_Botom_Frame = Frame(left_Frame, width=935, height=150, bg="white", bd=2)
left_Botom_Frame.pack(fill="both")

# Frame que contiene la consola
console_Frame = Frame(left_Botom_Frame, width=750, height=150, bg="white", bd=2)
console_Frame.pack(side=LEFT)

# Frame que contiene los botones
buttons_Frame = Frame(left_Botom_Frame, width=185, height=150, bg="white", bd=2)
buttons_Frame.pack(side=LEFT)

# _________________________Elementos de la interfaz__________________________________

# Text Area para el codigo
codeText = Text(code_Frame, width=30,
                height=41)  # En este caso, el largo y ancho es por letras, height 41 son 41 reglones

# ScrollbBar para navegar dentro del codigo
ScrollBar = Scrollbar(code_Frame)
ScrollBar.config(command=codeText.yview)
codeText.config(yscrollcommand=ScrollBar.set)
ScrollBar.pack(side=RIGHT, fill="y")
codeText.pack(fill="y")

# Canvas donde la tortuga dibujará
turtle_canvas = Canvas(turtle_Frame, width=xCanvas, height=yCanvas)
turtle_canvas.pack(fill="y")

# Imagen de la tortuga
turtle = PhotoImage(file=skin_path + "/" + turtle_skin)
turtleImage = turtle_canvas.create_image(xTurtle, yTurtle, image=turtle)

# Botones de compilacion y ejecución
compileButton = Button(buttons_Frame, text="Compilar", command=Compila)
compileButton.place(height=30, width=60, x=0, y=30)
executeButton = Button(buttons_Frame, text="Ejecutar", command=Ejecuta)
executeButton.place(height=30, width=60, x=0, y=75)

# Labels de las coordenadas
xCoords = Label(buttons_Frame, text="X = " + str(xTurtle), fg="black", bg="white")
yCoords = Label(buttons_Frame, text="Y = " + str(yTurtle), fg="black", bg="white")
xCoords.place(x=85, y=0)
yCoords.place(x=85, y=20)

# Text Area de la consola
consoleText = Text(console_Frame, width=93, height=9)
consoleText.insert(INSERT, "Hola, soy la Consola")
consoleText.config(state=DISABLED)

# ScrollBar de la consola
consoleBar = Scrollbar(console_Frame)
consoleBar.config(command=consoleText.yview)
codeText.config(yscrollcommand=consoleBar.set)
consoleBar.pack(side=RIGHT, fill="y")
consoleText.pack(fill="y")


# Pop up Window para obtener el nombre del archivo
def nameFileWindow():
    def caca():
        global file_path
        file_path = "caca.txt"
        window.destroy()

    window = Toplevel()
    window.wm_title("Window")
    l = Label(window, text="Input")
    l.grid(row=0, column=0)
    b = Button(window, text="Okay", command=caca)
    b.grid(row=1, column=0)


# Safe closure
def on_closing():
    if messagebox.askokcancel("Salir", "Seguros que quieres salir?"):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

# **********************************Compilador*********************************************************

# Build the lexer
import ply.lex as lex

lexer = lex.lex()
import ply.yacc as yacc

parser = yacc.yacc()
