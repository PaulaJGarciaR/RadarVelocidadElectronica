import customtkinter
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk 

app=customtkinter.CTk()
app.geometry("1280x650")
app.columnconfigure(0,weight=1)
app.configure(fg_color="#0D1B2A")

tab_principal=customtkinter.CTkTabview(app,width=780,text_color="#000",
                                       fg_color="#1B263B",segmented_button_fg_color="#f2f4f7",
                                       segmented_button_selected_color="#00a6fb",
                                       segmented_button_selected_hover_color="#0085c9",
                                       segmented_button_unselected_color="#778DA9",
                                       segmented_button_unselected_hover_color="#8ea0b8"
                                       )
tab_principal.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

tab_radar=tab_principal.add("Radar Velocidad")
tab_radar.columnconfigure(0,weight=0)
tab_radar.columnconfigure(1,weight=1)
tab_radar.columnconfigure(2,weight=1)
#tab_system_of_equations.rowconfigure(0,weight=1)
 
title=customtkinter.CTkLabel(tab_radar,
                             text="Radar de Velocidad",
                             font=("Impact",35),text_color="#fff")
title.grid(row=0,column=0,columnspan=3,pady=0)
#frame datos 
frame_data=customtkinter.CTkFrame(tab_radar,fg_color="#0D1B2A")
frame_data.grid(row=1, column=0, padx=20, pady=20,sticky="ew")
frame_data.grid_columnconfigure(0,weight=1)
frame_data.grid_rowconfigure(0,weight=1)

style_label_solution={
    "font":("Century Gothic",25,"bold"),
     "padx":10,
     "pady":5,
     "corner_radius":10,
     "width":300
}
data=["Tiempo(s)","Velocidad(cm/s)","Rango(cm)","Aceleración (cm/s²)"]
label_values=[]
range_cm=[0, 50, 100, 150, 200, 250]
speed=[random.randint(10, 50) for _ in range_cm]

#Creación de los labels para mostrar la solución
for i in range(4):
    data_title = customtkinter.CTkLabel(frame_data,text=f"{data[i]}",**style_label_solution,
                                     fg_color="#00a6fb",text_color="#000", )
    data_title.grid(row=i*2, column=0, padx=5,pady=10,sticky="w")
    values = customtkinter.CTkLabel(frame_data,text="",**style_label_solution,
                                     fg_color="#1B263B",text_color="#fff")
    values.grid(row=i*2+1, column=0, padx=5,pady=5,sticky="w")
    label_values.append(values)

#frame grafica
frame_graph=customtkinter.CTkFrame(tab_radar,fg_color="#1B263B")
frame_graph.grid(row=1,column=1, columnspan=2, padx=10, pady=20,sticky="nsew")
frame_graph.grid_columnconfigure(0,weight=1)
frame_graph.grid_rowconfigure(0,weight=1)

# Crear gráfica
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title('Distancia vs Velocidad')
ax.set_xlabel('Distancia (cm)')
ax.set_ylabel('Velocidad (cm/s)')
line, = ax.plot([], [], marker="o", color="b")

# Función para actualizar la gráfica y los labels
def actualizar_datos():
    global range_cm, speed
     #Generar nuevos valores aleatorios
    news_ranges = range_cm + [range_cm[-1] + 50]
    news_speeds =  speed + [random.randint(10, 50)]
    range_cm, speed = news_ranges, news_speeds
    # Actualizar la gráfica
    line.set_data(range_cm,speed)
    ax.relim()  # Recalcular límites
    ax.autoscale_view()  # Ajustar la vista
    canvas.draw()  # Redibujar la gráfica

    # Actualizar los labels con los últimos valores
    label_values[2].configure(text=f"{range_cm[-1]} cm")
    label_values[1].configure(text=f"{speed[-1]} cm/s")
    
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill="both", expand=True)

def actualizar():
    actualizar_datos()
    app.after(1000, actualizar)  # Llamar a la función cada 1 segundo (1000 ms)

# Iniciar el ciclo de actualización
actualizar()

def fixed_map(option):
    """Función para solucionar los problemas para aplicar estilos a la tabla"""
    return [elm for elm in style.map('Treeview', query_opt=option)
           if elm[:2] != ('!disabled', '!selected')]
style = ttk.Style()
#Definir un tema predeterminado
style.theme_use('default')
# Personalización (sobreescribe los estilos) de la tabla para el color de texto y fondo.
style.map('Treeview', foreground=fixed_map('foreground'),
          background=fixed_map('background'))
# Configuración los estilos para la tabla
style.configure("Treeview",
                font=("Century Gothic",20),
                 background="#F8F9FA",
                fieldbackground="#E9ECEF",
                foreground="#343A40",
                rowheight=40)

#Eliminación de los border de la tabla
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 

#Configuración de los estilos de los encabezados
style.configure("Treeview.Heading",
                font=("Century Gothic",20,"bold"),
                background="#00a6fb",
                foreground="#0D1B2A",
                relief="flat",
                padding=(10,10))

#Personalización de encabezados activos
style.map("Treeview.Heading",
          background=[('active', '#0085c9')])
#Personalización de filas seleccionadas
style.map("Treeview", background=[('selected', '#caf0f8')]) 
style.map("Treeview", foreground=[('selected', '#343A40')])  
 
# Lista para guardar los valores registrados
historial_datos = []

# Función para guardar y mostrar los datos
def guardar_datos():
    # Guardar el valor actual de velocidad y rango
    dato = {"Distancia": range_cm[-1], "Velocidad": speed[-1]}
    historial_datos.append(dato)
    label_warning_converge.configure(text="Datos guardados correctamente", text_color="#00FF00")
    for item in tabla.get_children():
        tabla.delete(item)
    # Agrega los datos del historial
    for dato in historial_datos:
        tabla.insert("", "end", values=(dato["Distancia"], dato["Velocidad"]))


label_warning_converge=customtkinter.CTkLabel(tab_radar,text="", 
                                              font=("Century Gothic",15,"bold"),corner_radius=4)
label_warning_converge.grid(row=2,column=0, pady=10,padx=10)

tab_save_values=tab_principal.add("Mostrar Datos")
tab_save_values.columnconfigure(0,weight=1)

tabla = ttk.Treeview(tab_save_values, columns=("Distancia", "Velocidad"), show="headings",height=20)
tabla.heading("Distancia", text="Distancia (cm)")
tabla.heading("Velocidad", text="Velocidad (cm/s)")
tabla.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Botón para actualizar la tabla con los datos guardados

button_solution=customtkinter.CTkButton(tab_radar,text="Guardar Valores",
                                     fg_color="#00a6fb",border_color="#0085c9",
                                     hover_color="#0085c9",border_width=3,corner_radius=50,
                                     font=("Century Gothic",15,"bold"),text_color="#000",command=guardar_datos)
button_solution.grid(row=3, columnspan=3,padx=10,ipady=5)

app.mainloop()