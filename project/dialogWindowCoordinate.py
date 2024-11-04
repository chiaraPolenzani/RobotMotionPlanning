import tkinter as tk
from tkinter import messagebox

class dialogWindowCoordinate:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()  # Nascondi la finestra principale finché l'utente non ha inserito le coordinate
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.dialogWindow_height = self.screen_height // 4
        self.dialogWindow_width = self.screen_width // 3
        # Chiedo all'utente di inserire il numero di righe e colonne della griglia
        self.rows, self.cols = self.get_rows_cols()
        # Chiedo all'utente di inserire le coordinate del punto di partenza e arrivo
        self.x_start, self.y_start = self.get_start_goal("inizio")
        self.x_goal, self.y_goal = self.get_start_goal("fine")
        # Chiedo all'utente di scegliere il numero degli ostacoli nella griglia
        self.num_obstacles = self.get_num_obstacles()
        
        self.master.deiconify()  # Mostra la finestra principale dopo l'input

    def get_rows_cols(self):

        dialogWindow = tk.Toplevel()  # crea una finestra di dialogo
        dialogWindow.title(f"Inserisci il numero di righe e colonne della griglia")
        x = (self.screen_width // 2) - (self.dialogWindow_width // 2)
        y = (self.screen_height // 2) - (self.dialogWindow_height // 2)
        dialogWindow.geometry(f"{self.dialogWindow_width}x{self.dialogWindow_height}+{x}+{y}")

        # Crea un frame per centrare gli elementi
        frame = tk.Frame(dialogWindow)
        frame.pack(expand=True)
        
        tk.Label(frame, text=f"Numero di righe della griglia:", 
                 font=("Arial", 12)).pack()
        rows_entry = tk.Entry(frame, background = "lightgray")
        rows_entry.pack(pady=10)
        rows_entry.insert(0, "20")  # Imposta il valore di default 
        
        tk.Label(frame, text=f"Numero di colonne della griglia:",
                 font=("Arial", 12)).pack()
        cols_entry = tk.Entry(frame, background = "lightgray")
        cols_entry.pack(pady=10)
        cols_entry.insert(0, "37")  # Imposta il valore di default

        def conferma():
            try:
                rows_value = int(rows_entry.get())
                cols_value = int(cols_entry.get())

                if rows_value <= 0 or cols_value <= 0:
                    raise ValueError("Il numero di righe e colonne deve essere maggiore di 0.")
                
                dialogWindow.rows_value = rows_value
                dialogWindow.cols_value = cols_value
                dialogWindow.destroy()  # Chiude la finestra se i valori sono validi
            except ValueError as e:
                messagebox.showerror("Errore", str(e))  # Mostra un messaggio di errore

        tk.Button(frame, text="Conferma", font=("Arial", 12), command=conferma, 
                background="lightgray").pack(pady=10)

        dialogWindow.wait_window()  # Aspetta la chiusura della finestra
        
        return dialogWindow.rows_value, dialogWindow.cols_value
    
    def get_num_obstacles(self):

        dialogWindow = tk.Toplevel()  # crea una finestra di dialogo
        dialogWindow.title(f"Inserisci il numero di ostacoli")
        x = (self.screen_width // 2) - (self.dialogWindow_width // 2)
        y = (self.screen_height // 2) - (self.dialogWindow_height // 2)
        dialogWindow.geometry(f"{self.dialogWindow_width}x{self.dialogWindow_height}+{x}+{y}")

        # Crea un frame per centrare gli elementi
        frame = tk.Frame(dialogWindow)
        frame.pack(expand=True)
        
        tk.Label(frame, text=f"Numero di ostacoli nella griglia:", 
                 font=("Arial", 12)).pack()
        obstacles_entry = tk.Entry(frame, background = "lightgray")
        obstacles_entry.pack(pady=10)
        
        def conferma():
            try:
                obstacles_value = int(obstacles_entry.get())

                if obstacles_value <= 0:
                    raise ValueError("Il numero di ostacoli deve essere maggiore di 0.")
                
                dialogWindow.obstacles_value = obstacles_value
                dialogWindow.destroy()  # Chiude la finestra se i valori sono validi
            except ValueError as e:
                messagebox.showerror("Errore", str(e))  # Mostra un messaggio di errore

        tk.Button(frame, text="Conferma", font=("Arial", 12), command=conferma, 
                background="lightgray").pack(pady=10)

        dialogWindow.wait_window()  # Aspetta la chiusura della finestra
        
        return dialogWindow.obstacles_value
    
    def get_start_goal(self, point_type):

        dialogWindow = tk.Toplevel()  # crea una finestra di dialogo
        dialogWindow.title(f"Inserisci le coordinate per il punto di {point_type}")
        x = (self.screen_width // 2) - (self.dialogWindow_width // 2)
        y = (self.screen_height // 2) - (self.dialogWindow_height // 2)
        dialogWindow.geometry(f"{self.dialogWindow_width}x{self.dialogWindow_height}+{x}+{y}")

        # Crea un frame per centrare gli elementi
        frame = tk.Frame(dialogWindow)
        frame.pack(expand=True)
        
        tk.Label(frame, text=f"Coordinata X del punto di {point_type} (compresa tra 0 e {self.cols - 1}):", 
                 font=("Arial", 12)).pack()
        x_entry = tk.Entry(frame, background = "lightgray")
        x_entry.pack(pady=10)
        if point_type == "inizio":
            x_entry.insert(0, "1")  # Imposta il valore di default 
        else:
            x_entry.insert(0, self.cols - 2)  
        
        tk.Label(frame, text=f"Coordinata Y del punto di {point_type} (compresa tra 0 e {self.rows -1 }):",
                 font=("Arial", 12)).pack()
        y_entry = tk.Entry(frame, background = "lightgray")
        y_entry.pack(pady=10)
        if point_type == "inizio":
            y_entry.insert(0, "1")  # Imposta il valore di default 
        else:
            y_entry.insert(0, self.rows - 2)  

        def conferma():
            try:
                x_value = float(x_entry.get())
                y_value = float(y_entry.get())
                
                # Controllo validità delle coordinate
                if not (0 <= x_value < self.cols):
                    raise ValueError(f"X deve essere compresa tra 0 e {self.cols - 1}.")
                if not (0 <= y_value < self.rows):
                    raise ValueError(f"Y deve essere compresa tra 0 e {self.rows - 1}.")
                
                dialogWindow.x_value = x_value
                dialogWindow.y_value = y_value
                dialogWindow.destroy()  # Chiude la finestra se i valori sono validi
            except ValueError as e:
                messagebox.showerror("Errore", str(e))  # Mostra un messaggio di errore

        tk.Button(frame, text="Conferma", font=("Arial", 12), command=conferma, 
                  background="lightgray").pack(pady=10)
        
        dialogWindow.wait_window()  # Aspetta la chiusura della finestra
        
        return dialogWindow.x_value, dialogWindow.y_value
