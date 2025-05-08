# PIA_Script.py
import tkinter as tk
from tkinter import messagebox
import random
from PIA_modulo import cargar_datos, obtener_info_local, mostrar_grafica_tipos

df_pokedex = cargar_datos()

def mostrar_pokemon(numero, text_widget, frame_imagenes):
    if not numero.isdigit():
        messagebox.showerror("Error", "Por favor, ingresa un número válido.")
        return
    info, imagenes = obtener_info_local(df_pokedex, numero)
    text_widget.config(state='normal')
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, f"(#{numero})\n\n{info}")
    text_widget.config(state='disabled')
    for widget in frame_imagenes.winfo_children():
        widget.destroy()
    for img in imagenes:
        etiqueta = tk.Label(frame_imagenes, image=img)
        etiqueta.image = img
        etiqueta.pack(side="left", padx=2)

def mostrar_pokemon_usuario():
    numero = entrada.get()
    mostrar_pokemon(numero, text_info1, frame_sprites1)

def mostrar_pokemon_random():
    numero_random = str(random.randint(1, 1010))
    mostrar_pokemon(numero_random, text_info2, frame_sprites2)

def graficar():
    mostrar_grafica_tipos(df_pokedex)

# Interfaz gráfica
ventana = tk.Tk()
ventana.bind('<Escape>', lambda e: ventana.destroy())
ventana.title("PokéDex PokeAPI Local")
ventana.geometry("1800x900")

frame_busqueda = tk.Frame(ventana)
frame_busqueda.pack(pady=10)
tk.Label(frame_busqueda, text="Número de Pokédex:").grid(row=0, column=0)
entrada = tk.Entry(frame_busqueda)
entrada.grid(row=0, column=1)
tk.Button(frame_busqueda, text="Buscar", command=mostrar_pokemon_usuario).grid(row=0, column=2, padx=10)
tk.Button(frame_busqueda, text="Random", command=mostrar_pokemon_random).grid(row=0, column=3)
tk.Button(frame_busqueda, text="Gráfica Tipos", command=graficar).grid(row=0, column=4, padx=10)

frame_p1 = tk.Frame(ventana, bd=2, relief="solid")
frame_p1.pack(side="left", padx=10, pady=10)
tk.Label(frame_p1, text="Tu Pokémon").pack()
scrollbar1 = tk.Scrollbar(frame_p1)
scrollbar1.pack(side="right", fill="y")
text_info1 = tk.Text(frame_p1, wrap="word", height=45, width=100, yscrollcommand=scrollbar1.set)
text_info1.pack(padx=5, pady=5)
text_info1.config(state="disabled")
scrollbar1.config(command=text_info1.yview)
frame_sprites1 = tk.Frame(frame_p1)
frame_sprites1.pack()

frame_p2 = tk.Frame(ventana, bd=2, relief="solid")
frame_p2.pack(side="right", padx=10, pady=10)
tk.Label(frame_p2, text="Pokémon Random").pack()
scrollbar2 = tk.Scrollbar(frame_p2)
scrollbar2.pack(side="right", fill="y")
text_info2 = tk.Text(frame_p2, wrap="word", height=45, width=100, yscrollcommand=scrollbar2.set)
text_info2.pack(padx=5, pady=5)
text_info2.config(state="disabled")
scrollbar2.config(command=text_info2.yview)
frame_sprites2 = tk.Frame(frame_p2)
frame_sprites2.pack()

ventana.mainloop()
