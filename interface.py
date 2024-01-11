import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1440
screen_height = 770

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Find Waldo-Ben.H-Menu")

# Load the background image
background_image = pygame.image.load("interface_assets/background.jpg")

# Resize the background image to match the screen dimensions
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Define button colors and fonts
button_color = (0, 100, 200)
button_font = pygame.font.Font(None, 36)
button_text_color = (255, 255, 255)

# Create play button
play_button_text = "Play"
play_button_width = 200
play_button_height = 75
play_button_x = (screen_width - play_button_width) // 2
play_button_y = 300
play_button_rect = pygame.Rect(play_button_x, play_button_y, play_button_width, play_button_height)

# Create scoreboard button
scoreboard_button_text = "Scoreboard"
scoreboard_button_width = 200
scoreboard_button_height = 75
scoreboard_button_x = (screen_width - scoreboard_button_width) // 2
scoreboard_button_y = 400
scoreboard_button_rect = pygame.Rect(scoreboard_button_x, scoreboard_button_y, scoreboard_button_width, scoreboard_button_height)

# Create demo button
demo_button_text = "Demo"
demo_button_width = 200
demo_button_height = 75
demo_button_x = (screen_width - demo_button_width) // 2
demo_button_y = 500
demo_button_rect = pygame.Rect(demo_button_x, demo_button_y, demo_button_width, demo_button_height)

# Main game loop
menu_open = True

while menu_open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_open = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    # Launch the game.py script as a separate process
                    subprocess.Popen(["python", "pregame.py"])
                    menu_open = False  # Close the menu window
                elif scoreboard_button_rect.collidepoint(mouse_pos):
                    # Handle scoreboard button click (e.g., show high scores)
                    print("Scoreboard button clicked")
                    # Run the scoreboard program as a separate process
                    subprocess.Popen(["python", "scoreboard.py"])
                elif demo_button_rect.collidepoint(mouse_pos):
                    # Handle demo button click (e.g., start a demo)
                    print("Demo button clicked")
                    # Run the demo program as a separate process
                    subprocess.Popen(["python", "demo.py"])

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw buttons
    pygame.draw.rect(screen, button_color, play_button_rect)
    pygame.draw.rect(screen, button_color, scoreboard_button_rect)
    pygame.draw.rect(screen, button_color, demo_button_rect)

    # Draw button text
    play_button_surface = button_font.render(play_button_text, True, button_text_color)
    play_button_text_rect = play_button_surface.get_rect(center=play_button_rect.center)
    screen.blit(play_button_surface, play_button_text_rect)

    scoreboard_button_surface = button_font.render(scoreboard_button_text, True, button_text_color)
    scoreboard_button_text_rect = scoreboard_button_surface.get_rect(center=scoreboard_button_rect.center)
    screen.blit(scoreboard_button_surface, scoreboard_button_text_rect)

    demo_button_surface = button_font.render(demo_button_text, True, button_text_color)
    demo_button_text_rect = demo_button_surface.get_rect(center=demo_button_rect.center)
    screen.blit(demo_button_surface, demo_button_text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame for the menu window
pygame.quit()
