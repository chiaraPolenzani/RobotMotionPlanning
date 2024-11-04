from shapely.geometry import Polygon
from draw import draw_node

class Nodo:
    def __init__(self, canvas, x, y, size, parent=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.parent = parent # Nodo che lo contiene, se è un sottonodo
        self.state = "EMPTY" # metto a OCCUPIED quando c'è intersezione con ostacolo
        self.rect = None
        self.visited = False
        self.parent_node = None
        self.distance = float('inf')  # distanza dal nodo sorgente, inizialmente infinita
        self.polygon = Polygon([(x, y), (x + size, y), (x + size, y + size), (x, y + size)]) # Poligono del nodo
        self.sub_nodes = [] 

    # Metodo per confrontare i nodi in base alla distanza
    def __lt__(self, other):
        return self.distance < other.distance
            

    def reset_node_properties(self): # per richiamare Dijkstra più volte

        self.visited = False
        self.parent_node = None
        self.distance = float('inf') 
        for node in self.sub_nodes:
            node.reset_node_properties()

    # Funzione per espandere virtualmente il nodo
    def expand_node(self, diagonally):

        if diagonally:
            new_x = self.x - 1
            new_y = self.y - 1
            new_size = self.size + 2 * 1
            return Polygon([(new_x, new_y), (new_x + new_size, new_y), (new_x + new_size, new_y + new_size), 
                            (new_x, new_y + new_size)])
        else:
            return Polygon([(self.x, self.y), (self.x, self.y - 1), (self.x + self.size, self.y - 1),
                            (self.x + self.size, self.y), (self.x + self.size + 1, self.y), 
                            (self.x + self.size + 1, self.y + self.size),(self.x + self.size, self.y + self.size), 
                            (self.x + self.size, self.y + self.size + 1),(self.x, self.y + self.size + 1), 
                            (self.x, self.y + self.size), (self.x - 1, self.y + self.size),(self.x - 1, self.y)])


    def split_node(self):

        if self.state == "PARTIALLY OCCUPIED" and not self.sub_nodes:
            self.create_subnodes() # Creo i 4 sotto-nodi
            return
        for n in self.sub_nodes:
            n.split_node()
            

    def create_subnodes(self):

        half_size = self.size // 2

        top_left = Nodo(self.canvas, self.x, self.y, half_size) 
        top_right = Nodo(self.canvas, self.x + half_size, self.y, half_size)
        bottom_right = Nodo(self.canvas, self.x + half_size, self.y + half_size, half_size)
        bottom_left = Nodo(self.canvas, self.x, self.y + half_size, half_size)

        self.sub_nodes = [top_left, top_right, bottom_right, bottom_left]
        
        for node in self.sub_nodes:
            node.parent = self
            draw_node(node)

