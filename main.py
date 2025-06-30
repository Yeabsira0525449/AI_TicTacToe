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
button_animating = False
button_anim_start = 0
button_anim_duration = 0.25  # seconds

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
    if check_win(2, minimax_board):
        return float('inf') - depth
    elif check_win(1, minimax_board):
        return float('-inf') + depth
    elif is_board_full(minimax_board):
        return 0
    if is_maximizing:
        max_eval = float('-inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    eval = minimax_ab(minimax_board, depth + 1, False, alpha, beta)
                    minimax_board[row][col] = 0
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
                    minimax_board[row][col] = 1
                    eval = minimax_ab(minimax_board, depth + 1, True, alpha, beta)
                    minimax_board[row][col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move():
    best_score = float('-inf')
    move = (-1, -1)
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax_ab(board, 0, False, float('-inf'), float('inf'))
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0

def draw_refresh_icon(center, radius, color, thickness=3, angle=0):
    # Draw a sharp refresh icon (arc + arrow)
    arc_rect = pygame.Rect(center[0] - radius + 2, center[1] - radius + 2, 2 * (radius - 2), 2 * (radius - 2))
    start_angle = math.radians(40 + angle)
    end_angle = math.radians(320 + angle)
    pygame.draw.arc(screen, color, arc_rect, start_angle, end_angle, thickness)
    # Arrowhead
    arrow_angle = end_angle
    arrow_length = radius * 0.7
    tip = (
        int(center[0] + arrow_length * math.cos(arrow_angle)),
        int(center[1] + arrow_length * math.sin(arrow_angle))
    )
    left = (
        int(tip[0] - 8 * math.cos(arrow_angle - math.pi / 8)),
        int(tip[1] - 8 * math.sin(arrow_angle - math.pi / 8))
    )
    right = (
        int(tip[0] - 8 * math.cos(arrow_angle + math.pi / 8)),
        int(tip[1] - 8 * math.sin(arrow_angle + math.pi / 8))
    )
    pygame.draw.polygon(screen, color, [tip, left, right])

def draw_refresh_button(anim_progress=0):
    # anim_progress: 0 (normal) to 1 (fully animated)
    scale = 1 + 0.15 * anim_progress
    anim_radius = int(button_radius * scale)
    # Draw button background
    pygame.draw.circle(screen, GRAY, button_center, anim_radius)
    pygame.draw.circle(screen, WHITE, button_center, anim_radius, 2)
    # Draw crisp refresh icon
    draw_refresh_icon(button_center, anim_radius - 4, BLACK, thickness=3, angle=anim_progress * 360)
    return pygame.Rect(button_center[0] - anim_radius, button_center[1] - anim_radius, anim_radius * 2, anim_radius * 2)

draw_lines()
player = 1
game_over = False
winner_line = None
winner_color = WHITE

# Animation state
button_animating = False
button_anim_start = 0

clock = pygame.time.Clock()

while True:
    anim_progress = 0
    if button_animating:
        elapsed = time.time() - button_anim_start
        anim_progress = min(1, elapsed / button_anim_duration)
        if elapsed > button_anim_duration:
            button_animating = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            button_rect = draw_refresh_button(anim_progress)
            if button_rect.collidepoint(mouse_pos):
                button_animating = True
                button_anim_start = time.time()
                restart_game()
                game_over = False
                winner_line = None
                winner_color = WHITE
                player = 1
                continue  # Don't process as a board click

            if not game_over:
                if mouse_pos[1] >= button_area:
                    mouseX = mouse_pos[0] // square_size
                    mouseY = (mouse_pos[1] - button_area) // square_size
                    if 0 <= mouseX < board_cols and 0 <= mouseY < board_rows:
                        if available_square(mouseY, mouseX):
                            mark_square(mouseY, mouseX, player)
                            draw_figures()
                            pygame.display.update()

                            if check_win(player):
                                winner_line = get_winning_line(player)
                                winner_color = GREEN
                                game_over = True
                            else:
                                player = player % 2 + 1
                                pygame.time.delay(500)
                                if not game_over:
                                    if best_move():
                                        draw_figures()
                                        pygame.display.update()
                                        if check_win(2):
                                            winner_line = get_winning_line(2)
                                            winner_color = RED
                                            game_over = True
                                        else:
                                            player = player % 2 + 1

                            if is_board_full() and not game_over:
                                winner_color = BLUE
                                game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                winner_line = None
                winner_color = WHITE
                player = 1

    screen.fill(BLACK)
    draw_lines()
    draw_figures()
    draw_refresh_button(anim_progress)

    if winner_line:
        pygame.draw.line(screen, winner_color, winner_line[0], winner_line[1], line_width * 2)
    elif game_over and winner_color == BLUE:
        draw_lines(color=BLUE)

    pygame.display.update()
    clock.tick(60)
