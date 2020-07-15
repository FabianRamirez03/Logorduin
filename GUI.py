from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import sys
import DrawController
from PIL import Image
from PIL import ImageTk

# Constantes Graficas
xCanvas = 935
yCanvas = 500

xCanvasCenter = xCanvas / 2
yCanvasCenter = yCanvas / 2

xTurtle = xCanvas / 2
yTurtle = yCanvas / 2

skin_path = "Imagenes"
turtle_skin = "turtle.png"

# Constantes logicas
file_path = ""


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
        messagebox.showerror(message="No hay archivo para guardar", title="Error")


def retroceder(distance):
    global xTurtle
    global yTurtle
    coords = retrocederAux(distance)
    xTurtle = coords[0]
    yTurtle = coords[1]


def retrocederAux(distance):
    return DrawController.avanza(turtle_canvas, turtleImage, distance, xTurtle,
                                 yTurtle, -1, xCoords, yCoords)


def avanza(distance):
    global xTurtle
    global yTurtle
    coords = avanzaAux(distance)
    xTurtle = coords[0]
    yTurtle = coords[1]


def avanzaAux(distance):
    return DrawController.avanza(turtle_canvas, turtleImage, distance, xTurtle,
                                 yTurtle, 1, xCoords, yCoords)  # El numero final depende de la direccion
    # 1 para avanzar
    # -1 para retroceder


def ponrumbo(grades):
    global turtle
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


def ponpos(coords):
    global xTurtle
    global yTurtle
    turtle_canvas.move(turtleImage, -xTurtle, -yTurtle)
    xTurtle = coords[0]
    yTurtle = coords[1]
    turtle_canvas.move(turtleImage, xTurtle, yTurtle)
    turtle_canvas.update()


def ponx(xCoord):
    global xTurtle
    turtle_canvas.move(turtleImage, -xTurtle, 0)
    xTurtle = xCoord
    turtle_canvas.move(turtleImage, xTurtle, 0)
    turtle_canvas.update()


def pony(yCoord):
    global yTurtle
    turtle_canvas.move(turtleImage, 0, -yTurtle)
    yTurtle = yCoord
    turtle_canvas.move(turtleImage, 0, yTurtle)
    turtle_canvas.update()


def giraDerecha(grades):
    girarAux(DrawController.girar(grades, -1))


def giraIzquierda(grades):
    girarAux(DrawController.girar(grades, 1))


def girarAux(gradesToRotate):
    global turtle
    path = skin_path + "/" + turtle_skin
    turtle = ImageTk.PhotoImage(image=Image.open(path).rotate(gradesToRotate))
    turtle_canvas.itemconfigure(turtleImage, image=turtle)
    turtle_canvas.update()


def bajaLapiz():
    DrawController.setCanDraw(True)


def subeLapiz():
    DrawController.setCanDraw(False)


def rumbo():
    return DrawController.seeingTo


def cuadrado(lado):
    grades = DrawController.seeingTo
    cont = 0
    while cont < 4:
        ponrumbo(grades + 90 * cont)
        avanza(lado)
        cont = cont + 1


def clean_canvas():
    for i in DrawController.figuresLists:
        turtle_canvas.delete(i)


def test():
    ponx(100)
    ponrumbo(270)
    avanza(500)


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
subMenu.add_command(label="Nuevo Archivo", command=doNothing)
subMenu.add_command(label="Abrir Archivo", command=open_file)
subMenu.add_command(label="Guardar", command=save_file)

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
compileButton = Button(buttons_Frame, text="Compilar")
compileButton.place(height=30, width=60, x=0, y=30)
executeButton = Button(buttons_Frame, text="Ejecutar", command=test)
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


# Safe closure
def on_closing():
    if messagebox.askokcancel("Salir", "Seguros que quieres salir?"):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
