import customtkinter
import random
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import matplotlib.pyplot as plt


app=customtkinter.CTk()
app.geometry("1280x650")
app.columnconfigure(0,weight=1)
app.configure(fg_color="#0D1B2A")

#Frame contenedor de todos los elementos 
frame_container=customtkinter.CTkFrame(app,fg_color="#778DA9")
frame_container.grid(row=0, column=0, padx=30, pady=40,sticky="nsew")
frame_container.grid_columnconfigure(1,weight=1)
frame_container.grid_columnconfigure(2,weight=1)
frame_container.grid_rowconfigure(0,weight=1)

title=customtkinter.CTkLabel(frame_container,
                             text="Radar de Velocidad",
                             font=("Impact",40),text_color="#000")
title.grid(row=0,column=0,columnspan=3,pady=10)
#frame datos 
frame_data=customtkinter.CTkFrame(frame_container,
                                                 fg_color="#778DA9")
frame_data.grid(row=1, column=0, padx=20, pady=20,sticky="w")
frame_data.grid_columnconfigure(0,weight=1)
frame_data.grid_rowconfigure(0,weight=1)


style_label_solution={
    "text_color":"#000",
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
                                     fg_color="#e76f51" )
    data_title.grid(row=i*2, column=0, padx=5,pady=10,sticky="w")
    values = customtkinter.CTkLabel(frame_data,text="",**style_label_solution,
                                     fg_color="#acb7c3")
    values.grid(row=i*2+1, column=0, padx=5,pady=5,sticky="w")
    label_values.append(values)

#frame grafica
frame_graph=customtkinter.CTkFrame(frame_container,fg_color="#1B263B")
frame_graph.grid(row=1, columnspan=2,column=1, padx=20, pady=20,sticky="nsew")
frame_graph.grid_columnconfigure(0,weight=1)
frame_graph.grid_rowconfigure(0,weight=1)

# Crear gráfica
#fig, ax = plt.subplots(figsize=(6, 4))
#ax.set_title('Distancia vs Velocidad')
#ax.set_xlabel('Distancia (cm)')
#ax.set_ylabel('Velocidad (cm/s)')
#line, = ax.plot([], [], marker="o", color="b")

# Función para actualizar la gráfica y los labels
#def actualizar_datos():
    #global range_cm, speed
    # Generar nuevos valores aleatorios
    #news_ranges = range_cm + [range_cm[-1] + 50]
    #news_speeds =  speed + [random.randint(10, 50)]
    #range_cm, speed = news_ranges, news_speeds
    # Actualizar la gráfica
    #line.set_data(range_cm,speed)
    #ax.relim()  # Recalcular límites
    #ax.autoscale_view()  # Ajustar la vista
    #canvas.draw()  # Redibujar la gráfica

    # Actualizar los labels con los últimos valores
    #label_values[2].configure(text=f"{range_cm[-1]} cm")
    #label_values[1].configure(text=f"{speed[-1]} cm/s")
    
#canvas = FigureCanvasTkAgg(fig, master=frame_graph)
#canvas.get_tk_widget().pack(fill="both", expand=True)

#def actualizar():
    #actualizar_datos()
    #app.after(1000, actualizar)  # Llamar a la función cada 1 segundo (1000 ms)

# Iniciar el ciclo de actualización
#actualizar()

label_warning_converge=customtkinter.CTkLabel(frame_container,text="", 
                                              font=("Century Gothic",15,"bold"),corner_radius=4)
label_warning_converge.grid(row=2,column=0, pady=10,padx=10)

app.mainloop()