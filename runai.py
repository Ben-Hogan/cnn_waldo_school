import numpy as np
import cv2
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image
from PIL import Image
import time
import threading
import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 770
WHITE = (255, 255, 255)

# Create the display surface for the Pygame canvas
canvas_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the font for rendering text
font = pygame.font.Font(None, 36)

# Load the model only once
model_path = "weights.h5"
model = models.load_model(model_path, backbone_name='resnet50')

def load_and_preprocess_image(image_path):
    image = read_image_bgr(image_path)
    image = preprocess_image(image)
    return image

def run_image_processing(image):
    draw = image.copy()
    draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
    waldo_box = None

    boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
    found_box = False

    for box, score, label in zip(boxes[0], scores[0], labels[0]):
        if score < 0.4:
            break
        b = box.astype(int)
        if label == 0:
            waldo_box = b
            found_box = True

    # Ensure the image array values are in the range [0, 255]
    draw = np.clip(draw, 0, 255).astype(np.uint8)
    draw_pil = Image.fromarray(draw)
    
    # Calculate the scale factor
    img_width, img_height = draw_pil.size
    scale_factor = min(SCREEN_WIDTH / img_width, SCREEN_HEIGHT / img_height)

    return draw_pil, waldo_box, scale_factor

try:
    with open("tempImg.txt", "r") as file:
        image_path = 'images/' + file.read().strip()
except Exception as e:
    print(f"Error reading image path: {e}")

image = load_and_preprocess_image(image_path)

image_processing_complete = False
waldo_box = None
network_output_pil = None
scale_factor = 1.0
image_processing_done_event = threading.Event()

def scale_surface_to_fit(surface, width, height):
    """
    Scales a pygame surface to fit within the specified width and height,
    while maintaining the image's aspect ratio.
    """
    img_width, img_height = surface.get_size()
    scale_factor = min(width / img_width, height / img_height)
    scaled_width = int(img_width * scale_factor)
    scaled_height = int(img_height * scale_factor)
    return pygame.transform.scale(surface, (scaled_width, scaled_height))

def image_processing_thread():
    global image_processing_complete, network_output_pil, waldo_box, scale_factor
    network_output_pil, waldo_box, scale_factor = run_image_processing(image)
    image_processing_complete = True
    image_processing_done_event.set()

image_processing_thread = threading.Thread(target=image_processing_thread)
image_processing_thread.start()

canvas_running = True
stopwatch_running = False
start_time = time.perf_counter()

while canvas_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            canvas_running = False

    canvas_screen.fill(WHITE)

    if not image_processing_complete:
        if not stopwatch_running:
            start_time = time.perf_counter()
            stopwatch_running = True
        elapsed_time = time.perf_counter() - start_time
        time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, (0, 0, 0))
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50))
        canvas_screen.blit(time_text, time_rect)
    else:
        if stopwatch_running:
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            stopwatch_running = False
        image_processing_done_event.wait()

        # Scale the bounding box
        if waldo_box is not None:
            waldo_box_scaled = [int(coord * scale_factor) for coord in waldo_box]
            cv2.rectangle(network_output_pil, (waldo_box_scaled[0], waldo_box_scaled[1]), 
                          (waldo_box_scaled[2], waldo_box_scaled[3]), (255, 0, 0), 10)
        
        full_image_pil = network_output_pil.copy()
        full_image = pygame.image.fromstring(full_image_pil.tobytes(), full_image_pil.size, full_image_pil.mode)
        scaled_image = scale_surface_to_fit(full_image, SCREEN_WIDTH, SCREEN_HEIGHT)
        canvas_screen.blit(scaled_image, ((SCREEN_WIDTH - scaled_image.get_width()) // 2, 
                                          (SCREEN_HEIGHT - scaled_image.get_height()) // 2))

    pygame.display.update()

pygame.quit()
