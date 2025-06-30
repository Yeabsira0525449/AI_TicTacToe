import sys
import pygame
import numpy as np
import math
import time

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Board and window dimensions
board_size = 300
button_area = 60  # Height reserved for the button
width = board_size
height = board_size + button_area

line_width = 5
board_rows = 3
board_cols = 3
square_size = board_size // board_cols
circle_radius = square_size // 3
circle_width = 15
cross_width = 15

# Button properties
button_radius = 20
button_center = (width // 2, button_area // 2)
button_animating = False  # Flag for button animation
button_anim_start = 0
button_anim_duration = 0.25  # Duration of animation in seconds

# Screen setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BLACK)

# Game board
board = np.zeros((board_rows, board_cols))

def draw_lines(color=WHITE):
    for i in range(1, board_rows):
        pygame.draw.line(screen, color, (0, button_area + square_size * i), (width, button_area + square_size * i), line_width)
        pygame.draw.line(screen, color, (square_size * i, button_area), (square_size * i, button_area + board_size), line_width)

def draw_figures(color=WHITE):
    for row in range(board_rows):
        for col in range(board_cols):
            center_x = int(col * square_size + square_size // 2)
            center_y = int(row * square_size + square_size // 2 + button_area)
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (center_x, center_y), circle_radius, circle_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                    (col * square_size + square_size // 4, row * square_size + square_size // 4 + button_area),
                    (col * square_size + 3 * square_size // 4, row * square_size + 3 * square_size // 4 + button_area),
                    cross_width)
                pygame.draw.line(screen, color,
                    (col * square_size + square_size // 4, row * square_size + 3 * square_size // 4 + button_area),
                    (col * square_size + 3 * square_size // 4, row * square_size + square_size // 4 + button_area),
                    cross_width)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    return not np.any(check_board == 0)

def get_winning_line(player, check_board=board):
    for col in range(board_cols):
        if np.all(check_board[:, col] == player):
            start = (col * square_size + square_size // 2, button_area)
            end = (col * square_size + square_size // 2, button_area + board_size)
            return (start, end)
    for row in range(board_rows):
        if np.all(check_board[row, :] == player):
            start = (0, button_area + row * square_size + square_size // 2)
            end = (width, button_area + row * square_size + square_size // 2)
            return (start, end)
    if check_board[0][0] == check_board[1][1] == check_board[2][2] == player:
        return ((0, button_area), (width, button_area + board_size))
    if check_board[0][2] == check_board[1][1] == check_board[2][0] == player:
        return ((width, button_area), (0, button_area + board_size))
    return None

def check_win(player, check_board=board):
    return get_winning_line(player, check_board) is not None

def minimax_ab(minimax_board, depth, is_maximizing, alpha, beta):
    if check_win(2, minimax_board):  # AI wins
        return float('inf') - depth
    elif check_win(1, minimax_board):  # Human wins
        return float('-inf') + depth
    elif is_board_full(minimax_board):
        return 0  # Draw
    if is_maximizing:
        max_eval = float('-inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2  # AI move
                    eval = minimax_ab(minimax_board, depth + 1, False, alpha, beta)
                    minimax_board[row][col] = 0  # Undo move
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1  # Human move
                    eval = minimax_ab(minimax_board, depth + 1, True, alpha, beta)
                    minimax_board[row][col] = 0  # Undo move
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def draw_refresh_icon(center, radius, color, thickness=3, angle=0):
    # Draw a simple refresh icon (circular arrow)
    points = []
    for i in range(0, 360, 30):
        rad = math.radians(i + angle)
        x = center[0] + radius * math.cos(rad)
        y = center[1] + radius * math.sin(rad)
        points.append((x, y))
    pygame.draw.lines(screen, color, True, points, thickness)

def draw_refresh_button(anim_progress=0):
    # anim_progress: 0 (normal) to 1 (fully animated)
    scale = 1 + 0.15 * anim_progress
    anim_radius = int(button_radius * scale)
    # Draw button background
    pygame.draw.circle(screen, GRAY, button_center, anim_radius)
    pygame.draw.circle(screen, WHITE, button_center, anim_radius, 2)
    # Draw refresh icon with animation
    draw_refresh_icon(button_center, anim_radius - 4, BLACK, thickness=3, angle=anim_progress * 360)
    return pygame.Rect(button_center[0] - anim_radius, button_center[1] - anim_radius, anim_radius * 2, anim_radius * 2)

# Main loop
running = True
while running:
    screen.fill(BLACK)
    draw_lines()
    draw_figures()
    
    # Draw refresh button with animation if active
    if button_animating:
        elapsed_time = (time.time() - button_anim_start) / button_anim_duration
        if elapsed_time < 1:
            draw_refresh_button(elapsed_time)  # Animate button
        else:
            button_animating = False  # Reset animation flag
    else:
        draw_refresh_button()  # Draw static button

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if mouse_y < button_area:  # Clicked in the button area
                button_animating = True  # Start button animation
                button_anim_start = time.time()  # Record the start time
            else:
                row = (mouse_y - button_area) // square_size
                col = mouse_x // square_size
                if available_square(row, col):
                    mark_square(row, col, 1)  # Human player
                    if not is_board_full():
                        # AI move (to be implemented)
                        pass

    pygame.display.flip()

pygame.quit()
sys.exit()