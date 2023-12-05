# Name: Megan Lee    Initials: ML
# Name: Tyler Nguyen    Initials: TN
# Name: Julia Stolf    Initials: JS
# Name: Steven Zhang    Initials: SZ

#the following libraries and modules must be imported in order for the game functions to operate
import pygame
import sys

# Initialize Pygame (SZ)
pygame.init()

# Start music (JS)
pygame.mixer.music.load('Envici November - Original Instrument.mp3')   
pygame.mixer.music.play(-1)

# Constants (SZ)
#dimensions of the game screen
WIDTH, HEIGHT = 600, 400
#dimensions of ball size
BALL_RADIUS = 10
#dimensions of ball
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
WHITE = (255, 255, 255)

# Create the game window (SZ)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Initialize game variables (SZ)
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [4, 4]

#initalizes the size and position of the left and right paddles
left_paddle_pos = [10, HEIGHT // 2 - PADDLE_HEIGHT // 2]
right_paddle_pos = [WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2]
paddle_speed = 3  # Reduced AI paddle speed

#initalizes the starting score
left_score = 0
right_score = 0

#initalizes font object used for rendering in-game text
font = pygame.font.Font(None, 36)

# Game mode (0: Player vs Player, 1: Player vs AI) (ML)
game_mode = 0

# AI difficulty (0:easy, 1:hard)
ai_difficulty = 0

# Game states (ML)
MENU = 0
INSTRUCTIONS = 1
PLAYING = 2
GAME_OVER = 3

# Initialize game state (ML)
game_state = MENU

# Additional flag for handling game over display (ML)
game_over_displayed = False

# Create surfaces for different screens (ML)
menu_surface = pygame.Surface((WIDTH, HEIGHT))
instructions_surface = pygame.Surface((WIDTH, HEIGHT))
playing_surface = pygame.Surface((WIDTH, HEIGHT))
game_over_surface = pygame.Surface((WIDTH, HEIGHT))  # New surface for game over screen

def draw_objects():
    # Draw paddles and ball (TN)
    pygame.draw.rect(playing_surface, WHITE, (left_paddle_pos[0], left_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(playing_surface, WHITE, (right_paddle_pos[0], right_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(playing_surface, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Draw scores (TN)
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    playing_surface.blit(left_text, (WIDTH // 4, 20))
    playing_surface.blit(right_text, (3 * WIDTH // 4 - right_text.get_width(), 20))

def show_menu():
    #displays the menu in proper font and texts when activated
    menu_font = pygame.font.Font(None, 48)
    title_text = menu_font.render("Pong", True, WHITE)
    start_text = menu_font.render("Press Enter to Play", True, WHITE)  # Added text
    instructions_text = menu_font.render("Press I for Instructions", True, WHITE)

    menu_surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    menu_surface.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 200))
    menu_surface.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, 250))

def show_instructions():
    #displays instruction menu in proper font and texts when performed
    instructions_font = pygame.font.Font(None, 24)
    instruction_text = instructions_font.render("Use W and S to move the left paddle up and down.", True, WHITE)
    instruction_text2 = instructions_font.render("Press A to toggle between Player vs Player and Player vs AI.", True, WHITE)
    instruction_text3 = instructions_font.render("If Player vs AI. is enabled, Press D to toggle between AI difficulty", True, WHITE)
    instruction_text4 = instructions_font.render("Press Esc to return to the main menu.", True, WHITE)
    instruction_text5 = instructions_font.render("Game ends when either player/AI reaches a score of 5.", True, WHITE)

    instructions_surface.blit(instruction_text, (50, 50))
    instructions_surface.blit(instruction_text2, (50, 100))
    instructions_surface.blit(instruction_text3, (50, 150))
    instructions_surface.blit(instruction_text4, (50, 200))
    instructions_surface.blit(instruction_text5, (50, 250))
    
def show_game_over():
    #displays game over screen in proper font and position
    game_over_font = pygame.font.Font(None, 36)
    winner_text = game_over_font.render(f"Game over! {'Player A' if left_score == 5 else 'Player B'} has won!", True, WHITE)
    return_text = game_over_font.render("Press P to return to the main menu.", True, WHITE)

    game_over_surface.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, 150))
    game_over_surface.blit(return_text, (WIDTH // 2 - return_text.get_width() // 2, 200))

# Game loop (TN)
while True:
    for event in pygame.event.get():
        #if quit is pressed, game ends and exits
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #if a key is pressed, program considers if user wants to play, display instructions, etc.
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                elif event.key == pygame.K_i:
                    game_state = INSTRUCTIONS
            elif game_state == INSTRUCTIONS:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU
            elif game_state == PLAYING:
                if event.key == pygame.K_a:
                    game_mode = (game_mode + 1) % 2
                elif event.key == pygame.K_p and (left_score == 5 or right_score == 5):
                    game_state = GAME_OVER
            elif game_state == GAME_OVER:
                if event.key == pygame.K_p:
                    left_score = 0
                    right_score = 0
                    game_state = MENU

    # Clear the surfaces (TN)
    menu_surface.fill((0, 0, 0))
    instructions_surface.fill((0, 0, 0))
    playing_surface.fill((0, 0, 0))
    game_over_surface.fill((0, 0, 0))

    #the following statements evaluate whether the game state displays menu, instructions, playthrough, etc.
    if game_state == MENU:
        show_menu()
        game_over_displayed = False  # Reset the flag when returning to the menu (JS)
        screen.blit(menu_surface, (0, 0))
    elif game_state == INSTRUCTIONS:
        show_instructions()
        game_over_displayed = False  # Reset the flag when going to instructions (JS)
        screen.blit(instructions_surface, (0, 0))
    elif game_state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and right_paddle_pos[1] > 0 and game_mode == 0:  # Disable control in Player vs AI mode (JS)
            right_paddle_pos[1] -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT and game_mode == 0:  # Disable control in Player vs AI mode (JS)
            right_paddle_pos[1] += paddle_speed
        if keys[pygame.K_w] and left_paddle_pos[1] > 0:
            left_paddle_pos[1] -= paddle_speed
        if keys[pygame.K_s] and left_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT:
            left_paddle_pos[1] += paddle_speed
            
        if keys[pygame.K_d]: #toggle ai difficulty
            ai_difficulty = (ai_difficulty + 1) % 2
        
        if game_mode == 1:
            #evaluates how difficult ai mode is set
            if ai_difficulty == 0:    
                if ball_pos[1] < right_paddle_pos[1] + PADDLE_HEIGHT // 2:
                    right_paddle_pos[1] -= paddle_speed
                elif ball_pos[1] > right_paddle_pos[1] + PADDLE_HEIGHT // 2:
                    right_paddle_pos[1] += paddle_speed
            elif ai_difficulty == 1:
                if ball_pos[1] < right_paddle_pos[1] + PADDLE_HEIGHT // 2:
                    right_paddle_pos[1] -= paddle_speed * 1.5
                elif ball_pos[1] > right_paddle_pos[1] + PADDLE_HEIGHT // 2:
                    right_paddle_pos[1] += paddle_speed * 1.5


        #the following reassigns the spped and position of ball
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        #the following evaluates whether the ball has hit the paddle
        if (
            left_paddle_pos[0] <= ball_pos[0] <= left_paddle_pos[0] + PADDLE_WIDTH and
            left_paddle_pos[1] <= ball_pos[1] <= left_paddle_pos[1] + PADDLE_HEIGHT
        ) or (
            right_paddle_pos[0] <= ball_pos[0] <= right_paddle_pos[0] + PADDLE_WIDTH and
            right_paddle_pos[1] <= ball_pos[1] <= right_paddle_pos[1] + PADDLE_HEIGHT
        ):
            ball_speed[0] = -ball_speed[0]

        #if ball is scored on a side, the corresponding side will add a point to the scoring
        if ball_pos[0] <= 0:
            right_score += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]
        elif ball_pos[0] >= WIDTH:
            left_score += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]

        #the following evaluates whether score is 5. if so, then game ends
        if left_score == 5 or right_score == 5:
            game_state = GAME_OVER
    elif game_state == GAME_OVER:
        if not game_over_displayed:
            show_game_over()
            screen.blit(game_over_surface, (0, 0))
            game_over_displayed = True  # Set the flag when the game-over screen is displayed (JS)

    # Draw game objects (JS)
    draw_objects()
    if game_state == PLAYING:
        screen.blit(playing_surface, (0, 0))

    #the following permits the screen to be refreshed
    pygame.display.flip()
    #the following counts time during the game
    pygame.time.Clock().tick(60)
