import random
import sys
import pygame

# Basic configs
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
FPS = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (40, 40, 40)

def draw_text(surface, text, font, color, x, y):
    rendered = font.render(text, True, color)
    surface.blit(rendered, (x, y))
    
def random_food_position(snake):
    max_x = WIDTH // BLOCK_SIZE - 1
    max_y = HEIGHT // BLOCK_SIZE - 1
    
    while True:
        x = random.randint(0, max_x) * BLOCK_SIZE
        y = random.randint(0, max_y) * BLOCK_SIZE
        if [x, y] not in snake:
            return [x, y]
        
# Main game
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    score_font = pygame.font.SysFont("arial", 28)
    game_over_font = pygame.font.SysFont("arial", 36, bold = True)
    info_font = pygame.font.SysFont("arial", 24)
    
    while True:
        # Reset game
        snake = [
            [WIDTH // 2, HEIGHT // 2],
            [WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2],
            [WIDTH // 2 -2 * BLOCK_SIZE, HEIGHT // 2],
        ]
        direction = "RIGHT"
        next_direction = direction
        food = random_food_position(snake)
        score = 0
        running = True
        
        while running:
            # Event handling
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
                        
            direction = next_direction
            
            # Updating head position
            head_x, head_y = snake [0]
            
            if direction == "UP":
                head_y -= BLOCK_SIZE
            elif direction == "DOWN":
                head_y += BLOCK_SIZE
            elif direction == "LEFT":
                head_x -= BLOCK_SIZE
            elif direction == "RIGHT":
                head_x += BLOCK_SIZE
                
            new_head = [head_x, head_y]
            
            # Collision check with walls
            hit_wall = (
                head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT
            )
            
            # Collision check with own body
            hit_self = new_head in snake[:1]
            
            if hit_wall or hit_self:
                running = False
                continue
            
            # Snake movement
            snake.insert(0, new_head)
            
            if new_head == food:
                score += 1
                food = random_food_position(snake)
            else:
                snake.pop()
                
            # Drawing
            screen.fill(BLACK)
            
            # Grid
            for x in range(0, WIDTH, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
                
            # Food
            pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
            
            # Snake
            for i, segment in enumerate(snake):
                color = GREEN if i == 0 else WHITE
                pygame.draw.rect(screen, color, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
                
            # Score
            draw_text(screen, f"Score: {score}", score_font, WHITE, 10, 10)
            
            pygame.display.flip()
            clock.tick(FPS)
            
        # Game over screen
        waiting = True
        while waiting:
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER", game_over_font, RED, WIDTH // 2 - 120, HEIGHT // 2 - 80)
            draw_text(screen, f"Final Score: {score}", info_font, WHITE, WIDTH // 2 - 80, HEIGHT // 2 - 20)
            draw_text(screen, "Press R for restart", info_font, WHITE, WIDTH // 2 - 105, HEIGHT // 2 + 20)
            draw_text(screen, "Press Q or close window to exit", info_font, WHITE, WIDTH // 2 - 165, HEIGHT // 2 + 55)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                        
            clock.tick(10)
            
            
if __name__ == "__main__":
    main()