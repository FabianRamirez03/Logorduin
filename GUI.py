import time
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
import DrawController
import compYacc
import re
from PIL import Image
from PIL import ImageTk

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

color = "black"

# Constantes logicas
file_path = ""
functionsList = []

global running, showingTurtle
running = False
escondida = False
detener = False

compYacc.rumbo = 90

nombreFunciones = ['Azar',
                   'Menos',
                   'Producto',
                   'Potencia',
                   'Division',
                   'Resto',
                   'Sen',
                   'Suma',
                   'Elegir',
                   'Cuenta',
                   'Ultimo',
                   'Elemento',
                   'Borrapantalla', 'Var',
                   'Inic',
                   'Inc',
                   'PonColorLapiz',
                   'Centro',
                   'Espera',
                   'Ejecuta',
                   'Repite',
                   'Si',
                   'Iguales',
                   'Y',
                   'O',
                   'MayorQue',
                   'MenorQue',
                   'Redondea',
                   'Cos',
                   'Diferencia',
                   'Avanza',
                   'Retrocede',
                   'GiraDerecha',
                   'GiraIzquierda',
                   'OcultaTortuga',
                   'ApareceTortuga',
                   'PonXY',
                   'PonRumbo',
                   'Rumbo',
                   'PonX',
                   'PonY',
                   'BajaLapiz',
                   'SubeLapiz',
                   'Coma',
                   'PuntoComa',
                   'Para',
                   'Fin']


# ______________________________Funciones de la interfaz grafica_______________________________________

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


def printConsola(string):
    consoleText.config(state=NORMAL)
    consoleText.insert(END, string + "\n")
    consoleText.config(state=DISABLED)


# ________________________________________________Funciones de la tortuga______________________________________________
def Retroceder(distance):
    global xTurtle, yTurtle, escondida
    if not escondida:
        coords = retrocederAux(distance)
        if DrawController.outOfBounds:
            compYacc.Error = "Movimiento fuera de los limites"
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
        if DrawController.outOfBounds:
            compYacc.Error = "Error: Movimiento fuera de los limites"
            printConsola(compYacc.Error)
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
            gradesLabel.config(text="Rumbo = " + str(int(DrawController.seeingTo)))
            turtle_canvas.update()
        elif gradesToRotate != 0:
            turtle = ImageTk.PhotoImage(image=Image.open(path).rotate(gradesToRotate))
            turtle_canvas.itemconfigure(turtleImage, image=turtle)
            gradesLabel.config(text="Rumbo = " + str(int(DrawController.seeingTo)))
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
        xCoords.configure(text="X = " + str(int(xTurtle)))
        yCoords.configure(text="Y = " + str(int(yTurtle)))
        turtle_canvas.update()
    else:
        pass


def ponx(xCoord):
    global xTurtle, escondida
    if not escondida:
        turtle_canvas.move(turtleImage, -xTurtle, 0)
        xTurtle = xCoord
        turtle_canvas.move(turtleImage, xTurtle, 0)
        xCoords.configure(text="X = " + str(int(xTurtle)))
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
        yCoords.configure(text="Y = " + str(int(yTurtle)))
        turtle_canvas.update()
    else:
        pass


def giraDerecha(grades):
    global escondida
    if not escondida:
        gradesToRotate = DrawController.seeingTo - grades
        Ponrumbo(gradesToRotate)
    else:
        pass


def giraIzquierda(grades):
    global escondida
    if not escondida:
        gradesToRotate = DrawController.seeingTo + grades
        Ponrumbo(gradesToRotate)
    else:
        pass


def girarAux(gradesToRotate):
    global turtle
    path = skin_path + "/" + turtle_skin
    DrawController.seeingTo = gradesToRotate
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


def colorComentarios(line_list):
    cont = 1.0
    codeText.tag_config('comentario', foreground="lime green")
    for line in line_list:
        if line[:2] == '//':
            length = len(line)
            codeText.tag_add("comentario", str(cont), str(cont) + "+" + str(length) + "c")
        else:
            pass
        cont += 1


def colorFunciones(line_list):
    global nombreFunciones
    codeText.tag_config('funcion', foreground="red")
    for funcion in nombreFunciones:
        cont = 1.0
        for line in line_list:
            if line[:2] == '//':
                cont += 1
                continue
            else:
                posicion = line.find(funcion)  # Donde se encontró la palabra
                if posicion != -1:  # Si se encontró
                    for word in re.finditer(funcion, line):
                        begin = str(cont) + "+" + str(word.start()) + "c"
                        end = str(cont) + "+" + str(word.end()) + "c"
                        codeText.tag_add("funcion", begin, end)
                    cont += 1
                    continue
                else:
                    cont += 1
                    continue


def Compila():
    global functionsList, running
    numeroDelinea = 1
    reiniciar()
    if not running:
        running = True
        line_list = codeText.get('1.0', 'end').split('\n')
        colorFunciones(line_list)
        colorComentarios(line_list)
        for line in line_list:
            if line != "":
                try:
                    compYacc.toDo = ""
                    compYacc.Entrada = line.replace("\n", "")
                    compYacc.parser.parse(compYacc.Entrada)
                    compYacc.Repite = True
                    print(compYacc.variables)
                    if not compYacc.Funcion:
                        if isinstance(compYacc.toDo, str) and compYacc.toDo != "":
                            functionsList.append(compYacc.toDo)
                        elif isinstance(compYacc.toDo, list):
                            for i in compYacc.toDo:
                                if compYacc.toDo != "":
                                    functionsList.append(i)
                except Exception as e:
                    print(e)
                    print(compYacc.Error)
                    if not compYacc.Error:
                        compYacc.Error = str(e)
                    break
            if compYacc.Error:
                print(compYacc.Error)
                break
            if numeroDelinea >= 1 and not compYacc.Comentario:
                compYacc.Error = "No hay Comentario en la primera linea\n"
                break
            numeroDelinea = numeroDelinea + 1
        consoleText.config(state=NORMAL)
        if not compYacc.variables and not compYacc.Error:
            compYacc.Error = "No hay ninguna variable definida\n"
        elif compYacc.Funcion and not compYacc.Error:
            consoleText.insert(END, "Error de sintaxis. Todo Para debe tener un fin.\n")
            compYacc.Error = "Error"
        elif not compYacc.Error:
            consoleText.insert(END, "Compilado correctamente\n")
        else:
            if compYacc.Comentario:
                consoleText.insert(END, "En la linea número " + str(numeroDelinea) + ": " + line + "\n")
                consoleText.insert(END, compYacc.Error + "\n")
            else:
                consoleText.insert(INSERT, compYacc.Error)
        consoleText.config(state=DISABLED)
        running = False
    else:
        printConsola("Ya se encuentra un proceso en marcha")


def Ejecuta():
    global functionsList, running, detener
    Compila()
    length = len(functionsList)
    i = 0
    if not running:
        while i < length and compYacc.Error == "" and not detener:
            function = functionsList[i]
            if function is not None and function != "Logic" and function != "":
                eval(str(function))
            i += 1
        running = False
    else:
        printConsola("Ya se encuentra un proceso en marcha")


def detenerEjecucion():
    global detener, running
    detener = True
    DrawController.detener = True
    reiniciar()
    if running:
        printConsola("Ejecución detenida con éxito")
    else:
        printConsola("No hay proceso para detener")


def reiniciar():
    global functionsList, detener, color
    functionsList = []
    apareceTortuga()
    DrawController.outOfBounds = False
    codeText.tag_remove("comentario", "1.0", 'end')
    reiniciarConsola()
    compYacc.reiniciar()
    clean_canvas()
    centro()
    Ponrumbo(90)
    detener = False
    DrawController.detener = False
    DrawController.seeingTo = 90
    subeLapiz()
    DrawController.color = color


def reiniciarConsola():
    consoleText.config(state=NORMAL)
    consoleText.delete('1.0', END)
    consoleText.insert(INSERT, "Logorduin. Version 1.0\n")
    consoleText.config(state=DISABLED)


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


def doritoAux():
    update_skin("dorito.png")


def pigAux():
    update_skin("pig.png")


def pencilAux():
    update_skin("lapiz.png")


# _________________________________Logica de la velocidad________________________________________

def defaultSpeed():
    DrawController.speed = 20


def slowSpeed():
    DrawController.speed = 30


def hightSpeed():
    DrawController.speed = 10


def toretto():
    DrawController.speed = 5


# ____________________________________Logica del cambio de fondo del canvas____________________________________

def changeBG(bg, fg):
    global color
    color = fg
    DrawController.color = fg
    turtle_canvas.config(bg=bg)
    xCoords.config(bg=bg, fg=fg)
    yCoords.config(bg=bg, fg=fg)
    gradesLabel.config(bg=bg, fg=fg)
    turtle_canvas.update()


def bgDefault():
    changeBG("gray63", "black")


def bgWhite():
    changeBG("white", "black")


def bgBlack():
    changeBG("black", "white")


def bgRed():
    changeBG("firebrick2", "black")


def bgGreen():
    changeBG("lime green", "black")


def bgPink():
    changeBG("deep pink", "black")


def bgPurple():
    changeBG("dark violet", "black")


def bgOrange():
    changeBG("DarkOrange1", "black")


# +____________________________________Logica del cambio de fondo del codigo____________________________________

def changeCodeColor(backGround, fontGround):
    codeText.config(bg=backGround, fg=fontGround)
    consoleText.config(bg=backGround, fg=fontGround)
    buttons_Frame.config(bg=backGround)
    console_Frame.config(bg=backGround)
    left_Botom_Frame.config(bg=backGround)
    left_Frame.config(bg=backGround)
    turtle_Frame.config(bg=backGround)
    code_Frame.config(bg=backGround)
    root.update()


def brightCode():
    changeCodeColor("white", "black")


def darkCode():
    changeCodeColor("gray17", "white")


# ___________________________________-Aplicacion Grafica_____________________________________________
root = Tk()

root.title("Logorduin")
icon = PhotoImage(file="Imagenes/turtle.png")
root.iconphoto(False, icon)

# root.geometry("1400x650")
root.geometry('%dx%d+%d+%d' % (1400, 650, 20, 20))
root.resizable(height=False, width=False)
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
skinMenu.add_command(label="Dorito", command=doritoAux)
skinMenu.add_command(label="Cerdo", command=pigAux)
skinMenu.add_command(label="Lapiz", command=pencilAux)

speedMenu = Menu(viewMenu)
viewMenu.add_cascade(label="Velocidad", menu=speedMenu)
speedMenu.add_command(label="Default", command=defaultSpeed)
speedMenu.add_command(label="Lento", command=slowSpeed)
speedMenu.add_command(label="Alto", command=hightSpeed)
speedMenu.add_command(label="Muy alto", command=toretto)

bgMenu = Menu(viewMenu)
canvasColorMenu = Menu(bgMenu)
viewMenu.add_cascade(label="Fondo", menu=bgMenu)
canvasColorMenu = Menu(bgMenu)
bgMenu.add_cascade(label="Canvas", menu=canvasColorMenu)
canvasColorMenu.add_command(label="Default", command=bgDefault)
canvasColorMenu.add_command(label="Blanco", command=bgWhite)
canvasColorMenu.add_command(label="Negro", command=bgBlack)
canvasColorMenu.add_command(label="Rojo", command=bgRed)
canvasColorMenu.add_command(label="Verde", command=bgGreen)
canvasColorMenu.add_command(label="Rosado", command=bgPink)
canvasColorMenu.add_command(label="Púrpura", command=bgPurple)
canvasColorMenu.add_command(label="Naranja", command=bgOrange)

codeColorBG = Menu(bgMenu)
bgMenu.add_cascade(label="Tema", menu=codeColorBG)
codeColorBG.add_command(label="Modo estandar", command=brightCode)
codeColorBG.add_command(label="Modo Oscuro", command=darkCode)
# ________________________________________Frames para organizar los elementos__________________

# Frame donde se digita el codigo
code_Frame = Frame(root, height=150, width=800, bg="white", bd=2)
code_Frame.pack(fill=Y, side="right")

# Frame que contiene el resto de la interfaz fuera del recuadro del codigo
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
codeText = Text(code_Frame, width=52,
                height=41, wrap=NONE)  # En este caso, el largo y ancho es por letras, height 41 son 41 reglones

# ScrollbBar para navegar dentro del codigo
ScrollBarY = Scrollbar(code_Frame)
ScrollBarX = Scrollbar(code_Frame, orient=HORIZONTAL)
ScrollBarY.config(command=codeText.yview)
ScrollBarX.config(command=codeText.xview)
codeText.config(yscrollcommand=ScrollBarY.set)
codeText.config(xscrollcommand=ScrollBarX.set)
ScrollBarY.pack(side=RIGHT, fill="y")
ScrollBarX.pack(side=BOTTOM, fill="x")
codeText.pack(fill=BOTH)

# Canvas donde la tortuga dibujará
turtle_canvas = Canvas(turtle_Frame, width=xCanvas, height=yCanvas, bg="gray63", bd=0, relief='ridge', borderwidth=0, highlightthickness=0)
turtle_canvas.pack(fill="y")

# Imagen de la tortuga
turtle = PhotoImage(file=skin_path + "/" + turtle_skin)
turtleImage = turtle_canvas.create_image(xTurtle, yTurtle, image=turtle)

# Botones de compilacion y ejecución
compilePhoto = PhotoImage(file="Imagenes/compilar.png")
executePhoto = PhotoImage(file="Imagenes/ejecutar.png")
stopPhote = PhotoImage(file="Imagenes/detener.png")

compileButton = Button(buttons_Frame, command=Compila, bg='white', image=compilePhoto, bd=0)
executeButton = Button(buttons_Frame, command=Ejecuta, bg='white', image=executePhoto, bd=0)
stopButton = Button(buttons_Frame, command=detenerEjecucion, bg='white', image=stopPhote, bd=0)

executeButton.place(x=47, y=10)
compileButton.place(x=47, y=45)
stopButton.place(x=47, y=80)

# Labels de las coordenadas
xCoords = Label(turtle_canvas, text="X = " + str(xTurtle), fg="black", bg="gray63")
yCoords = Label(turtle_canvas, text="Y = " + str(yTurtle), fg="black", bg="gray63")
xCoords.place(x=5, y=465)
yCoords.place(x=5, y=481)

# Labels del rumbo de la tortuga
gradesLabel = Label(turtle_canvas, text="Rumbo = " + str(DrawController.seeingTo), fg="black", bg="gray63")
gradesLabel.place(x=5, y=449)

# Text Area de la consola
consoleText = Text(console_Frame, width=93, height=9)
consoleText.insert(INSERT, "Logorduin. Version 1.0\n")
consoleText.config(state=DISABLED)

# ScrollBar de la consola
consoleBar = Scrollbar(console_Frame, bg="red")
consoleXBar = Scrollbar(console_Frame, orient=HORIZONTAL, bg="red")
consoleXBar.config(command=consoleText.xview)
consoleText.config(xscrollcommand=consoleXBar.set)
consoleBar.config(command=consoleText.yview)
codeText.config(yscrollcommand=consoleBar.set)
consoleBar.pack(side=RIGHT, fill="y")
consoleXBar.pack(side=BOTTOM, fill="x")
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
