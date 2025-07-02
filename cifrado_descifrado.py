
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

import os
import sys

def ruta_recurso(nombre_archivo):
    """Devuelve la ruta absoluta al recurso para que funcione en .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    return os.path.join(os.path.abspath("."), nombre_archivo)


# 🎨 Configuración de estilo
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# 🎨 Paleta de colores personalizada
COLOR_PRINCIPAL = "#5D5FEF"
COLOR_HOVER = "#BBA734"
COLOR_ADVERTENCIA = "#E74C3C"

# 🌌 Crear ventana principal
ventana = ctk.CTk()
ventana.title("🔐 EcoCifrado")
ventana.geometry("760x740")
ventana.grid_columnconfigure((0, 1), weight=1)

# 🖼️ Logo + Identidad visual


try:
    ruta_logo = ruta_recurso("logo_2.png")

    logo_2 = ctk.CTkImage(dark_image=Image.open(ruta_logo), size=(140, 140))

    ctk.CTkLabel(ventana, image=logo_2, text="").grid(row=0, column=0, padx=16, pady=12, sticky="w")


    frame_titulo = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_titulo.grid(row=0, column=1, sticky="e", padx=10)

    ctk.CTkLabel(frame_titulo, text="EcoCifrado", font=("Segoe UI", 20, "bold")).pack()
    ctk.CTkLabel(frame_titulo, text="🧬 Recicla ideas. Protege tu información.", font=("Segoe UI", 12, "italic")).pack()
except Exception as e:
    print("⚠️ No se pudo cargar el logo:", e)


# 🔤 Alfabetos para cifrado
abc_min = "abcdefghijklmnñopqrstuvwxyz"
abc_may = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# 🔧 Funciones principales
def procesar_texto(texto, k, modo):
    resultado = ""
    for c in texto:
        if c in abc_min:
            pos = abc_min.index(c)
            nueva_pos = (pos + k if modo == "cifrar" else pos - k) % len(abc_min)
            resultado += abc_min[nueva_pos]
        elif c in abc_may:
            pos = abc_may.index(c)
            nueva_pos = (pos + k if modo == "cifrar" else pos - k) % len(abc_may)
            resultado += abc_may[nueva_pos]
        else:
            resultado += c
    return resultado

def aplicar_cifrado(modo):
    try:
        k = int(desplazamiento.get())
        texto = entrada.get("1.0", "end")
        resultado = procesar_texto(texto, k, modo)
        salida.delete("1.0", "end")
        salida.insert("end", resultado)
    except ValueError:
        messagebox.showerror("❌ Error", "El desplazamiento debe ser un número entero.")

def cifrar(): aplicar_cifrado("cifrar")
def descifrar(): aplicar_cifrado("descifrar")

def abrir_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            entrada.delete("1.0", "end")
            entrada.insert("end", f.read())

def guardar_archivo():
    texto = salida.get("1.0", "end")
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(texto.strip())
        messagebox.showinfo("✅ Guardado", "Archivo guardado correctamente.")

def copiar_resultado():
    texto = salida.get("1.0", "end").strip()
    ventana.clipboard_clear()
    ventana.clipboard_append(texto)
    ventana.update()

def limpiar_campos():
    entrada.delete("1.0", "end")
    salida.delete("1.0", "end")
    desplazamiento.delete(0, "end")

# ✨ Función para crear botones
def crear_boton(texto, comando, contenedor, fila, columna, color=COLOR_PRINCIPAL, hover=COLOR_HOVER):
    boton = ctk.CTkButton(
        contenedor,
        text=texto,
        command=comando,
        fg_color=color,
        hover_color=hover,
        text_color="#FFFFFF",
        border_color="#BDBDBD",
        border_width=2,
        corner_radius=8
    )
    boton.grid(row=fila, column=columna, padx=10, pady=10, sticky="ew")
    return boton

# 📝 Entrada de texto
ctk.CTkLabel(ventana, text="Texto:", font=("Segoe UI", 14)).grid(row=1, column=0, columnspan=2, pady=(10, 2))
entrada = ctk.CTkTextbox(ventana, height=150, width=500)
entrada.grid(row=2, column=0, columnspan=2, padx=20)

# 📁 Archivo + 🔢 Desplazamiento
ctk.CTkButton(ventana, text="📂 Abrir archivo", command=abrir_archivo).grid(row=3, column=0, pady=10)

frame_opciones = ctk.CTkFrame(ventana)
frame_opciones.grid(row=3, column=1, sticky="e", padx=10)
ctk.CTkLabel(frame_opciones, text="Desplazamiento:", font=("Segoe UI", 12)).pack(side="left", padx=6)
desplazamiento = ctk.CTkEntry(frame_opciones, width=60)
desplazamiento.pack(side="left", padx=6)

# 🔐 Botones de cifrado
frame_botones = ctk.CTkFrame(ventana)
frame_botones.grid(row=4, column=0, columnspan=2)
crear_boton("🔐 Cifrar", cifrar, frame_botones, fila=0, columna=0)
crear_boton("🔓 Descifrar", descifrar, frame_botones, fila=0, columna=1)

# 📤 Resultado
ctk.CTkLabel(ventana, text="Resultado:", font=("Segoe UI", 14)).grid(row=5, column=0, columnspan=2, pady=10)
salida = ctk.CTkTextbox(ventana, height=150, width=500)
salida.grid(row=6, column=0, columnspan=2, padx=20)

# 🛠️ Acciones finales
frame_acciones = ctk.CTkFrame(ventana)
frame_acciones.grid(row=7, column=0, columnspan=2, pady=20)

ctk.CTkButton(frame_acciones, text="📄 Copiar", command=copiar_resultado).pack(side="left", padx=10)
ctk.CTkButton(frame_acciones, text="🧹 Limpiar", command=limpiar_campos).pack(side="left", padx=10)
ctk.CTkButton(frame_acciones, text="💾 Guardar", command=guardar_archivo).pack(side="left", padx=10)

# 🟢 Ejecutar interfaz
ventana.mainloop()





