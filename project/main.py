import random
import tkinter as tk
from tkinter import *
from griglia import Griglia
from dialogWindowCoordinate import dialogWindowCoordinate 
from camminoMinimoDijkstra import cammino_minimo_dijkstra, draw_path
from draw import draw_obstacles, draw_start_goal, show_progress, show_negative_result, show_positive_result, show_final_result

root = tk.Tk()
root.title("Occupancy grid")

def main():
    
    # Crea una finestra di dialogo per raccogliere le info dall'utente
    dialogWindow = dialogWindowCoordinate(root)
    rows = dialogWindow.rows 
    cols = dialogWindow.cols 
    x_start = dialogWindow.x_start
    y_start = dialogWindow.y_start
    x_goal = dialogWindow.x_goal
    y_goal = dialogWindow.y_goal

    # creo l'oggetto griglia 
    grid = Griglia(root, rows = rows, cols = cols, x_start = x_start, y_start = y_start , x_goal = x_goal, y_goal = y_goal) 
    
    max_split = 3
    current_split = 0
    num_obstacles =  dialogWindow.num_obstacles
    min_vertices = 3
    max_vertices = 5

    while len(grid.obstacles) < num_obstacles:
        grid.create_obstacle(num_vertices=random.randint(min_vertices, max_vertices))
    draw_obstacles(grid)
    draw_start_goal(grid, x_start, y_start, x_goal, y_goal)
    grid.node_intersection()
    
    color = "green" # colore dei nodi visitati dall'algoritmo di Dijkstra
    result = cammino_minimo_dijkstra(grid, grid.start, grid.goal, color)
    root.after(1500, lambda: show_progress(grid))
        
    if not result:
        root.after(4000, lambda: show_negative_result(grid))
    
    def step():
        nonlocal current_split, result
        if result: 
            draw_path(grid, grid.goal)
            draw_start_goal(grid, x_start, y_start, x_goal, y_goal)
            root.after(2000, lambda: show_positive_result(grid))
            
            return  # esce dalla ricorsione

        grid.split_nodes()
        current_split += 1
        print(f"Split #{current_split}")
        draw_obstacles(grid)
        grid.node_intersection()
        grid.reset_nodes_properties()
        root.after(1000, lambda: draw_result())

    def draw_result():
        nonlocal result
        result = cammino_minimo_dijkstra(grid, grid.start, grid.goal, color)
        root.after(1000, lambda: show_progress(grid))
        if result:  # Se il cammino è stato trovato, mostra il risultato e ferma la ricorsione
            root.after(3000, lambda: draw_path(grid, grid.goal))
            root.after(3000, lambda: draw_start_goal(grid, x_start, y_start, x_goal, y_goal))
            root.after(4500, lambda: show_positive_result(grid))
        else:
            # Se non trovato, continua la ricorsione se non è stato raggiunto il max_split
            if current_split < max_split:
                root.after(4000, lambda: show_negative_result(grid))  # Mostra il risultato temporaneo
                root.after(6500, step)  
            else:
                # Se max_split è raggiunto e il cammino non è stato trovato, mostra il risultato finale
                root.after(4000, lambda: show_final_result(grid))
                    
    # Inizia il processo ricorsivo con il primo step 
    root.after(6500, step)
   
    root.mainloop() # mantiene attiva l'interfaccia grafica fino a quando l'utente decide di chiudere l'applicazione.


main()