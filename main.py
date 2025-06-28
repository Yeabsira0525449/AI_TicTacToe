import sys
import pygame
import numpy as np


class TicTacToe:
    """A Tic Tac Toe game implementation using Pygame."""
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # Dimensions
    WIDTH = 300
    HEIGHT = 300
    LINE_WIDTH = 5
    BOARD_ROWS = 3
    BOARD_COLS = 3
    SQUARE_SIZE = WIDTH // BOARD_COLS
    CIRCLE_RADIUS = SQUARE_SIZE // 3
    CIRCLE_WIDTH = 15
    CROSS_WIDTH = 15
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Tic Tac Toe')
        self.screen.fill(self.BLACK)
        
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS))
        self.current_player = 1
        
    def draw_lines(self):
        """Draw the grid lines on the screen."""
        for i in range(1, self.BOARD_ROWS):
            # Horizontal lines
            pygame.draw.line(
                self.screen, 
                self.WHITE, 
                (0, self.SQUARE_SIZE * i), 
                (self.WIDTH, self.SQUARE_SIZE * i), 
                self.LINE_WIDTH
            )
            # Vertical lines
            pygame.draw.line(
                self.screen, 
                self.WHITE, 
                (self.SQUARE_SIZE * i, 0), 
                (self.SQUARE_SIZE * i, self.HEIGHT), 
                self.LINE_WIDTH
            )
    
    def draw_figures(self, color=None):
        """Draw X and O figures on the board."""
        if color is None:
            color = self.WHITE
            
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                center_y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                
                if self.board[row][col] == 1:
                    # Draw circle (O)
                    pygame.draw.circle(
                        self.screen, 
                        color,
                        (center_x, center_y),
                        self.CIRCLE_RADIUS, 
                        self.CIRCLE_WIDTH
                    )
                elif self.board[row][col] == 2:
                    # Draw cross (X)
                    offset = self.SQUARE_SIZE // 4
                    start_x = col * self.SQUARE_SIZE + offset
                    start_y = row * self.SQUARE_SIZE + offset
                    end_x = col * self.SQUARE_SIZE + 3 * offset
                    end_y = row * self.SQUARE_SIZE + 3 * offset
                    
                    # Main diagonal line
                    pygame.draw.line(
                        self.screen, 
                        color,
                        (start_x, start_y),
                        (end_x, end_y),
                        self.CROSS_WIDTH
                    )
                    # Anti-diagonal line
                    pygame.draw.line(
                        self.screen, 
                        color,
                        (start_x, end_y),
                        (end_x, start_y),
                        self.CROSS_WIDTH
                    )
    
    def mark_square(self, row, col, player):
        """Mark a square on the board for the specified player."""
        if self.available_square(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def available_square(self, row, col):
        """Check if a square is available (empty)."""
        return self.board[row][col] == 0
    
    def is_board_full(self):
        """Check if the board is completely filled."""
        return not np.any(self.board == 0)
    
    def check_winner(self, player):
        """Check if the specified player has won."""
        # Check rows
        for row in range(self.BOARD_ROWS):
            if np.all(self.board[row, :] == player):
                return True
        
        # Check columns
        for col in range(self.BOARD_COLS):
            if np.all(self.board[:, col] == player):
                return True
        
        # Check main diagonal
        if np.all(np.diag(self.board) == player):
            return True
        
        # Check anti-diagonal
        if np.all(np.diag(np.fliplr(self.board)) == player):
            return True
        
        return False
    
    def get_winning_line(self, player):
        """Get the coordinates for drawing the winning line."""
        # Check rows
        for row in range(self.BOARD_ROWS):
            if np.all(self.board[row, :] == player):
                start = (0, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                end = (self.WIDTH, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                return (start, end)
        
        # Check columns
        for col in range(self.BOARD_COLS):
            if np.all(self.board[:, col] == player):
                start = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, 0)
                end = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, self.HEIGHT)
                return (start, end)
        
        # Check main diagonal
        if np.all(np.diag(self.board) == player):
            return ((0, 0), (self.WIDTH, self.HEIGHT))
        
        # Check anti-diagonal
        if np.all(np.diag(np.fliplr(self.board)) == player):
            return ((self.WIDTH, 0), (0, self.HEIGHT))
        
        return None
    
    def get_clicked_square(self, mouse_pos):
        """Convert mouse position to board coordinates."""
        col = mouse_pos[0] // self.SQUARE_SIZE
        row = mouse_pos[1] // self.SQUARE_SIZE
        return row, col
    
    def switch_player(self):
        """Switch to the next player."""
        self.current_player = 2 if self.current_player == 1 else 1
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS))
        self.current_player = 1
        self.screen.fill(self.BLACK)
        self.draw_lines()
    
    def run(self):
        """Main game loop."""
        self.draw_lines()
        running = True
        game_over = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_square(mouse_pos)
                    
                    if self.mark_square(row, col, self.current_player):
                        if self.check_winner(self.current_player):
                            game_over = True
                        elif self.is_board_full():
                            game_over = True  # Tie game
                        else:
                            self.switch_player()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press 'R' to restart
                        self.reset_game()
                        game_over = False
            
            self.draw_figures()
            pygame.display.update()
        
        pygame.quit()
        sys.exit()


# Usage
if __name__ == "__main__":
    game = TicTacToe()
    game.run()
