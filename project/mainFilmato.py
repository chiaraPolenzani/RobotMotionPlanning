import glob
import time
import random
import threading
import tkinter as tk
from tkinter import *
from gif import create_gif
from griglia import Griglia
from camminoMinimoDijkstra import cammino_minimo_dijkstra, draw_path
from draw import draw_obstacles, draw_start_goal

root = tk.Tk()
root.title("Occupancy grid")

def main():
   
    rows = 18
    cols = 38
    x_start = 6
    y_start = 15
    x_goal = 30
    y_goal = 5

    # creo l'oggetto griglia 
    grid = Griglia(root, rows = rows, cols = cols, x_start = x_start, y_start = y_start , x_goal = x_goal, y_goal = y_goal) 
    
    max_split = 3
    current_split = 0
    num_obstacles = 40
    min_vertices = 3
    max_vertices = 6

    while len(grid.obstacles) < num_obstacles:
        grid.create_obstacle(num_vertices=random.randint(min_vertices, max_vertices))

    draw_obstacles(grid)
    draw_start_goal(grid, x_start, y_start, x_goal, y_goal)
    grid.save_grid_as_image('frame_1.png')
    grid.node_intersection()
    grid.save_grid_as_image('frame_2.png')
    time.sleep(1)
    text = grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, fill="red", 
                                   font=("Arial", 40), text="Ricerca del percorso...")
    time.sleep(2)
    grid.save_grid_as_image('frame_3.png')
    grid.canvas.delete(text)
    time.sleep(1)

    def execute_dijkstra(grid):
       
        # Esegui Dijkstra per cercare il percorso minimo
        color = "green" # colore dei nodi visitati dall'algoritmo di Dijkstra        
        result = cammino_minimo_dijkstra(grid, grid.start, grid.goal, color)
        if result:
            draw_path(grid, grid.goal)
            draw_start_goal(grid, x_start, y_start, x_goal, y_goal)
            grid.save_grid_as_image('frame_50.png')
            time.sleep(2)
            grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, 
                                           fill="red", font=("Arial Bold", 40), text="Percorso trovato!!")
            grid.save_grid_as_image('frame_60.png')
            return True
        else:
            return False
    
    
    result = execute_dijkstra(grid)
    counter = 4
    while not result and current_split < max_split:

        text = grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, fill="red", 
                                       font=("Arial Bold", 40), text="Percorso non trovato!!")
        time.sleep(2)
        grid.save_grid_as_image(f'frame_{counter}.png')
        grid.canvas.delete(text)
        time.sleep(1)
        grid.split_nodes()
        draw_obstacles(grid)
        grid.save_grid_as_image(f'frame_{counter+1}.png')
        grid.node_intersection()
        grid.reset_nodes_properties()
        grid.save_grid_as_image(f'frame_{counter+2}.png')
        text = grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, fill="red", 
                                font=("Arial", 40), text="Ricerca del percorso...")
        time.sleep(1)
        grid.save_grid_as_image(f'frame_{counter+3}.png')
        grid.canvas.delete(text)
        time.sleep(1)
        current_split += 1
        result = execute_dijkstra(grid)
        time.sleep(1)
        counter += 4
    if not result:
        # Raggiunto il numero massimo di suddivisioni senza trovare il percorso
        grid.canvas.create_text((grid.cols * grid.size) // 2, (grid.rows * grid.size) // 2, fill="red", 
                                font=("Arial Bold", 40), text="Risultato finale:\nPercorso non trovato!!")
        time.sleep(2)
        grid.save_grid_as_image('frame_40.png')
        return

def extract_number(filename):
    # Estrae il numero da un nome di file
    return int(''.join(filter(str.isdigit, filename)))

def main2():
    button.pack_forget()
    threading.Thread(target=main).start()

# Dopo aver premuto il pulsante Avvia parte il filmato
button = tk.Button(root, text="Avvia", command=main2)
button.pack(pady=10)

root.mainloop()

image_files = sorted(glob.glob('frame_*.png'), key=extract_number)
create_gif(image_files, 'output.gif')

