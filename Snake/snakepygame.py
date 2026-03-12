import random
import sys
import pygame

# Basic configs
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
FPS = 8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (40, 40, 40)
YELLOW = (255, 255, 0)

def draw_text(surface, text, font, color, x, y, center=False):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(rendered, rect)

def random_food_position(snake):
    max_x = WIDTH // BLOCK_SIZE - 1
    max_y = HEIGHT // BLOCK_SIZE - 1

    while True:
        x = random.randint(0, max_x) * BLOCK_SIZE
        y = random.randint(0, max_y) * BLOCK_SIZE
        if [x, y] not in snake:
            return [x, y]

def draw_grid(screen):
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def start_screen(screen, title_font, info_font, clock):
    while True:
        screen.fill(BLACK)
        draw_text(screen, "SNAKE GAME", title_font, GREEN, WIDTH // 2, HEIGHT // 2 - 100, True)
        draw_text(screen, "Press SPACE to start", info_font, WHITE, WIDTH // 2, HEIGHT // 2 - 20, True)
        draw_text(screen, "Press Q to quit", info_font, WHITE, WIDTH // 2, HEIGHT // 2 + 20, True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(10)

def pause_screen(screen, title_font, info_font, clock):
    paused = True
    while paused:
        screen.fill(BLACK)
        draw_text(screen, "PAUSED", title_font, YELLOW, WIDTH // 2, HEIGHT // 2 - 60, True)
        draw_text(screen, "Press P to continue", info_font, WHITE, WIDTH // 2, HEIGHT // 2, True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(10)

def game_over_screen(screen, title_font, info_font, clock, score, high_score):
    while True:
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", title_font, RED, WIDTH // 2, HEIGHT // 2 - 100, True)
        draw_text(screen, f"Score: {score}", info_font, WHITE, WIDTH // 2, HEIGHT // 2 - 30, True)
        draw_text(screen, f"High Score: {high_score}", info_font, WHITE, WIDTH // 2, HEIGHT // 2 + 5, True)
        draw_text(screen, "Press R to restart", info_font, WHITE, WIDTH // 2, HEIGHT // 2 + 45, True)
        draw_text(screen, "Press Q to quit", info_font, WHITE, WIDTH // 2, HEIGHT // 2 + 80, True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(10)

# Main game
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", 40, bold=True)
    score_font = pygame.font.SysFont("arial", 28)
    info_font = pygame.font.SysFont("arial", 24)

    high_score = 0

    start_screen(screen, title_font, info_font, clock)

    while True:
        snake = [
            [WIDTH // 2, HEIGHT // 2],
            [WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2],
            [WIDTH // 2 - 2 * BLOCK_SIZE, HEIGHT // 2],
        ]
        direction = "RIGHT"
        next_direction = direction
        food = random_food_position(snake)
        score = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != "DOWN":
                        next_direction = "UP"
                    elif event.key == pygame.K_DOWN and direction != "UP":
                        next_direction = "DOWN"
                    elif event.key == pygame.K_LEFT and direction != "RIGHT":
                        next_direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and direction != "LEFT":
                        next_direction = "RIGHT"
                    elif event.key == pygame.K_p:
                        pause_screen(screen, title_font, info_font, clock)

            direction = next_direction

            head_x, head_y = snake[0]

            if direction == "UP":
                head_y -= BLOCK_SIZE
            elif direction == "DOWN":
                head_y += BLOCK_SIZE
            elif direction == "LEFT":
                head_x -= BLOCK_SIZE
            elif direction == "RIGHT":
                head_x += BLOCK_SIZE

            new_head = [head_x, head_y]

            hit_wall = (
                head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT
            )
            hit_self = new_head in snake[1:]

            if hit_wall or hit_self:
                running = False
                continue

            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                if score > high_score:
                    high_score = score
                food = random_food_position(snake)
            else:
                snake.pop()

            screen.fill(BLACK)
            draw_grid(screen)

            pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

            for i, segment in enumerate(snake):
                color = GREEN if i == 0 else WHITE
                pygame.draw.rect(screen, color, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

            draw_text(screen, f"Score: {score}", score_font, WHITE, 10, 10)
            draw_text(screen, f"High Score: {high_score}", score_font, WHITE, 10, 40)
            draw_text(screen, "P = Pause", score_font, WHITE, 10, 70)

            pygame.display.flip()
            clock.tick(FPS)

        game_over_screen(screen, title_font, info_font, clock, score, high_score)

if __name__ == "__main__":
    main()