import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Initialize game variables
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [4, 4]

left_paddle_pos = [10, HEIGHT // 2 - PADDLE_HEIGHT // 2]
right_paddle_pos = [WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2]
paddle_speed = 5

left_score = 0
right_score = 0

font = pygame.font.Font(None, 36)

# Game mode (0: Player vs Player, 1: Player vs AI)
game_mode = 0

# Game states
MENU = 0
INSTRUCTIONS = 1
PLAYING = 2

# Initialize game state
game_state = MENU

def draw_menu():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50))

    # Add text to the menu
    menu_text = font.render("Press Enter", True, WHITE)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 30))

def draw_instructions():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, HEIGHT // 2 - 25, 300, 50))

    # Add text to the instructions
    instructions_text = font.render("Press Esc to return to Menu", True, WHITE)
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + 30))

def draw_objects():
    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, (left_paddle_pos[0], left_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (right_paddle_pos[0], right_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Draw scores
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (3 * WIDTH // 4 - right_text.get_width(), 20))

# Wait for the initial key press to start the game loop
initial_key_pressed = False
while not initial_key_pressed:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            initial_key_pressed = True

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:  # Enter key
                    game_state = PLAYING
                elif event.key == pygame.K_i:  # I key for instructions
                    game_state = INSTRUCTIONS
            elif game_state == INSTRUCTIONS:
                if event.key == pygame.K_ESCAPE:  # Esc key to return to main menu
                    game_state = MENU

    if game_state == MENU:
        draw_menu()
    elif game_state == INSTRUCTIONS:
        draw_instructions()
    elif game_state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and right_paddle_pos[1] > 0:
            right_paddle_pos[1] -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT:
            right_paddle_pos[1] += paddle_speed
        if keys[pygame.K_w] and left_paddle_pos[1] > 0:
            left_paddle_pos[1] -= paddle_speed
        if keys[pygame.K_s] and left_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT:
            left_paddle_pos[1] += paddle_speed

        # Update ball position
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # Ball collisions with walls
        if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Ball collisions with paddles
        if (
            left_paddle_pos[0] <= ball_pos[0] <= left_paddle_pos[0] + PADDLE_WIDTH and
            left_paddle_pos[1] <= ball_pos[1] <= left_paddle_pos[1] + PADDLE_HEIGHT
        ) or (
            right_paddle_pos[0] <= ball_pos[0] <= right_paddle_pos[0] + PADDLE_WIDTH and
            right_paddle_pos[1] <= ball_pos[1] <= right_paddle_pos[1] + PADDLE_HEIGHT
        ):
            ball_speed[0] = -ball_speed[0]

        # Check for scoring and end game
        if ball_pos[0] <= 0:
            right_score += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]  # Reset ball position
        elif ball_pos[0] >= WIDTH:
            left_score += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]  # Reset ball position

        if left_score == 5 or right_score == 5:
            # Game ends when one player reaches a score of 5
            left_score = 0
            right_score = 0
            game_state = MENU  # Return to the main menu

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw game objects
    draw_objects()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
