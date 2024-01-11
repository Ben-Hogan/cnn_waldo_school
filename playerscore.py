import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1440, 770
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 80
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100
BUTTON_COLOR = (0, 128, 255)  # Blue color for the button
BUTTON_TEXT_COLOR = WHITE
BUTTON_FONT_SIZE = 40

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Score Interface")

# Load the font
font = pygame.font.Font(None, FONT_SIZE)

# Read data from files
with open("tempName.txt", "r") as name_file:
    player_name = name_file.read().strip()

with open("stopwatch_time.txt", "r") as time_file:
    stopwatch_time = time_file.read().strip()

# Create a message
message = f"{player_name}, you found Waldo in {stopwatch_time} seconds"
message_text = font.render(message, True, BLACK)

# Calculate the text position to center it on the screen
text_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2.7))

# Create a button
button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 1.5, BUTTON_WIDTH, BUTTON_HEIGHT)
button_text = font.render("Test AI", True, BUTTON_TEXT_COLOR)
button_text_rect = button_text.get_rect(center=button_rect.center)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                # Close the current window
                pygame.quit()
                
                # Run the other script in a separate process
                subprocess.Popen(["python", "runai.py"])
                sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Display the message
    screen.blit(message_text, text_rect)

    # Draw the button
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(button_text, button_text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame (this part will be executed only if the user closes the window)
pygame.quit()
sys.exit()
