import pygame
import random

# Initialize pygame
pygame.init()

# Set window dimensions
window_width = 2560
window_height = 1440

# Create the window
screen = pygame.display.set_mode((window_width, window_height))

# Set the title of the window
pygame.display.set_caption("DVD Idle Screen")

# Set the DVD logo image
dvd_logo = pygame.image.load("dvd_logo.png")

# Get the width and height of the DVD logo image
dvd_logo_width, dvd_logo_height = dvd_logo.get_size()

# Set the initial position of the DVD logo
dvd_logo_x = random.randint(0, window_width - dvd_logo_width)
dvd_logo_y = random.randint(0, window_height - dvd_logo_height)

# Set the initial velocity of the DVD logo
dvd_logo_velocity_x = 1
dvd_logo_velocity_y = 1

# Set the running flag to True
running = True

# Run the game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the position of the DVD logo
    dvd_logo_x += dvd_logo_velocity_x
    dvd_logo_y += dvd_logo_velocity_y

    # Check if the DVD logo has hit the edge of the screen
    if dvd_logo_x + dvd_logo_width >= window_width or dvd_logo_x <= 0:
        dvd_logo_velocity_x = -dvd_logo_velocity_x
    if dvd_logo_y + dvd_logo_height >= window_height or dvd_logo_y <= 0:
        dvd_logo_velocity_y = -dvd_logo_velocity_y

    # Check if the DVD logo has hit the corner of the screen
    if (dvd_logo_x <= 0 and dvd_logo_y <= 0) or \
       (dvd_logo_x + dvd_logo_width >= window_width and dvd_logo_y <= 0) or \
       (dvd_logo_x <= 0 and dvd_logo_y + dvd_logo_height >= window_height) or \
       (dvd_logo_x + dvd_logo_width >= window_width and dvd_logo_y + dvd_logo_height >= window_height):
        print("Congratulations, you hit the corner!")
        running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the DVD logo
    screen.blit(dvd_logo, (dvd_logo_x, dvd_logo_y))

    # Update the display
    pygame.display.flip()

# Quit py