import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1440
screen_height = 770

# Create the screen
main_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Find Waldo-Ben.H-Scoreboard")

# Define colors and fonts
background_color = (255, 255, 255)
text_color = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Load data from the "score.txt" file
with open("interface_assets/score.txt", "r") as file:
    lines = file.readlines()

# Initialize variables for scrolling
scroll_offset = 0
line_height = 50
scroll_speed = 1

# Main game loop for the scoreboard
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle scroll wheel events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll Up
                scroll_offset = max(scroll_offset - 1, 0)
            elif event.button == 5:  # Scroll Down
                scroll_offset = min(scroll_offset + 1, max(0, len(lines) // 4 - screen_height // line_height))

    # Clear the screen
    main_screen.fill(background_color)

    # Draw text on the main screen
    y_pos = 0
    for i in range(scroll_offset * 4, min(scroll_offset * 4 + screen_height // line_height * 4, len(lines)), 4):
        try:
            player_name = lines[i].split(": ")[1].strip()
            human_time = lines[i + 1].split(": ")[1].strip()
            ai_time = lines[i + 2].split(": ")[1].strip()
            picture_number = lines[i + 3].split(": ")[1].strip()

            # Render and blit each text element separately
            player_text = font.render(f"Player: {player_name}", True, text_color)
            main_screen.blit(player_text, (50, y_pos))

            human_time_text = font.render(f"Human Time: {human_time}", True, text_color)
            main_screen.blit(human_time_text, (200, y_pos))

            ai_time_text = font.render(f"AI Time: {ai_time}", True, text_color)
            main_screen.blit(ai_time_text, (400, y_pos))

            picture_number_text = font.render(f"Picture Number: {picture_number}", True, text_color)
            main_screen.blit(picture_number_text, (600, y_pos))

            y_pos += line_height + 10  # Add a small gap between entries
        except IndexError:
            # Handle cases where there are not enough lines in the file
            pass

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
