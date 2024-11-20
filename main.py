import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk 
import serial 
import time
import threading

app=customtkinter.CTk()
app.geometry("1280x650")
app.columnconfigure(0,weight=1)
app.configure(fg_color="#0D1B2A")

try:
    arduino = serial.Serial(port="COM3", baudrate=9600, timeout=1)
    time.sleep(2)
except ValueError:
    arduino=None
    print("No se pudo Conectar a puerto")

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

tab_save_values=tab_principal.add("Mostrar Datos")
tab_save_values.columnconfigure(0,weight=1)
 
title=customtkinter.CTkLabel(tab_radar,
                             text="Radar de Velocidad",
                             font=("Impact",35),text_color="#fff")
title.grid(row=0,column=0,columnspan=3,pady=0)

#frame datos 
frame_data=customtkinter.CTkFrame(tab_radar,fg_color="#0D1B2A")
frame_data.grid(row=1, column=0, padx=20, pady=20,sticky="ew")
frame_data.grid_columnconfigure(0,weight=1)
frame_data.grid_rowconfigure(0,weight=1)

#frame grafica
frame_graph=customtkinter.CTkFrame(tab_radar,fg_color="#1B263B")
frame_graph.grid(row=1,column=1, columnspan=2, padx=10, pady=20,sticky="nsew")
frame_graph.grid_columnconfigure(0,weight=1)
frame_graph.grid_rowconfigure(0,weight=1)

fig, ax = plt.subplots()
ax.set_title("Distancia vs. Velocidad")
ax.set_xlabel("Distancia (cm)")
ax.set_ylabel("Velocidad (cm/s)")
ax.grid()

#Listas para guardar datos
distancias=[]
velocidades=[]
tiempos=[]
Aceleracion=[]

canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill="both", expand=True)

def leer_datos_arduino():
    while True:
        try:
            linea = arduino.readline().decode('utf-8', errors='ignore').strip()
            if linea and ',' in linea:
                datos = linea.split(',')  
                if len(datos) == 3: 
                    distancia = float(datos[0]) 
                    velocidad = float(datos[1])
                    tiempo=float(datos[2])
                       
                    # Agregar datos a las listas
                    distancias.append(distancia)
                    velocidades.append(velocidad)
                    tiempos.append(tiempo)

                    if len(distancias) > 100:
                        distancias.pop(0)
                        velocidades.pop(0)
                        
                    actualizar_grafica()
        except Exception as e:
            print(f"Error al leer datos: {e}")
        time.sleep(0.1)         
        
def actualizar_grafica():
    ax.clear() 
    ax.set_title("Distancia vs. Velocidad")
    ax.set_xlabel("Distancia (cm)")
    ax.set_ylabel("Velocidad (cm/s)")
    ax.grid()
    ax.plot(distancias, velocidades, marker="o", linestyle="-", color="red", label="Datos")
    ax.legend()
    canvas.draw()
    
hilo_arduino = threading.Thread(target=leer_datos_arduino, daemon=True)
hilo_arduino.start()

style_label_solution={
    "font":("Century Gothic",25,"bold"),
     "padx":10,
     "pady":5,
     "corner_radius":10,
     "width":300
}
data=["Tiempo(s)","Velocidad(cm/s)","Rango(cm)","Aceleración (cm/s²)"]
label_values=[]

#Creación de los labels para mostrar la solución
for i in range(4):
    data_title = customtkinter.CTkLabel(frame_data,text=f"{data[i]}",**style_label_solution,
                                     fg_color="#00a6fb",text_color="#000", )
    data_title.grid(row=i*2, column=0, padx=5,pady=10,sticky="w")
    values = customtkinter.CTkLabel(frame_data,text="",**style_label_solution,
                                     fg_color="#1B263B",text_color="#fff")
    values.grid(row=i*2+1, column=0, padx=5,pady=5,sticky="w")
    label_values.append(values)

def actualizar_datos():
    global distancias, velocidades
    label_values[0].configure(text=f"{tiempos[-1]} s")
    label_values[1].configure(text=f"{velocidades[-1]} cm/s")
    label_values[2].configure(text=f"{distancias[-1]} cm")
    
def actualizar():
    actualizar_datos()
    app.after(1000, actualizar)  

actualizar()

def fixed_map(option):
    """Función para solucionar los problemas para aplicar estilos a la tabla"""
    return [elm for elm in style.map('Treeview', query_opt=option)
           if elm[:2] != ('!disabled', '!selected')]
style = ttk.Style()

style.theme_use('default')

style.map('Treeview', foreground=fixed_map('foreground'),
          background=fixed_map('background'))

style.configure("Treeview",
                font=("Century Gothic",20),
                 background="#F8F9FA",
                fieldbackground="#E9ECEF",
                foreground="#343A40",
                rowheight=40)

style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 

style.configure("Treeview.Heading",
                font=("Century Gothic",20,"bold"),
                background="#00a6fb",
                foreground="#0D1B2A",
                relief="flat",
                padding=(10,10))

style.map("Treeview.Heading",
          background=[('active', '#0085c9')])

style.map("Treeview", background=[('selected', '#caf0f8')]) 
style.map("Treeview", foreground=[('selected', '#343A40')])  
 
historial_datos = []

def guardar_datos():
    dato = {"Distancia": distancias[-1], "Velocidad": velocidades[-1],"Tiempo":tiempos[-1]}
    historial_datos.append(dato)
    label_warning_converge.configure(text="Datos guardados correctamente", text_color="#00FF00")
    for item in tabla.get_children():
        tabla.delete(item)
    for dato in historial_datos:
        tabla.insert("", "end", values=(dato["Distancia"], dato["Velocidad"], dato["Tiempo"]))


label_warning_converge=customtkinter.CTkLabel(tab_radar,text="", 
                                              font=("Century Gothic",15,"bold"),corner_radius=4)
label_warning_converge.grid(row=2,column=0, pady=10,padx=10)


tabla = ttk.Treeview(tab_save_values, columns=("Distancia", "Velocidad","Tiempo"), show="headings",height=20)
tabla.heading("Distancia", text="Distancia (cm)")
tabla.heading("Velocidad", text="Velocidad (cm/s)")
tabla.heading("Tiempo", text="Tiempo(s)")
tabla.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Botón para actualizar la tabla con los datos guardados

button_solution=customtkinter.CTkButton(tab_radar,text="Guardar Valores",
                                     fg_color="#00a6fb",border_color="#0085c9",
                                     hover_color="#0085c9",border_width=3,corner_radius=50,
                                     font=("Century Gothic",15,"bold"),text_color="#000",command=guardar_datos)
button_solution.grid(row=3, columnspan=3,padx=10,ipady=5)

app.mainloop()

if arduino and arduino.is_open:
    arduino.close()