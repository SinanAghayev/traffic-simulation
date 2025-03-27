import math
import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 960, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Car dimensions
car_width, car_height = 15, 30

# Clock for controlling frame rate
clock = pygame.time.Clock()


# Car class
class Car:
    def __init__(self, x, y, width, height, color, speed, direction=0):
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.direction = direction  # Angle in degrees, 0 is up, 90 is left
        self.color = color
        self.is_colliding = False

    def move(self):
        # Convert direction to radians for calculations
        radians = math.radians(self.direction)
        dx = self.speed * -math.sin(radians)
        dy = self.speed * -math.cos(radians)

        # Update position
        self.rect.x += dx
        self.rect.y += dy

        # Clamp position between 0 and WIDTH
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self, surface):
        # Rotate the car image based on its direction
        self.rotated_image = pygame.transform.rotate(
            self.original_image, self.direction
        )
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)
        surface.blit(self.rotated_image, self.rotated_rect.topleft)

    def get_mask(self):
        # Create a mask for the rotated image
        return pygame.mask.from_surface(self.rotated_image)


# Create cars
cars = [
    Car(
        random.randint(0, WIDTH - 50),
        HEIGHT - 150,
        car_width,
        car_height,
        RED,
        random.randint(2, 5),
    )
]
cars.extend(
    [
        Car(
            random.randint(0, WIDTH - 50),
            HEIGHT,
            car_width,
            car_height,
            BLUE,
            random.randint(2, 5),
        )
        for _ in range(10)
    ]
)

# Assign the first car to be user-controlled
user_car = cars[0]
# Draw everything
screen.fill(WHITE)
for car in cars:
    car.draw(screen)


# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle user input for controlling the user car
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            user_car.speed = 5  # Move forward
        elif keys[pygame.K_DOWN]:
            user_car.speed = -5  # Move backward
        else:
            user_car.speed = 0  # Stop

        if keys[pygame.K_LEFT]:
            user_car.direction += 5  # Turn left
        if keys[pygame.K_RIGHT]:
            user_car.direction -= 5  # Turn right

        # Update cars
        for car in cars:
            car.move()

        check_collisions()

        for car in cars:
            if car.is_colliding:
                car.original_image.fill(GREEN)
            else:
                car.original_image.fill(car.color)

        # Draw everything
        screen.fill(WHITE)
        for car in cars:
            car.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def check_collisions():
    for car in cars:
        car.is_colliding = False
    # Check for collisions
    for i in range(len(cars)):
        for j in range(i + 1, len(cars)):
            # Get masks and offsets for collision detection
            mask1 = cars[i].get_mask()
            mask2 = cars[j].get_mask()
            offset = (
                cars[j].rotated_rect.x - cars[i].rotated_rect.x,
                cars[j].rotated_rect.y - cars[i].rotated_rect.y,
            )
            if mask1.overlap(mask2, offset):
                # Change color of cars on collision
                cars[i].is_colliding = True
                cars[j].is_colliding = True


if __name__ == "__main__":
    main()
