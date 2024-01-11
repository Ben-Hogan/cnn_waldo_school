import pygame
import sys
import os
import random
import datetime
import subprocess  # Import the subprocess module

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1440, 770
WHITE = (255, 255, 255)
BUTTON_COLOR = (50, 150, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)
COUNTDOWN_FONT_COLOR = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Find Waldo-Ben.H-Game")

# Folder containing your images
image_folder = "images"

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

running = True

# Countdown properties
countdown_font = pygame.font.Font(None, 100)
countdown_time = 5  # Initial countdown time in seconds
countdown_text = ""

# Stopwatch properties
stopwatch_font = pygame.font.Font(None, 36)
stopwatch_text = ""
start_time = None

# File to store stopwatch time
stopwatch_filename = "stopwatch_time.txt"

# Function to save stopwatch time
def save_stopwatch_time(elapsed_time):
    with open(stopwatch_filename, "w") as file:
        file.write(elapsed_time)

# Function to run the playerscore script
def run_playerscore_script():
    try:
        subprocess.Popen(["python", "playerscore.py"])  # Replace "python" with the appropriate command if needed
    except FileNotFoundError:
        print("Error: playerscore.py not found or Python is not in the system PATH.")

# Start the countdown loop
while countdown_time > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    # Update countdown text
    countdown_text = str(countdown_time)
    countdown_render = countdown_font.render(countdown_text, True, COUNTDOWN_FONT_COLOR)

    # Center the countdown text
    countdown_x = (WIDTH - countdown_render.get_width()) // 2
    countdown_y = (HEIGHT - countdown_render.get_height()) // 2

    screen.blit(countdown_render, (countdown_x, countdown_y))
    pygame.display.flip()

    pygame.time.delay(1000)  # Delay for 1 second
    countdown_time -= 1

# Countdown finished, display the image and button
if image_files:
    random_image = random.choice(image_files)
    image_path = os.path.join(image_folder, random_image)

    original_image = pygame.image.load(image_path)
    image_width, image_height = original_image.get_size()

    max_width = WIDTH
    max_height = HEIGHT - 100

    scale_factor = min(max_width / image_width, max_height / image_height)
    scaled_image = pygame.transform.smoothscale(original_image, (int(image_width * scale_factor), int(image_height * scale_factor)))

    # Save the filename to 'tempImg.txt'
    with open('tempImg.txt', 'w') as temp_file:
        temp_file.write(random_image)

button_width = 200
button_height = 50
button_x = (WIDTH - button_width) // 2
button_y = HEIGHT - 70

button_font = pygame.font.Font(None, 36)
button_text = button_font.render("Found Him", True, BUTTON_TEXT_COLOR)
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Start the stopwatch
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Button Clicked!")
                end_time = pygame.time.get_ticks()
                elapsed_time_ms = end_time - start_time
                elapsed_time_sec = elapsed_time_ms / 1000.0  # Convert milliseconds to seconds
                elapsed_time_str = "{:.2f}".format(elapsed_time_sec)  # Format to two decimal places
                save_stopwatch_time(elapsed_time_str)  # Save stopwatch time to a text file
                run_playerscore_script()  # Run the playerscore script
                pygame.quit()
                sys.exit()

    screen.fill(WHITE)
    screen.blit(scaled_image, (WIDTH // 2 - scaled_image.get_width() // 2, HEIGHT // 2 - scaled_image.get_height() // 2))

    # Update and display the stopwatch text with two decimal places
    elapsed_time_ms = pygame.time.get_ticks() - start_time
    elapsed_time_sec = elapsed_time_ms / 1000.0  # Convert milliseconds to seconds
    elapsed_time_str = "{:.2f}".format(elapsed_time_sec)  # Format to two decimal places
    stopwatch_text = f"Time: {elapsed_time_str} seconds"
    stopwatch_render = stopwatch_font.render(stopwatch_text, True, COUNTDOWN_FONT_COLOR)
    screen.blit(stopwatch_render, (20, HEIGHT // 2 - stopwatch_render.get_height() // 2))

    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(button_text, (button_x + 20, button_y + 10))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
