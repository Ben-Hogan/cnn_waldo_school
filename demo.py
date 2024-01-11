import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1440
screen_height = 770

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Find Waldo-Ben.H-Game_Instructions")

# List of image file paths
image_paths = ["interface_assets/demo/demo1.jpg", "interface_assets/demo/demo2.jpg", "interface_assets/demo/demo3.jpg", "interface_assets/demo/demo4.jpg"]  # Add your image file paths here

# Load images and scale them to fill the screen
images = [pygame.transform.scale(pygame.image.load(image_path), (screen_width, screen_height)) for image_path in image_paths]

# Set initial image index
current_image_index = 0

# Load arrow images
arrow_left = pygame.transform.scale(pygame.image.load("interface_assets/demo/left.png"), (50, 50))
arrow_right = pygame.transform.scale(pygame.image.load("interface_assets/demo/right.png"), (50, 50))

# Slideshow settings
slideshow_delay = 3  # Time delay between images in seconds
slideshow_timer = 0

# Cross-fade transition settings
transition_duration = 1000  # Time in milliseconds for the transition effect
transition_start_time = 0

# Surface for the cross-fade transition
transition_surface = pygame.Surface((screen_width, screen_height))

# Clock to control frame rate
clock = pygame.time.Clock()

# Function to handle button clicks
def handle_button_click(x, y):
    global current_image_index
    if x < screen_width // 2:
        # Left button clicked, go to the previous image
        transition_to_image((current_image_index - 1) % len(images))
    else:
        # Right button clicked, go to the next image
        transition_to_image((current_image_index + 1) % len(images))

# Function to smoothly transition to a new image using cross-fade
def transition_to_image(new_index):
    global current_image_index, transition_start_time
    current_image_index = new_index
    transition_start_time = pygame.time.get_ticks()

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle button clicks
            x, y = pygame.mouse.get_pos()
            handle_button_click(x, y)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        # Go to the previous image
        transition_to_image((current_image_index - 1) % len(images))

    if keys[pygame.K_RIGHT]:
        # Go to the next image
        transition_to_image((current_image_index + 1) % len(images))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Calculate the transition alpha based on time
    elapsed_time = pygame.time.get_ticks() - transition_start_time
    if elapsed_time < transition_duration:
        transition_alpha = int((elapsed_time / transition_duration) * 255)
    else:
        transition_alpha = 255

    # Display the current image
    current_image = images[current_image_index]
    screen.blit(current_image, (0, 0))

    # Display arrow buttons
    screen.blit(arrow_left, (10, (screen_height - arrow_left.get_height()) // 2))
    screen.blit(arrow_right, (screen_width - 10 - arrow_right.get_width(), (screen_height - arrow_right.get_height()) // 2))

    # Apply the cross-fade transition effect
    transition_surface.set_alpha(255 - transition_alpha)
    transition_surface.fill((0, 0, 0))
    screen.blit(transition_surface, (0, 0))

    # Update the display
    pygame.display.flip()

    # Delay to control the frame rate
    pygame.time.delay(30)  # Cap the frame rate to a reasonable value

# Quit Pygame
pygame.quit()

# Exit the demo
sys.exit()
