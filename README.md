# RobotMotionPlanning


*******	Approximate cell decomposition *******

Questo progetto è un'applicazione Python che riguarda la pianificazione del moto di un robot tra ostacoli basandosi sul metodo di decomposizione in celle approssimata.
L'ambiente è rappresentato da una griglia di occupazione; ogni cella può essere libera, occupata dal robot o da un ostacolo. 
Il percorso dal punto di partenza al punto di arrivo viene calcolato tramite l'algoritmo di Dijkstra. 
Questo metodo non è completo, infatti in alcuni casi non viene trovato nessun percorso, anche se esiste. 
La soluzione è quella di utilizzare una griglia adattativa, che suddivide i nodi che parzialmente intersecano un ostacolo.

- versione: 1.0

- Librerie necessarie: tkinter, shapely, random, heapq, PIL, numpy, imageio.v3, glob, time, threading.

- Il progetto è salvato in formato .rar, facilmente caricabile da Visual Studio Code oppure manovrando i file .py all'interno.

- Il file principale è main.py nel quale è presente il metodo "main" per eseguire l'applicazione.

- Il file mainFilmato.py è stato creato con lo scopo di permettere il salvataggio delle immagini per la creazione di un filmato del programma in esecuzione. 

- All'avvio dell'applicazione viene mostrata una finestra di dialogo per raccogliere alcune informazioni dall'utente; in particolare viene richiesto di inserire il numero di righe e colonne della griglia, le coordinate del punto di partenza e arrivo e il numero di ostacoli.

- la variabile "max_split" serve a definire una condizione di arresto per l'algoritmo nel caso in cui il percorso non venga ripetutamente trovato e rappresenta il numero massimo di suddivisioni di un nodo.



