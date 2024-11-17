import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time

# Crear ventana principal
root = ctk.CTk()
root.geometry("800x600")
root.title("Gráfica de Distancia y Velocidad")

# Variables globales para almacenar datos
distancias = [0, 50, 100, 150, 200, 250]
velocidades = [random.randint(10, 50) for _ in distancias]

# Crear frame para la gráfica
frame_grafica = ctk.CTkFrame(root)
frame_grafica.pack(pady=20, padx=20, fill="both", expand=True)

# Crear frame para los labels
frame_labels = ctk.CTkFrame(root)
frame_labels.pack(pady=10, padx=10, fill="x")

label_distancia = ctk.CTkLabel(frame_labels, text="Última Distancia: N/A", anchor="w")
label_distancia.pack(pady=5, padx=5, fill="x")

label_velocidad = ctk.CTkLabel(frame_labels, text="Última Velocidad: N/A", anchor="w")
label_velocidad.pack(pady=5, padx=5, fill="x")

# Crear gráfica
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title('Distancia vs Velocidad')
ax.set_xlabel('Distancia (cm)')
ax.set_ylabel('Velocidad (cm/s)')
line, = ax.plot([], [], marker="o", color="b")

# Función para actualizar la gráfica y los labels
def actualizar_datos():
    global distancias, velocidades

    # Generar nuevos valores aleatorios
    nuevas_distancias = distancias + [distancias[-1] + 50]
    nuevas_velocidades = velocidades + [random.randint(10, 50)]

    distancias, velocidades = nuevas_distancias, nuevas_velocidades

    # Actualizar la gráfica
    line.set_data(distancias, velocidades)
    ax.relim()  # Recalcular límites
    ax.autoscale_view()  # Ajustar la vista
    canvas.draw()  # Redibujar la gráfica

    # Actualizar los labels con los últimos valores
    label_distancia.configure(text=f"Última Distancia: {distancias[-1]} cm")
    label_velocidad.configure(text=f"Última Velocidad: {velocidades[-1]} cm/s")

# Crear el canvas de la gráfica
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Función para actualizar continuamente
def actualizar():
    actualizar_datos()
    root.after(1000, actualizar)  # Llamar a la función cada 1 segundo (1000 ms)

# Iniciar el ciclo de actualización
actualizar()

# Iniciar la interfaz
root.mainloop()
