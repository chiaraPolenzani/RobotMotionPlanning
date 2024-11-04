import random
import tkinter as tk
from nodo import Nodo
import PIL.ImageGrab as ImageGrab
from shapely.geometry import Polygon
from draw import draw_node, change_node_color

class Griglia:
    def __init__(self, master, rows, cols, x_start, y_start, x_goal, y_goal):
        # Ottieni le dimensioni dello schermo
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # Calcola la dimensione della cella in base al numero di righe e colonne
        margin_height = 100
        margin_width = 50
        grid_height = screen_height - margin_height
        grid_width = screen_width - margin_width
        cell_width = grid_width // cols
        cell_height = grid_height // rows
        cell_sizes = [2, 4, 8, 16, 32, 64, 128] # altrimenti errore nella grafica delle celle
        cell_size  = min(cell_width, cell_height)  # Prendi il minimo per evitare che una cella sia troppo grande
        valid_sizes = []
        for size in cell_sizes:
            if size <= cell_size:
                valid_sizes.append(size)
        cell_size = max(valid_sizes) # prendo il valore più grande tra quelli più piccoli di cell_size

        self.cols = cols
        self.rows = rows
        self.size = cell_size
        self.obstacles = []
        self.canvas = tk.Canvas(master, width = cols * cell_size, height = rows * cell_size) # Creazione di un Canvas
        # un Canvas è un widget che fornisce uno spazio per disegnare forme, immagini e altri oggetti grafici. 
        # utile quando si vuole creare interfacce grafiche interattive.
        self.canvas.pack() # inserisce il widget canvas nella finestra principale e lo rende visibile

        self.nodes = [] # viene creata una lista vuota di nodi
        for row in range(rows):
            element = []
            for col in range(cols):
                node = Nodo(self.canvas, col * cell_size, row * cell_size, cell_size)
                draw_node(node)
                element.append(node)
            self.nodes.append(element) # matrice bidimensionale, ogni elemento rappresenta un nodo della griglia. 
        
        self.start = self.nodes[int(y_start)][int(x_start)]
        self.goal = self.nodes[int(y_goal)][int(x_goal)]
        
        self.nodes_to_split = []
    
    # Funzione che controlla se c'è intersezione tra i nodi e gli ostacoli e modifica lo stato e il colore del nodo
    def node_intersection(self):

        def check_node_intersection(node, obstacle):
            intersection = node.polygon.intersection(obstacle)
            if not intersection.is_empty and node.state != "FULLY OCCUPIED":
                if intersection.area == (node.size) ** 2:  
                    node.state = "FULLY OCCUPIED"
                else:
                    node.state = "PARTIALLY OCCUPIED"
                    change_node_color(node, "gray")

        def check_sub_nodes(node, obstacle):
            if len(node.sub_nodes) == 0:
                check_node_intersection(node, obstacle)
                return
            for n in node.sub_nodes:
                check_sub_nodes(n, obstacle)

        for x in range(len(self.nodes)):  # righe
            for y in range(len(self.nodes[x])):  # colonne di quella riga
                for obstacle in self.obstacles:
                    check_sub_nodes(self.nodes[x][y], obstacle)


    def create_obstacle(self, num_vertices):

        # stabilisco una distanza minima e massima tra gli ultimi 2 vertici per ridimensionare la grandezza degli ostacoli
        min_distance = (self.size * 2)**2  
        max_distance = (self.size * 4)**2  
             
        points = []
        for _ in range(num_vertices):
            while True:
                x = random.uniform(0, self.cols * self.size)  # entro la griglia
                y = random.uniform(0, self.rows * self.size)
                if len(points) == 0:
                    # Se è il primo punto, accettalo direttamente
                    break
                else:
                    x_distance = (x - points[-1][0]) ** 2 # points[-1] restituisce l'ultimo elemento della lista
                    y_distance = (y - points[-1][1]) ** 2
                    total_distance = x_distance + y_distance
                    # Controlla se la distanza è accettabile
                    if min_distance <= total_distance <= max_distance:
                        break
            
            points.append((x, y))
        
        # Creo il poligono con i punti casuali
        polygon = Polygon(points)
        convex_hull = polygon.convex_hull

        intersect = False
        for obstacle in self.obstacles:
            if convex_hull.intersects(obstacle):
                intersect = True
                break  # Esci dal ciclo se c'è un'intersezione
        
        # il poligono non deve essere creato sopra lo start o il goal
        if (intersect == False and self.start.polygon.intersects(convex_hull) == False and self.goal.polygon.intersects(convex_hull) == False):
            self.obstacles.append(convex_hull)
            

    # la griglia diventa adattativa se il percorso non è stato trovato
    def split_nodes(self):

        for x in range (0, len(self.nodes)): 
            for y in range (0, len(self.nodes[x])):
                self.nodes[x][y].split_node()

   
    def reset_nodes_properties(self):
        
        for x in range (0, len(self.nodes)): 
            for y in range (0, len(self.nodes[x])):
                self.nodes[x][y].reset_node_properties()


    # utilizzo il Canvas di Tkinter per creare un'immagine e poi salvarla come file.  
    def save_grid_as_image(self, filename):

        # Forza l'aggiornamento del canvas
        self.canvas.update_idletasks()
        # Ottieni le coordinate del canvas
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        # Cattura la porzione dello schermo corrispondente al canvas e salva come PNG
        img = ImageGrab.grab((x, y, x1, y1))
        img.save(filename, 'png')