import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Define Colors
WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Color for the snake

# Square properties
snake_size = 15
snake = [(100, 100)]  # Start with one square
snake_direction = 'RIGHT'  # Initial direction
tolerance=15 #Range between snake and fruit

# Fruit properties
fruit_images = [
    pygame.image.load('.idea/apple.png'),
    pygame.image.load('.idea/cherry.png'),
    pygame.image.load('.idea/strawberry.png')
]

current_fruit_image= random.choice(fruit_images)
current_fruit_image= pygame.transform.scale(current_fruit_image,(18, 18))
def generate_fruit_position():
    while True:
        position = (random.randrange(1, (WIDTH // snake_size)) * snake_size,
                    random.randrange(1, (HEIGHT // snake_size)) * snake_size)
        # Check if the fruit position is not on the snake
        if position not in snake:
            return position

fruit_position = generate_fruit_position()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_s and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_a and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_d and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # Update the snake's position
    if snake_direction == 'UP':
        new_head = (snake[0][0], snake[0][1] - snake_size)
    elif snake_direction == 'DOWN':
        new_head = (snake[0][0], snake[0][1] + snake_size)
    elif snake_direction == 'LEFT':
        new_head = (snake[0][0] - snake_size, snake[0][1])
    elif snake_direction == 'RIGHT':
        new_head = (snake[0][0] + snake_size, snake[0][1])

    # Check if the snake has eaten the fruit
    distance = ((snake[0][0] - fruit_position[0]) ** 2 + (snake[0][1] - fruit_position[1]) ** 2) ** 0.5
    if distance < tolerance:
        snake.append(snake[-1])  # Grow the snake by adding a new segment
        fruit_position = generate_fruit_position()  # Generate a new fruit position

    # Move the snake: insert new head
    snake.insert(0, new_head)
    if not snake[0] == fruit_position:
        snake.pop()

    # Fill the screen with white
    screen.fill(BLACK)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], snake_size, snake_size])

    # Draw the fruit

    screen.blit(current_fruit_image, (fruit_position[0],fruit_position[1]))

    #Game over rules

    if snake[0][0] < 0 or snake[0][0] >= WIDTH or snake[0][1] < 0 or snake[0][1] >= HEIGHT:
        running = False
        font = pygame.font.Font(None, 36)
        text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1500)

    if snake[0] in snake[1:]:
        running = False
        font = pygame.font.Font(None, 36)
        text = font.render('Game Over!', True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1500)

    #Display the score
    font_score = pygame.font.Font(None, 36)
    score = font_score.render(f"Score: {len(snake)}", True, WHITE)
    screen.blit(score, (0, 0))
    # Update the display
    pygame.display.update()

    # Frame rate
    pygame.time.Clock().tick(8)  # Set FPS to 8 for a slower game

# Quit Pygame
pygame.quit()
