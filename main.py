import pygame
import random

# ---------------------------------------
# Inicializace pygame knihovny
# ---------------------------------------
pygame.init()

# ---------------------------------------
# Rozměry okna a velikost jedné buňky
# ---------------------------------------
WIDTH, HEIGHT = 1500, 900
CELL_SIZE = 100  # Velikost jednoho políčka (had + jídlo)

# ---------------------------------------
# Barvy
# ---------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ---------------------------------------
# Vytvoření herního okna
# ---------------------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# ---------------------------------------
# FPS a rychlost
# ---------------------------------------
clock = pygame.time.Clock()
FPS = 60               # Obnovovací frekvence (plynulost)
SNAKE_SPEED = 8        # Zatím nevyužito, ale může se hodit

# ---------------------------------------
# Načtení grafických souborů
# ---------------------------------------
background_image = pygame.image.load("pozadí-snejk,hotovo.png")
snake_head_image = pygame.image.load("hlava_hada.png")
snake_body_image = pygame.image.load("tělo_hada.png")
food_image = pygame.image.load("jablko_had.png")

# ---------------------------------------
# Úprava velikostí obrázků
# ---------------------------------------
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
snake_head_image = pygame.transform.scale(snake_head_image, (CELL_SIZE, CELL_SIZE))
snake_body_image = pygame.transform.scale(snake_body_image, (CELL_SIZE, CELL_SIZE))

# Jablko je 1,5× větší než políčko
food_image = pygame.transform.scale(food_image, (CELL_SIZE * 1.5, CELL_SIZE * 1.5))

# ---------------------------------------
# Font pro texty
# ---------------------------------------
font = pygame.font.SysFont("comicsansms", 30)

# ---------------------------------------
# Funkce pro kreslení textu
# ---------------------------------------
def draw_text(text, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

# ---------------------------------------
# Funkce vykreslení hada
# Každá část je obrázek (hlava/tělo)
# ---------------------------------------
def draw_snake(snake):
    for i, segment in enumerate(snake):
        if i == 0:  # první segment = hlava
            screen.blit(snake_head_image, segment)
        else:
            screen.blit(snake_body_image, segment)

# ---------------------------------------
# Funkce vykreslení jídla
# ---------------------------------------
def draw_food(food):
    screen.blit(food_image, food)

# ---------------------------------------
# Funkce resetuje celou hru na začátek
# ---------------------------------------
def reset_game():
    global snake, snake_dir, snake_last_dir, food, score

    # Výchozí umístění hada (3 segmenty)
    snake = [
        (100, 100),
        (100 - CELL_SIZE, 100),
        (100 - 2 * CELL_SIZE, 100)
    ]

    # Had začíná pohybem doprava
    snake_dir = (CELL_SIZE, 0)
    snake_last_dir = snake_dir

    # Náhodná pozice jídla
    food = (
        random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
        random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
    )

    score = 0

# ---------------------------------------
# Obrazovka GAME OVER
# ---------------------------------------
def game_over(score):
    screen.fill(BLACK)
    draw_text(f"Game Over! Your Score: {score}", WHITE, WIDTH // 3, HEIGHT // 3)
    draw_text("Press 'Q' to Quit or 'R' to Restart", WHITE, WIDTH // 3, HEIGHT // 2)
    pygame.display.flip()

    # Čekání na vstup hráče
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

                elif event.key == pygame.K_r:
                    reset_game()
                    main_game()  # zpět do hry

# ---------------------------------------
# Hlavní herní smyčka
# Obsahuje vše: pohyb, logiku a vykreslování
# ---------------------------------------
def main_game():
    global snake, snake_dir, snake_last_dir, food, score

    running = True
    frame_counter = 0

    # Čas posledního pohybu hada
    last_move_time = pygame.time.get_ticks()

    # Interval pohybu → 150ms * 1.25 = pomalejší had
    MOVE_INTERVAL = 150 * 1.25

    while running:
        # ---------------------------
        # Ovládání hráče
        # ---------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Zamezení otočení o 180° → kontrola snake_last_dir
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and snake_last_dir != (0, CELL_SIZE):
            snake_dir = (0, -CELL_SIZE)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and snake_last_dir != (0, -CELL_SIZE):
            snake_dir = (0, CELL_SIZE)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and snake_last_dir != (CELL_SIZE, 0):
            snake_dir = (-CELL_SIZE, 0)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and snake_last_dir != (-CELL_SIZE, 0):
            snake_dir = (CELL_SIZE, 0)

        # ---------------------------
        # Pohyb hada podle času
        # ---------------------------
        current_time = pygame.time.get_ticks()

        if current_time - last_move_time > MOVE_INTERVAL:
            last_move_time = current_time

            # Vypočet nové hlavy
            new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

            # Posunutí hada → nový head + bez posledního
            snake = [new_head] + snake[:-1]

            snake_last_dir = snake_dir

            # ---------------------------
            # Kolize s okrajem
            # ---------------------------
            if new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= WIDTH or new_head[1] >= HEIGHT:
                game_over(score)
                return

            # ---------------------------
            # Kolize se sebou
            # ---------------------------
            if new_head in snake[1:]:
                game_over(score)
                return

            # ---------------------------
            # Snězení jídla
            # ---------------------------
            if new_head == food:
                snake.append(snake[-1])  # prodloužení
                food = (
                    random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
                )
                score += 1

        # ---------------------------
        # Vykreslování
        # ---------------------------
        screen.blit(background_image, (0, 0))
        draw_snake(snake)
        draw_food(food)
        draw_text(f"Score: {score}", WHITE, 10, 10)
        pygame.display.flip()

        # FPS
        clock.tick(FPS)
        frame_counter += 1

# ---------------------------------------
# Úvodní menu
# ---------------------------------------
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

# ---------------------------------------
# Spuštění hry
# ---------------------------------------
start_menu()
pygame.quit()
