import os
import tkinter as tk
from tkinter import Tk, Button, Entry, Label, messagebox, PhotoImage
from tkinter import StringVar, Frame
import random

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

class Wordle(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.fila = 0
        self.verde = '#19C065'
        self.naranjado = '#E3B30E'
        self.gris = '#8F8E8C'
        self.texto = StringVar()
        self.texto.trace("w", lambda *args: self.limitar(self.texto))
        self.crer_widgets()
        self.palabra_aleatoria()

    def crer_widgets(self):
        self.frame_titulo = Frame(
            self.master, bg='pale green', width=900, height=300)
        self.frame_titulo.grid_propagate(0)
        self.frame_titulo.grid(column=0, row=0, sticky='nsew')
        self.frame_cuadros = Frame(
            self.master, bg='pale green', width=950, height=580)
        self.frame_cuadros.grid_propagate(0)
        self.frame_cuadros.pack_propagate(0)
        self.frame_cuadros.grid(column=0, row=1, sticky='nsew')

        self.contendor_cuadrados = Frame(
            self.frame_cuadros, bg="pale green", width=900, height=10)
        # self.contendor_cuadrados.propagate(0)
        self.contendor_cuadrados.pack_propagate(0)
        self.contendor_cuadrados.pack(side='top')

        self.frame_control = Frame(
            self.master, bg='pale green', width=400, height=10)
        self.frame_control.grid_propagate(0)
        self.frame_control.grid(column=0, row=2, sticky='nsew')

        Label(self.frame_titulo,  bg='pale green', fg='dark green', text='WORDLE',
              font=('Bauhaus 93', 25, 'bold')).pack(side='top')

        self.signal = Label(self.frame_control,  bg='pale green', fg='dark green', text=f'Ingrese una palabra de {difi} letras',
                            font=('Bahnschrift', 20))
        self.signal.pack(side='left', expand=True)

        self.palabra = Entry(self.frame_control, font=('Bahnschrift', 15), justify='center',
                             textvariable=self.texto, fg='black', highlightcolor="green2", highlightthickness=2, width=12)
        self.palabra.pack(side='left', expand=True)

        self.enviar = Button(self.frame_control, text='Enviar', bg='gray50', activebackground='green2',
                             fg='white', font=('Bahnschrift', 22, 'bold'), command=self.verificar_palabra)
        self.enviar.pack(side='left', expand=True)

        self.borrar = Button(self.frame_control, text='Borrar', bg='gray50', activebackground='green2',
                             fg='white', font=('Bahnschrift', 22, 'bold'), width=6, command=lambda: self.texto.set(''))
        self.borrar.pack(side='right', expand=True)

    # Aqui limito los caracteres que se pueden ingresar por consola, los cuales corresponden a la dificultad (cantidad de letras)
    def limitar(self, texto):
        if len(texto.get()) > 0:
            texto.set(texto.get()[:difi])

    def dibujar_cuadros_grises(self):
        for f in range(6):
            for j in range(difi):
                self.cuadros = Label(self.contendor_cuadrados, width=5, height=2, fg='white',
                                     bg=self.gris, font=('Geometr706 BlkCn BT', 25, 'bold'))
                self.cuadros.grid(column=j, row=f, padx=5, pady=5)
                self.cuadros['bg'] = self.gris

    # Esta funcion seria la que da inicio al juego

    def palabra_aleatoria(self):
        nombre_lemario = f'lemario{difi}'
        lemario_actual = lemarios.get(nombre_lemario, set())
        self.p_a = random.choice(list(lemario_actual))

    def verificar_palabra(self):
        palabra = self.texto.get().lower()
        nombre_lemario = f'lemario{difi}'

        # La complejidad de buscar un string contenido en el set es O(1)
        if palabra in lemarios[nombre_lemario] and len(palabra) == difi:
            self.signal['text'] = ''
            print(f"Palabra: {self.p_a}, Intento: {palabra}")
            if self.fila <= 6:
                for i, letra in enumerate(palabra):
                    self.cuadros = Label(self.contendor_cuadrados, width=5, height=2, fg='white',
                                         bg=self.gris, text=letra.upper(), font=('Geometr706 BlkCn BT', 25, 'bold'))
                    self.cuadros.grid(column=i, row=self.fila, padx=5, pady=5)
                    if letra == self.p_a[i]:
                        self.cuadros['bg'] = self.verde

                    if letra in self.p_a and letra != self.p_a[i]:
                        self.cuadros['bg'] = self.naranjado

                    if letra not in self.p_a:
                        self.cuadros['bg'] = self.gris

            self.fila = self.fila + 1
            if self.fila <= 6 and self.p_a == palabra:
                messagebox.showinfo(
                    'GANASTE', 'FELICIDADES ERES TODO UN GENIO')
                respuesta = tk.messagebox.askquestion(
                    "Wordle", "¿Quieres volver al inicio para seguir jugando?")
                self.master.destroy()
                self.master.quit()
                if respuesta == "yes":
                    dar_inicio()

            if self.fila == 6 and self.p_a != palabra:
                messagebox.showinfo('PERDISTE', 'INTENTALO DE NUEVO PERDEDOR')
                respuesta = tk.messagebox.askquestion(
                    "Wordle", "¿Quieres volver al inicio para seguir jugando?")
                self.master.destroy()
                self.master.quit()
                if respuesta == "yes":
                    dar_inicio()

        elif len(palabra) != difi:
            self.signal['text'] = f"La palabra debe contener {difi} letras"

        else:
            self.signal['text'] = 'Esta palabra no se encuentra en el lemario'


def crear_frame_inicio():
    global frame_inicio
    frame_inicio = tk.Frame(ventana)
    frame_inicio.pack(fill="both")
    frame_inicio.config(bg="pale green")

    etiqueta_wordle = tk.Label(frame_inicio, text="Wordle", font=(
        "Bauhaus 93", 100), bg="pale green", fg="dark green", padx=20, pady=20)
    etiqueta_wordle.pack()

    etiqueta_dificultad = tk.Label(
        frame_inicio, text="Elige la Dificultad de la Partida", bg="pale green", fg="red", font=("Bahnschrift", 46), padx=40, pady=40)
    etiqueta_dificultad.pack()

    frame_botones = tk.Frame(frame_inicio)
    frame_botones.pack()
    frame_botones.config(bg="pale green")

    boton_4_letras = tk.Button(
        frame_botones, text="4 letras", fg="red", font=("Bahnschrift", 30))
    boton_5_letras = tk.Button(
        frame_botones, text="5 letras", fg="red", font=("Bahnschrift", 30))
    boton_6_letras = tk.Button(
        frame_botones, text="6 letras", fg="red", font=("Bahnschrift", 30))
    boton_7_letras = tk.Button(
        frame_botones, text="7 letras", fg="red", font=("Bahnschrift", 30))
    boton_8_letras = tk.Button(
        frame_botones, text="8 letras", fg="red", font=("Bahnschrift", 30))

    boton_4_letras.grid(row=0, column=0, padx=5, pady=5)
    boton_5_letras.grid(row=0, column=1, padx=5, pady=5)
    boton_6_letras.grid(row=1, column=0, padx=5, pady=5)
    boton_7_letras.grid(row=1, column=1, padx=5, pady=5)
    boton_8_letras.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    boton_4_letras.bind("<Button-1>", lambda event,
                        dificultad=4: crear_frame_juego(dificultad))
    boton_5_letras.bind("<Button-1>", lambda event,
                        dificultad=5: crear_frame_juego(dificultad))
    boton_6_letras.bind("<Button-1>", lambda event,
                        dificultad=6: crear_frame_juego(dificultad))
    boton_7_letras.bind("<Button-1>", lambda event,
                        dificultad=7: crear_frame_juego(dificultad))
    boton_8_letras.bind("<Button-1>", lambda event,
                        dificultad=8: crear_frame_juego(dificultad))


def crear_frame_juego(dificultad):
    global difi
    difi = dificultad
    # print(difi)
    # Eliminar el frame de inicio
    frame_inicio.destroy()

    global root
    root = Wordle(ventana)
    root.dibujar_cuadros_grises()


def dar_inicio():
    global ventana
    ventana = Tk()
    ventana.config(bg='pale green')
    ventana.geometry('950x730')  # '950x750'
    ventana.resizable(0, 0)
    ventana.title('Wordle')

    crear_frame_inicio()

    ventana.mainloop()


def crear_lemario(nombre_archivo):
    lemario = set()

    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            palabra = linea.strip("\n")
            palabra = normalize(palabra)
            lemario.add(palabra)

    return lemario


# Crear un diccionario para almacenar los conjuntos
lemarios = {}

# Definir conjuntos para cada archivo
for i in range(4, 9):
    lemarios[f'lemario{i}'] = crear_lemario(os.path.join('lemarios', f'data{i}.txt'))


if __name__ == "__main__":
    dar_inicio()
