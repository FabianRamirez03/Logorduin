from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import sys
import Drawing

# Constantes Graficas
xCanvas = 935
yCanvas = 500

xCanvasCenter = xCanvas / 2
yCanvasCenter = yCanvas / 2

xTurtle = xCanvas / 2
yTurtle = yCanvas / 2

skin_path = "Imagenes"
turtle_skin = "pacman.png"

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

#En caso de que haya un archivo abierto, lo reescribe con la informacion en el texto del codigo
def save_file():
    if file_path != "":
        file_to_write = open(file_path, "w")
        file_to_write.write(codeText.get('1.0', END))
        file_to_write.close()
    else:
        messagebox.showerror(message="No hay archivo para guardar", title="Error")


def makeLine():
    Drawing.line(turtle_canvas)

def avanzaAux():
    Drawing.avanza(turtle_canvas, turtleImage, 100)


def clean_canvas():
    for i in Drawing.figuresLists:
        turtle_canvas.delete(i)



# Logica de las skins___________________________________
def update_skin(name):
    global turtle
    turtle = PhotoImage(file=skin_path + "/" + name)
    turtle_canvas.itemconfigure(turtleImage, image=turtle)
    turtle_canvas.update()



def shrekAux():
    update_skin("shrek.png")


def pacManAux():
    update_skin("pacman.png")


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
skinMenu.add_command(label="Shrek", command=shrekAux)
skinMenu.add_command(label="Pacman", command=pacManAux)
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
compileButton = Button(buttons_Frame, text="Compilar", command=avanzaAux)
compileButton.place(height=30, width=60, x=55, y=30)
executeButton = Button(buttons_Frame, text="Ejecutar", command=makeLine)
executeButton.place(height=30, width=60, x=55, y=75)

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

root.mainloop()
