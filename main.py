import pygame
import sys

from game import get_starting_position
# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 600
BOARD_COLOR = (181, 101, 29)
TRIANGLE_LIGHT = (230, 200, 160)
TRIANGLE_DARK = (120, 60, 20)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

# Piece settings
PIECE_RADIUS = 20
BOARD_MARGIN = 50
TRIANGLE_WIDTH = (WIDTH - 2 * BOARD_MARGIN) // 12
TRIANGLE_HEIGHT = HEIGHT // 2 - 2 * BOARD_MARGIN

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backgammon Board (Initial Setup)")

# Draw triangles for points
def draw_board():
    screen.fill(BOARD_COLOR)

    # Draw 24 triangles (12 on top, 12 on bottom)
    for i in range(12):
        color = TRIANGLE_DARK if i % 2 == 0 else TRIANGLE_LIGHT

        # Top row triangles
        points_top = [
            (BOARD_MARGIN + i * TRIANGLE_WIDTH, BOARD_MARGIN),
            (BOARD_MARGIN + (i + 1) * TRIANGLE_WIDTH, BOARD_MARGIN),
            (BOARD_MARGIN + i * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2, BOARD_MARGIN + TRIANGLE_HEIGHT),
        ]
        pygame.draw.polygon(screen, color, points_top)

        # Bottom row triangles (reversed)
        color = TRIANGLE_LIGHT if i % 2 == 0 else TRIANGLE_DARK
        points_bottom = [
            (BOARD_MARGIN + i * TRIANGLE_WIDTH, HEIGHT - BOARD_MARGIN),
            (BOARD_MARGIN + (i + 1) * TRIANGLE_WIDTH, HEIGHT - BOARD_MARGIN),
            (BOARD_MARGIN + i * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2, HEIGHT - BOARD_MARGIN - TRIANGLE_HEIGHT),
        ]
        pygame.draw.polygon(screen, color, points_bottom)

    # Draw center bar
    pygame.draw.rect(screen, (100, 50, 0), (WIDTH // 2 - TRIANGLE_WIDTH // 4 - 4, BOARD_MARGIN, TRIANGLE_WIDTH // 2, HEIGHT - 2 * BOARD_MARGIN+1))


# Draw checkers (pieces)
def draw_pieces(board):
    def draw_pieces_at_pos(point, color, count):
        # print(point, color, count)
        # Determine triangle index and top/bottom half
        if point <= 12:
            # Bottom half, points 1–12 from right to left
            idx = 12 - point
            x = BOARD_MARGIN + idx * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
            base_y = HEIGHT - BOARD_MARGIN - PIECE_RADIUS - 5
            direction = -1
        else:
            # Top half, points 13–24 from left to right
            idx = point - 13
            x = BOARD_MARGIN + idx * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
            base_y = BOARD_MARGIN + PIECE_RADIUS + 5
            direction = 1

        # Draw stack of pieces
        for i in range(count):
            y = base_y + direction * i * (PIECE_RADIUS * 2 + 2)
            pygame.draw.circle(screen, color, (x, y), PIECE_RADIUS)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), PIECE_RADIUS, 2)

    for i, num in enumerate(board):
        if num == 0:
            continue
        color = WHITE if num > 0 else BLACK
        draw_pieces_at_pos(i+1, color, abs(num))
            


        

# Main loop
def main():
    position = get_starting_position()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board()
        draw_pieces(position[0])
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
