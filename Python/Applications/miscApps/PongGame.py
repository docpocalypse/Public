import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
FPS = 60

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Paddle settings
paddle_speed = 10
player_paddle = pygame.Rect(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(SCREEN_WIDTH - 10 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball settings
ball_speed_x, ball_speed_y = 7, 7
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Clock
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN]:
        player_paddle.y += paddle_speed
    if keys[pygame.K_w]:
        opponent_paddle.y -= paddle_speed
    if keys[pygame.K_s]:
        opponent_paddle.y += paddle_speed

    # Keep paddles on the screen
    player_paddle.y = max(player_paddle.y, 0)
    player_paddle.y = min(player_paddle.y, SCREEN_HEIGHT - PADDLE_HEIGHT)
    opponent_paddle.y = max(opponent_paddle.y, 0)
    opponent_paddle.y = min(opponent_paddle.y, SCREEN_HEIGHT - PADDLE_HEIGHT)

    # Ball Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    # Ball reset if it goes past paddle
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_speed_x *= -1

    # Rendering
    screen.fill((0, 0, 0))  # Black background
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Updating the window
    pygame.display.flip()
    clock.tick(FPS)
