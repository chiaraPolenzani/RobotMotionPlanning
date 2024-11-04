import heapq    

def cammino_minimo_dijkstra(grid, start, goal, color):
    
    show_expansion = False # se messo a True colora i nodi che vengono visitati dall'algoritmo
    path_found = False
    start.distance = 0
    # heap queue algorithm
    node_list = []
    heapq.heappush(node_list, start)
            
    while node_list:
        current_node = heapq.heappop(node_list) # pop method returns the smallest item
        if current_node.visited:
            continue
        current_node.visited = True
        # Se ho raggiunto il nodo destinazione mi fermo e traccio il percorso
        if current_node == goal:
            return True
        
        near_nodes = get_near_nodes(grid, current_node) # nodi vicini al nodo corrente
        for near_node in near_nodes:
            if near_node.visited:
                continue
            if show_expansion:
                # colora i nodi visitati
                grid.canvas.create_rectangle(near_node.x, near_node.y, near_node.x + near_node.size, near_node.y + near_node.size, 
                                             fill=color, outline="black")
            
            # distanza del nuovo nodo dalla sorgente, passando per il nodo corrente
            new_distance = current_node.distance + near_node.size
            # Se troviamo un percorso più corto, aggiorniamo
            if new_distance < near_node.distance:
                near_node.distance = new_distance
                near_node.parent_node = current_node
                heapq.heappush(node_list, near_node) # aggiungo il nuovo nodo alla lista

    return path_found


def draw_path(grid, goal):
   
    n = goal
    center_coords = []  # Lista per memorizzare le coordinate dei centri dei nodi

    # Costruisco la lista di coordinate dal nodo goal fino al nodo di partenza
    while n.parent_node is not None:
        # Calcola il centro del nodo attuale
        center_x = n.x + n.size / 2
        center_y = n.y + n.size / 2 
        center_coords.append((center_x, center_y))
        
        n = n.parent_node

    # Aggiungo il centro del nodo iniziale
    center_x = n.x + n.size / 2 
    center_y = n.y + n.size / 2
    center_coords.append((center_x, center_y))
    
# Disegno la linea che collega i punti
    for i in range(len(center_coords) - 1):
        x1, y1 = center_coords[i] 
        x2, y2 = center_coords[i+1] 
        grid.canvas.create_line(x1, y1, x2, y2, fill = "red", width = 2) # freccia: arrow=tk.LAST


# metodo che restituisce i nodi vicini, quelli con le dimensioni di partenza
def get_big_nodes(grid, node):
    
    nodes = []
    x = node.x // grid.size
    y = node.y // grid.size

    if x < grid.cols - 1 and (grid.nodes[y][x + 1].state != "FULLY OCCUPIED"): # Destra
        nodes.append(grid.nodes[y][x + 1]) 

    if y < grid.rows - 1 and (grid.nodes[y + 1][x].state != "FULLY OCCUPIED"): # Sotto
        nodes.append(grid.nodes[y + 1][x])
 
    if x > 0 and (grid.nodes[y][x - 1].state != "FULLY OCCUPIED"): # Sinistra
        nodes.append(grid.nodes[y][x - 1]) 

    if y > 0 and (grid.nodes[y - 1][x].state != "FULLY OCCUPIED"): # Sopra
        nodes.append(grid.nodes[y - 1][x]) 

    return nodes


def get_top_parent(node):

    while node.parent:
        node = node.parent
    return node


# metodo per trovare tutte le foglie di un nodo
def get_leaves(node):

    if not node.sub_nodes:
        if node.state == "EMPTY": 
            return [node]  # Nodo è una foglia
    leaves = []
    for sub_node in node.sub_nodes:
        leaves += get_leaves(sub_node) # Ritorna tutte le foglie ricorsivamente
    return leaves
   

# metodo per trovare tutti i vicini di un nodo
def get_near_nodes(grid, node):

    near_nodes = []
    # aumento virtualmente le dimensioni del nodo
    new_node_polygon = node.expand_node(False)
    top_parent = get_top_parent(node) 

    array_big_nodes = get_big_nodes(grid, top_parent)
    array_big_nodes.append(top_parent)
    
    leaves = []
    for big_node in array_big_nodes: 
        leaves += get_leaves(big_node)

    for leaf in leaves:
        intersection = new_node_polygon.intersection(leaf.polygon)
        if ((leaf.x != node.x or leaf.y != node.y) and intersection.area > 0):
            near_nodes.append(leaf)

    return near_nodes






