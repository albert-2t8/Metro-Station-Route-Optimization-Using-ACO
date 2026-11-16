# -*- coding: utf-8 -*-
"""
Created on Wed May 28 17:49:56 2025

@author: alber
"""

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
import random
from collections import defaultdict

###############################################################################################################
############################## ZOOM A LA IMAGEN

class ZoomImagen:
    def __init__(self, root, ruta_imagen):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

    
        self.canvas = tk.Canvas(self.frame, width=600, height=600, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        
        self.scroll_x = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.grid(row=1, column=0, sticky="ew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        
        self.img = Image.open(ruta_imagen)
        self.zoom = 500 / max(self.img.width, self.img.height)
        self.puntos = {}  # Aquí guardamos los puntos
        self.actualizar_imagen()

        
        self.canvas.bind("<MouseWheel>", self.hacer_zoom_scroll)
        self.canvas.bind("<ButtonPress-1>", self.iniciar_arrastre)
        self.canvas.bind("<B1-Motion>", self.arrastrar)

    def actualizar_imagen(self):
        ancho = int(self.img.width * self.zoom)
        alto = int(self.img.height * self.zoom)
        img_zoom = self.img.resize((ancho, alto), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_zoom)

        self.canvas.delete("all")
        self.imagen_id = self.canvas.create_image(0, 0, image=self.tk_img, anchor=tk.NW)
        self.canvas.config(scrollregion=(0, 0, ancho, alto))

        self._redibujar_puntos()

    def hacer_zoom_scroll(self, event):
        if event.delta > 0 or event.num == 4:
            self.zoom *= 1.1
        elif event.delta < 0 or event.num == 5:
            self.zoom /= 1.1
        self.actualizar_imagen()

    def zoom_mas(self):
        self.zoom *= 1.1
        self.actualizar_imagen()

    def zoom_menos(self):
        self.zoom /= 1.1
        self.actualizar_imagen()

    def iniciar_arrastre(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def arrastrar(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def dibujar_puntos(self, puntos, mejor_camino_nombres, nod_bloq):
        self.puntos = puntos  
        self.mejor_camino_nombres= mejor_camino_nombres
        self.nod_bloq=nod_bloq
        self._redibujar_puntos()

    def _redibujar_puntos(self):
        if not self.puntos:
            return 
        
        self.canvas.delete("puntos")
        
        coincidencias = set(self.puntos.keys()) & set(self.mejor_camino_nombres)
        if coincidencias:
            for etiqueta in coincidencias:
                x, y = self.puntos[etiqueta]
                x_zoom = x * self.zoom
                y_zoom = y * self.zoom
                
                self.canvas.create_oval(x_zoom - 7, y_zoom - 7, x_zoom + 7, y_zoom + 7, fill='#0DFF05', outline='black', tags="puntos")
                
            x_bloq, y_bloq = self.puntos[self.nod_bloq]
            x_zoom_b = x_bloq * self.zoom
            y_zoom_b = y_bloq * self.zoom
            self.canvas.create_line(x_zoom_b - 7, y_zoom_b - 7, x_zoom_b + 7, y_zoom_b + 7, fill='#B90101', width=4, tags="puntos")
            self.canvas.create_line(x_zoom_b - 7, y_zoom_b + 7, x_zoom_b + 7, y_zoom_b - 7, fill='#B90101', width=4, tags="puntos")
            
                

####################################################################################################################
############################ Puntos de cada estación del mapa metro
puntos = {
    'El Rosario': (198, 315),
    'Instituto del Petróleo': (620, 416),
    'Deportivo 18 de Marzo': (766, 469),
    'Martín Carrera': (936, 466), 
    'La Raza': (684, 578),
    'Tacuba': (262, 670),
    'Consulado': (867, 714),
    'Guerrero': (618, 798),
    'Garibaldi/Lagunilla': (667, 806),
    'Morelos': (834, 844),
    'Oceanía': (1079, 799),
    'Hidalgo': (606, 860),
    'Bellas Artes': (657, 872),
    'Balderas': (590, 949),
    'Salto del Agua': (647, 954), 
    'Pino Suárez': (712, 960),
    'Candelaria': (821, 947),
    'San Lázaro': (861, 926),
    'Tacubaya': (287, 1154), 
    'Centro Médico': (540, 1121),
    'Chabacano': (692, 1106),
    'Jamaica': (807, 1101),
    'Pantitlán': (1190, 1051),
    'Santa Anita': (808, 1137),
    'Mixcoac': (273, 1375),
    'Zapata': (459, 1426),
    'Ermita': (633, 1502), 
    'Atlalilco': (940, 1555)
}

#######################################################################################################33
##################### Incicializar aco 

estaciones = {
    0: 'El Rosario', 1: 'Instituto del Petróleo', 2: 'Deportivo 18 de Marzo',
    3: 'Martín Carrera', 4: 'La Raza', 5: 'Tacuba', 6: 'Consulado', 7: 'Guerrero',
    8: 'Garibaldi/Lagunilla', 9: 'Morelos', 10: 'Oceanía', 11: 'Hidalgo',
    12: 'Bellas Artes', 13: 'Balderas', 14: 'Salto del Agua', 15: 'Pino Suárez',
    16: 'Candelaria', 17: 'San Lázaro', 18: 'Tacubaya', 19: 'Centro Médico',
    20: 'Chabacano', 21: 'Jamaica', 22: 'Pantitlán', 23: 'Santa Anita',
    24: 'Mixcoac', 25: 'Zapata', 26: 'Ermita', 27: 'Atlalilco'
}

nombre_a_numero = {v: k for k, v in estaciones.items()}

coordenadas = {
    0: (19.504337697945125, -99.2000578067338), 1: (19.48955293772144, -99.14558769328143),
    2: (19.485167187694017, -99.12492054075264), 3: (19.484930670878814, -99.10394308214848),
    4: (19.469509787606103, -99.13675234286538), 5: (19.459114038259585, -99.18758693957822),
    6: (19.455080481695273, -99.11345254628829), 7: (19.44466487395678, -99.145057189552),
    8: (19.443780339805496, -99.13849343558209), 9: (19.43975365217246, -99.11841443188034),
    10: (19.445034590934842, -99.08655880489536), 11: (19.43785178936796, -99.14571353188033),
    12: (19.436293984523143, -99.1416466509254), 13: (19.427017409192263, -99.14861304775997),
    14: (19.427120719478616, -99.14352399145558), 15: (19.42434619541662, -99.13289833563479),
    16: (19.429143651740635, -99.11908484352193), 17: (19.430379252163952, -99.11428364912729),
    18: (19.401724581495568, -99.187367347223670), 19: (19.406452674166367, -99.15487536441795),
    20: (19.40863154042804, -99.1330976588653), 21: (19.41075297851883, -99.12151489330645),
    22: (19.404703736203754, -99.03918048531392), 23: (19.404530836184964, -99.12086848346304),
    24: (19.371765446468288, -99.18793212214231), 25: (19.371134403689904, -99.16422947981401),
    26: (19.36109767265947, -99.14290747605953), 27: (19.352253151919342, -99.10616527187415)
}

estaciones_conectadas = [
    (0, 1), (0, 5), (1, 2), (1, 4), (2, 3), (2, 4), (3, 6),
    (4, 6), (4, 7), (5, 11), (5, 18), (6, 9), (6, 10), (7, 8),
    (7, 11), (8, 9), (8, 12), (9, 16), (9, 17), (10, 17), (10, 22),
    (11, 12), (11, 13), (12, 14), (12, 15), (13, 14), (13, 18),
    (13, 19), (14, 15), (14, 20), (15, 16), (15, 20), (16, 17),
    (16, 21), (17, 22), (18, 19), (18, 24), (19, 20), (19, 25),
    (20, 21), (20, 23), (20, 26), (21, 22), (21, 23), (23, 27),
    (24, 25), (25, 26), (26, 27)
]

conexiones_numeradas = {}
for a, b in estaciones_conectadas:
    dist = np.linalg.norm(np.array(coordenadas[a]) - np.array(coordenadas[b]))
    conexiones_numeradas[(a, b)] = dist
    conexiones_numeradas[(b, a)] = dist  

# Parámetros ACO
feromonas = {arista: 0.01 for arista in conexiones_numeradas}
rho = 0.9                
alpha = 1.5              
beta = 2                 
Q = 1                    
num_hormigas = 10
num_iteraciones = 100
eta = {arista: 1.0 / conexiones_numeradas[arista] for arista in conexiones_numeradas}


adjacency = defaultdict(list)
for (nodo1, nodo2) in conexiones_numeradas:
    adjacency[nodo1].append(nodo2)


# Función para seleccionar el siguiente nodo 
def seleccionar_siguiente(actual, visitados, nodo_bloqueado):
    vecinos = [n for n in adjacency[actual] 
               if n not in visitados and n!=nodo_bloqueado]
    if not vecinos:
        return None
    probabilidades = []
    for vecino in vecinos:
        arista = (actual, vecino)
        tau = feromonas[arista] ** alpha
        et = eta[arista] ** beta
        probabilidades.append(tau * et)
    total = sum(probabilidades)
    probabilidades = [p / total for p in probabilidades]
    return random.choices(vecinos, weights=probabilidades, k=1)[0]




##########################################################################################################
################################ Ventana principal

ventana = tk.Tk()
ventana.title("METRO CDMX")
ventana.geometry("770x750")
ventana.configure(bg="#FF6F00")
ventana.resizable(False, False) 


# Título
titulo = tk.Label(ventana, text="METRO CDMX", font=("Comic Sans Ms", 40, "bold"), bg="#FF6F00")
titulo.pack(pady=10)

#############################################################################################################
###################### Simbolo del metro

frame_izquierdo = tk.Frame(ventana, bg="#FF6F00")
frame_izquierdo.pack(side=tk.LEFT, padx=20)

imagen_simbolo = Image.open("simbolo_1.png")  
imagen_sim_redi = imagen_simbolo.resize((100, 100))
imagen_tk_1 = ImageTk.PhotoImage(imagen_sim_redi)

imagen1_label = tk.Label(frame_izquierdo, image=imagen_tk_1, bg="#9FFD61")
imagen1_label.pack(pady=10)


#############################################################################################################
###################### Seleccionar inicio y destino


lugar_label = tk.Label(frame_izquierdo, text="Inicio", font=("Comic Sans Ms", 11, "bold"), bg="#9FFD61")
lugar_label.pack()
lugar_combobox = ttk.Combobox(frame_izquierdo, values=list(estaciones.values()), font=("Comic Sans Ms", 8))
lugar_combobox.pack(pady=5)


destino_label = tk.Label(frame_izquierdo, text="Destino", font=("Comic Sans Ms", 11, "bold"), bg="#9FFD61")
destino_label.pack()
destino_combobox = ttk.Combobox(frame_izquierdo, values=list(estaciones.values()), font=("Comic Sans Ms", 8))
destino_combobox.pack(pady=5)

#############################################################################################################
###################### Mapa del metro
frame_derecho = tk.Frame(ventana, bg="#FF6F00")
frame_derecho.pack(side=tk.LEFT, padx=40)

cuadro_imagen = tk.Frame(frame_derecho, borderwidth=2, relief="groove", bg="#9FFD61")
cuadro_imagen.pack(pady=50)

zoom_widget = ZoomImagen(cuadro_imagen, "metro.jpg")




#############################################################################################################
################## Mejor ruta

ruta_label = tk.Label(frame_izquierdo, text="Mejor Ruta", font=("Comic Sans Ms", 11, "bold"), bg="#9FFD61")
ruta_label.pack()

ruta_frame = tk.Frame(frame_izquierdo)
ruta_frame.pack(pady=10)

ruta_resultado = tk.Text(ruta_frame, width=20, height=10, wrap="word", relief="groove", font=("Comic Sans MS", 8))
ruta_resultado.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(ruta_frame, command=ruta_resultado.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

ruta_resultado.config(yscrollcommand=scrollbar.set)



def calcular_ruta():

    inicio=lugar_combobox.get()
    destino=destino_combobox.get()
    
    origen_num = nombre_a_numero[inicio]  
    destino_num = nombre_a_numero[destino] 
    
    nodo_bloqueado = random.choice([n for n in range(len(estaciones)) if n not in (origen_num, destino_num)])

    
    mejor_camino_nums = None
    mejor_longitud = float('inf')

    for iter in range(num_iteraciones):
        caminos = []
        longitudes = []

        for _ in range(num_hormigas):
            actual = origen_num
            camino = [actual]
            visitados = set([actual])

            while actual != destino_num:
                siguiente = seleccionar_siguiente(actual, visitados, nodo_bloqueado)
                if siguiente is None:
                    break  
                camino.append(siguiente)
                visitados.add(siguiente)
                actual = siguiente

            if actual == destino_num:
                longitud = 0
                for i in range(len(camino) - 1):
                    arista = (camino[i], camino[i+1])
                    longitud += conexiones_numeradas[arista]

                caminos.append(camino)
                longitudes.append(longitud)

                if longitud < mejor_longitud:
                    mejor_longitud = longitud
                    mejor_camino_nums = camino

        for arista in feromonas:
            feromonas[arista] *= rho

        for camino, longitud in zip(caminos, longitudes):
            for i in range(len(camino) - 1):
                arista = (camino[i], camino[i+1])
                feromonas[arista] += Q / longitud

    if mejor_camino_nums is None:
        texto="Error: No existe ruta"
        ruta_resultado.delete(1.0, tk.END)  
        ruta_resultado.insert(tk.END, texto)
        
    mejor_camino_nombres = [estaciones[num] for num in mejor_camino_nums]
    
    long=f"Mejor ruta: ({(mejor_longitud*1000):.4f} m)"
    nod_bloq=estaciones[nodo_bloqueado]
    estacion_bloqueada=f"Estación bloqueada: {nod_bloq}"
    texto_ruta = long + "\n\n" + estacion_bloqueada + "\n\n" + " →\n".join(mejor_camino_nombres)
    ruta_resultado.delete(1.0, tk.END)  
    ruta_resultado.insert(tk.END, texto_ruta)  
    
    zoom_widget.dibujar_puntos(puntos, mejor_camino_nombres, nod_bloq)
    
    


################################################################################################################
################# Boton calcular ruta

boton_calcular = tk.Button(
    frame_izquierdo,
    text="Calcular Ruta",
    font=("Comic Sans Ms", 11, "bold"),
    bg="#9FFD61",
    fg="black",
    activebackground="#CC5600",
    relief="raised",
    padx=10,
    pady=5, 
    command=calcular_ruta
)
boton_calcular.pack(pady=5)


ventana.mainloop()