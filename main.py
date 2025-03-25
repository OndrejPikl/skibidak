import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1500, 900
CELL_SIZE = 100  # Zvetseno z 20 na 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60  # Zvýšeno na 60 FPS
SNAKE_SPEED = 8  # Rychlost hada, nastavena pro hratelnost

# Load sounds

# Load graphics
background_image = pygame.image.load("pozadí-snejk,hotovo.png")
snake_head_image = pygame.image.load("hlava_hada.png")
snake_body_image = pygame.image.load("tělo_hada.png")
food_image = pygame.image.load("jablko_had.png")

# Scale graphics to fit CELL_SIZE
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
snake_head_image = pygame.transform.scale(snake_head_image, (CELL_SIZE, CELL_SIZE))
snake_body_image = pygame.transform.scale(snake_body_image, (CELL_SIZE, CELL_SIZE))

# Zvetseni velikosti jablka
food_image = pygame.transform.scale(food_image, (CELL_SIZE * 1.5, CELL_SIZE * 1.5))

# Fonts
font = pygame.font.SysFont("comicsansms", 30)

def draw_text(text, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def draw_snake(snake):
    for i, segment in enumerate(snake):
        if i == 0:
            screen.blit(snake_head_image, segment)
        else:
            screen.blit(snake_body_image, segment)

def draw_food(food):
    screen.blit(food_image, food)

def reset_game():
    global snake, snake_dir, snake_last_dir, food, score
    # Snake and food initialization
    snake = [(100, 100), (100 - CELL_SIZE, 100), (100 - 2 * CELL_SIZE, 100)]
    snake_dir = (CELL_SIZE, 0)
    snake_last_dir = snake_dir  # Prevents instant reverse movement
    food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
    score = 0

def game_over(score):
    # Display the game over screen
    screen.fill(BLACK)
    draw_text(f"Game Over! Your Score: {score}", WHITE, WIDTH // 3, HEIGHT // 3)
    draw_text("Press 'Q' to Quit or 'R' to Restart", WHITE, WIDTH // 3, HEIGHT // 2)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    reset_game()  # Reset the game state
                    main_game()  # Restart the game

# Main game loop
def main_game():
    global snake, snake_dir, snake_last_dir, food, score
    running = True
    frame_counter = 0

    # Time-based movement interval (in milliseconds)
    last_move_time = pygame.time.get_ticks()

    # Zpomaleni hada o 25% -> prodloužení intervalu pohybu
    MOVE_INTERVAL = 150 * 1.25  # Zvýšeno o 25%

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Control the snake (Arrow keys and WASD keys)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and snake_last_dir != (0, CELL_SIZE):
            snake_dir = (0, -CELL_SIZE)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and snake_last_dir != (0, -CELL_SIZE):
            snake_dir = (0, CELL_SIZE)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and snake_last_dir != (CELL_SIZE, 0):
            snake_dir = (-CELL_SIZE, 0)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and snake_last_dir != (-CELL_SIZE, 0):
            snake_dir = (CELL_SIZE, 0)

        # Get current time for movement control
        current_time = pygame.time.get_ticks()

        # Move the snake only if the time interval has passed
        if current_time - last_move_time > MOVE_INTERVAL:
            last_move_time = current_time

            new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
            snake = [new_head] + snake[:-1]
            snake_last_dir = snake_dir  # Store last direction

            # Check collisions with walls
            if new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= WIDTH or new_head[1] >= HEIGHT:
                game_over(score)
                return

            # Check collisions with itself
            if new_head in snake[1:]:
                game_over(score)
                return

            # Check if the snake eats the food
            if new_head == food:
                snake.append(snake[-1])
                food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                        random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
                score += 1

        # Draw everything
        screen.blit(background_image, (0, 0))
        draw_snake(snake)
        draw_food(food)
        draw_text(f"Score: {score}", WHITE, 10, 10)
        pygame.display.flip()

        # Control the game speed (FPS)
        clock.tick(FPS)  # FPS nastaveno na 60 pro plynulý chod hry
        frame_counter += 1

def start_menu():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Press 'P' to Play or 'Q' to Quit", WHITE, WIDTH // 3, HEIGHT // 3)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_p:
                    reset_game()
                    main_game()
                    running = False


start_menu()

pygame.quit()
