import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Constants for colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 48
FONT = pygame.font.Font(None, FONT_SIZE)

# Create the screen
screen_width, screen_height = 1440, 770
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Find Waldo-Ben.H-Name")

# Input box attributes (centered)
input_box_width = 400
input_box_height = 60
input_box_x = (screen_width - input_box_width) // 2
input_box_y = (screen_height - input_box_height - 100) // 2
input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
user_text = ''
active = False

# Submit button attributes
button_width = 200
button_height = 60
button_x = (screen_width - button_width) // 2
button_y = input_box_y + input_box_height + 20
button = pygame.Rect(button_x, button_y, button_width, button_height)
button_color = pygame.Color('dodgerblue2')
button_hover_color = pygame.Color('deepskyblue1')

# Text for the submit button
button_font = pygame.font.Font(None, 36)
button_text = button_font.render("Submit", True, WHITE)
button_text_rect = button_text.get_rect(center=button.center)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            elif button.collidepoint(event.pos):
                # Save user input to a text file
                with open("tempName.txt", "w") as file:
                    file.write(user_text)
                user_text = ''  # Clear the input field after saving
                
                # Execute the game.py script
                subprocess.Popen(["python", "game.py"])  # Adjust the command as needed
                pygame.quit()  # Quit Pygame and stop this script
                sys.exit()

            else:
                active = False
            color = color_active if active else color_inactive

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # Save user input to a text file
                    with open("tempName.txt", "w") as file:
                        file.write(user_text)
                    user_text = ''  # Clear the input field after saving
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    # Fill the background with white
    screen.fill(WHITE)

    # Draw the input box and text
    txt_surface = FONT.render(user_text, True, color)
    width = max(input_box_width, txt_surface.get_width() + 10)
    input_box.w = width
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + (input_box_height - FONT_SIZE) // 2))

    # Draw the submit button
    pygame.draw.rect(screen, button_color, button)
    pygame.draw.rect(screen, BLACK, button, 2)
    screen.blit(button_text, button_text_rect)

    # Draw the label (centered)
    label = FONT.render("Enter your name:", True, BLACK)
    label_x = (screen_width - label.get_width()) // 2
    label_y = input_box.y - FONT_SIZE - 20
    screen.blit(label, (label_x, label_y))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
