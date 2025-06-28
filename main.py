import sys
import pygame
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dimensions
width = 300
height = 300
line_width = 5
board_rows = 3
board_cols = 3
square_size = width // board_cols
circle_radius = square_size // 3
circle_width = 15
cross_width = 15


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BLACK)


board = np.zeros((board_rows, board_cols))
player = 1


def draw_lines():
    for i in range(1, board_rows):
        pygame.draw.line(screen, WHITE, (0, square_size * i), (width, square_size * i), line_width)
        pygame.draw.line(screen, WHITE, (square_size * i, 0), (square_size * i, height), line_width)

def draw_figures():
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, WHITE, (col * square_size + square_size // 2, row * square_size + square_size // 2), circle_radius, circle_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, WHITE, (col * square_size + square_size // 4, row * square_size + square_size // 4), (col * square_size + 3 * square_size // 4, row * square_size + 3 * square_size // 4), cross_width)
                pygame.draw.line(screen, WHITE, (col * square_size + square_size // 4, row * square_size + 3 * square_size // 4), (col * square_size + 3 * square_size // 4, row * square_size + square_size // 4), cross_width)


# Draw O and X
def draw_figures(color=WHITE):
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color,
                                   (int(col * square_size + square_size // 2), int(row * square_size + square_size // 2)),
                                   circle_radius, circle_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                                 (col * square_size + square_size // 4, row * square_size + square_size // 4),
                                 (col * square_size + 3 * square_size // 4, row * square_size + 3 * square_size // 4),
                                 cross_width)
                pygame.draw.line(screen, color,
                                 (col * square_size + square_size // 4, row * square_size + 3 * square_size // 4),
                                 (col * square_size + 3 * square_size // 4, row * square_size + square_size // 4),
                                 cross_width)

