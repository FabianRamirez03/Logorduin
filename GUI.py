from tkinter import *
import sys

# Constantes Graficas
xCanvas = 935
yCanvas = 500

xCanvasCenter = xCanvas / 2
yCanvasCenter = yCanvas / 2


def doNothing():
    print("Test")


root = Tk()
root.title("Logorduin")
root.geometry("1200x650")
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="Archivo", menu=subMenu)
subMenu.add_command(label="Nuevo Archivo", command=doNothing)
subMenu.add_command(label="Abrir Archivo", command=doNothing)
subMenu.add_command(label="Guardar", command=doNothing)
subMenu.add_separator()

editMenu = Menu(menu)
menu.add_cascade(label="Canvas", menu=editMenu)
editMenu.add_command(label="Limpiar", command=doNothing)

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

# ______________________________________________Elementos de la interfaz__________________________________

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
turtle = PhotoImage(file='Imagenes\shrek2.png')
turtle_canvas.create_image(xCanvasCenter, yCanvasCenter, image=turtle)

# Botones de compilacion y ejecución
compileButton = Button(buttons_Frame, text="Compilar")
compileButton.place(height=30, width=60, x=55, y=30)
executeButton = Button(buttons_Frame, text="Ejecutar")
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
