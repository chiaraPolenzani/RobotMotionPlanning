from shapely import Point

def draw_obstacles(grid):

    for obstacle in grid.obstacles:
        vertices = list(obstacle.exterior.coords) # vertici del poligono
        # Disegno il poligono sul canvas
        grid.canvas.create_polygon(vertices, outline="black", fill="black", width=1)
        
       
def draw_node(node):

    if node.rect is None:  # Se il nodo non è stato ancora disegnato
        node.rect = node.canvas.create_rectangle(
        node.x, node.y, node.x + node.size, node.y + node.size, fill="white", outline="black")


def change_node_color(node, color):

    if node.rect is not None:  
        node.canvas.itemconfig(node.rect, fill=color)
        

def draw_start_goal(grid, x_start, y_start, x_goal, y_goal):

    start = Point(x_start, y_start)
    goal = Point(x_goal, y_goal)
    # Calcola le posizioni nel canvas (la griglia assume che l'origine sia in alto a sinistra)
    draw_point(grid, start, "yellow", "S")
    draw_point(grid, goal, "Aquamarine", "G")
       

def draw_point(grid, point, color, label):

    # Trasformiamo le coordinate di Shapely in pixel sulla griglia
    col = int(point.x)
    row = int(point.y)

    # Disegna il cerchio centrato nella cella corrispondente
    x1 = col * grid.size + grid.size * 0.1  
    y1 = row * grid.size + grid.size * 0.1
    x2 = col * grid.size + grid.size * 0.9
    y2 = row * grid.size + grid.size * 0.9
    grid.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
    text_x = col * grid.size + grid.size * 0.5  # testo al centro della cella
    text_y = row * grid.size + grid.size * 0.5  
    grid.canvas.create_text(text_x, text_y, text=label, font=("Arial", 12, "bold"), fill="black")


def show_progress(grid):
    text = grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, fill="red", 
                                   font=("Arial", 40), text="Ricerca del percorso...")
    grid.canvas.after(2000, lambda: grid.canvas.delete(text))


def show_negative_result(grid):
    text = grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, fill="red", 
                                   font=("Arial Bold", 40), text="Percorso non trovato!!")
    grid.canvas.after(2500, lambda: grid.canvas.delete(text))


def show_positive_result(grid):
    grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, fill="red", 
                                   font=("Arial Bold", 40), text="Percorso trovato!!")
    
def show_final_result(grid):
    grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, fill="red", 
                                   font=("Arial Bold", 40), text="Risultato finale:\nPercorso non trovato!!")