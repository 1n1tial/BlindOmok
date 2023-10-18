try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

import pygame
import sys
import random
import os


# Constants
GRID_SIZE = 25
GRID_WIDTH = 25
GRID_HEIGHT = 25
WINDOW_SIZE = (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
LINE_COLOR = (0, 0, 0)
GRID_COLOR = (179, 116, 9)
PLAYER_X_COLOR = PLAYER_O_COLOR = random.choice([(0, 0, 0), (255, 255, 255)])
PLAYER_X = "X"
PLAYER_O = "O"

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Blind Omok")

# Create the game board
board = [["." for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_player = PLAYER_X
winner = None

# Function to draw the game board
def draw_board():
    screen.fill(GRID_COLOR)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, LINE_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            if board[y][x] == PLAYER_X:
                pygame.draw.circle(screen, PLAYER_X_COLOR, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 2)
            elif board[y][x] == PLAYER_O:
                pygame.draw.circle(screen, PLAYER_O_COLOR, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 2)

    if winner:
        screen.fill(GRID_COLOR)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(screen, LINE_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                if board[y][x] == PLAYER_X:
                    pygame.draw.circle(screen, (0,0,0), (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 2)
                elif board[y][x] == PLAYER_O:
                    pygame.draw.circle(screen, (255,255,255), (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 2)
        
        num = 1 if winner == PLAYER_X else 2
        font = pygame.font.Font(None, 50)
        text = font.render(f"Player {num} wins!", True, (255,0,0))
        screen.blit(text, (WINDOW_SIZE[0] // 2 - 120, WINDOW_SIZE[1] // 2 - 40))

        restart_button = pygame.draw.rect(screen, (0, 255, 0), (WINDOW_SIZE[0] // 2 - 50, WINDOW_SIZE[1] // 2 + 40, 100, 30))
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, (0, 0, 0))
        screen.blit(text, (WINDOW_SIZE[0] // 2 - 40, WINDOW_SIZE[1] // 2 + 45))
        pygame.display.update()
        return restart_button
    else:
        pygame.display.update()
        return None

# Check for a win condition
def check_win(x, y):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for i in range(1, 5):
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and board[ny][nx] == current_player:
                count += 1
            else:
                break
        for i in range(1, 5):
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and board[ny][nx] == current_player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

# Main game loop
restart = False
running = True
while running:
    draw_board()
    if restart:
        board = [["." for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        current_player = PLAYER_X
        winner = None
        restart = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not winner:
            x, y = event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and board[y][x] == ".":
                board[y][x] = current_player
                if check_win(x, y):
                    winner = current_player
                else:
                    current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
        elif event.type == pygame.MOUSEBUTTONDOWN and winner:
            restart_button = draw_board()
            if restart_button and restart_button.collidepoint(event.pos):
                restart = True

pygame.quit()
sys.exit()
