import imageio.v3 as iio
import numpy as np
from PIL import Image

def create_gif(image_files, gif_filename):

    images = []

    # Trova la dimensione minima tra tutte le immagini
    min_width, min_height = None, None

    for filename in image_files:
        img = Image.open(filename)
        if min_width is None or min_height is None:
            min_width, min_height = img.size
        else:
            min_width = min(min_width, img.width)
            min_height = min(min_height, img.height)

    # Ridimensiona le immagini alla dimensione minima e aggiungile alla lista
    for filename in image_files:
        img = Image.open(filename)
        resized_img = img.resize((min_width, min_height), Image.LANCZOS)
        images.append(np.array(resized_img))  

    # Crea la GIF con le immagini ridimensionate
    iio.imwrite(gif_filename, images, duration=3000, loop=1)  # tra un'immagine e la successiva passano 3 secondi


