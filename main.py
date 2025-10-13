import pygame
import random
import sys

from game import (
    get_starting_position,
    simple_next_black_move,
    process_white_human_move,
)

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backgammon Board")
PIECE_RADIUS = 20
global position
position = get_starting_position()

# Colors
TABLE_GREEN = (34, 139, 34)
BOARD_LIGHT = (240, 230, 200)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (200, 50, 50)
GREY = (180, 180, 180)

font = pygame.font.SysFont(None, 48)

# Layout
MARGIN = 60
BOARD_WIDTH = WIDTH - 2 * MARGIN
TRIANGLE_WIDTH = BOARD_WIDTH // 12
TRIANGLE_HEIGHT = HEIGHT // 2 - 60

# ---- Dummy processing function ----
def process_human_move(dice_value, p):
    global position
    if p != "BAR":
        if p <= 12:
            p = 13 - p
        else:
            p = 24 + 13 - p
    position_option = process_white_human_move(position[0], position[1], position[2], dice_value, str(p))
    if position_option:
        position = position_option
    print(f"process_human_move called with dice={dice_value}, position={p}")


# ---- Board setup ----
triangles = []
triangle_positions = []  # (points, rect, point_number)

# Upper row (points 13–24)
for i in range(12):
    x = MARGIN + i * TRIANGLE_WIDTH
    top = MARGIN
    points = [
        (x, top),
        (x + TRIANGLE_WIDTH, top),
        (x + TRIANGLE_WIDTH / 2, top + TRIANGLE_HEIGHT),
    ]
    triangles.append(points)
    rect = pygame.Rect(x, top, TRIANGLE_WIDTH, TRIANGLE_HEIGHT)
    point_num = 24 - i
    triangle_positions.append((points, rect, point_num))

# Lower row (points 12–1)
for i in range(12):
    x = MARGIN + i * TRIANGLE_WIDTH
    bottom = HEIGHT - MARGIN
    points = [
        (x, bottom),
        (x + TRIANGLE_WIDTH, bottom),
        (x + TRIANGLE_WIDTH / 2, bottom - TRIANGLE_HEIGHT),
    ]
    triangles.append(points)
    rect = pygame.Rect(x, bottom - TRIANGLE_HEIGHT, TRIANGLE_WIDTH, TRIANGLE_HEIGHT)
    point_num = i + 1
    triangle_positions.append((points, rect, point_num))

# ---- Dice drawing ----
def draw_dice(surface, dice_values, selected_index=None):
    size = 60
    spacing = 20
    start_x = WIDTH // 2 - size - spacing // 2
    y = HEIGHT // 2 - size // 2
    dice_rects = []
    for i, val in enumerate(dice_values):
        rect = pygame.Rect(start_x + i * (size + spacing), y, size, size)
        color = YELLOW if i == selected_index else WHITE
        pygame.draw.rect(surface, color, rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, rect, 2)
        draw_dots(surface, rect, val)
        dice_rects.append(rect)
    return dice_rects


def draw_dots(surface, rect, val):
    cx, cy = rect.center
    r = 6
    offsets = {
        1: [(0, 0)],
        2: [(-15, -15), (15, 15)],
        3: [(-15, -15), (0, 0), (15, 15)],
        4: [(-15, -15), (-15, 15), (15, -15), (15, 15)],
        5: [(-15, -15), (-15, 15), (0, 0), (15, -15), (15, 15)],
        6: [(-15, -15), (-15, 0), (-15, 15), (15, -15), (15, 0), (15, 15)],
    }
    for ox, oy in offsets[val]:
        pygame.draw.circle(surface, BLACK, (cx + ox, cy + oy), r)


def draw_pieces(board):
    def draw_pieces_at_pos(point, color, count):
        if point <= 12:
            idx = 12 - point
            x = MARGIN + idx * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
            base_y = HEIGHT - MARGIN - PIECE_RADIUS - 5
            direction = -1
        else:
            idx = point - 13
            x = MARGIN + idx * TRIANGLE_WIDTH + TRIANGLE_WIDTH // 2
            base_y = MARGIN + PIECE_RADIUS + 5
            direction = 1

        for i in range(count):
            y = base_y + direction * i * (PIECE_RADIUS * 2 + 2)
            pygame.draw.circle(screen, color[0], (x, y), PIECE_RADIUS)
            pygame.draw.circle(screen, color[1], (x, y), PIECE_RADIUS, 2)

    for i, num in enumerate(board):
        if num == 0:
            continue
        color = [WHITE, BLACK] if num > 0 else [BLACK, WHITE]
        draw_pieces_at_pos(i + 1, color, abs(num))

def draw_bar_checkers(surface, white_bar_count, black_bar_count, bar_white_rect, bar_black_rect):
    """
    Draws white and black checkers stacked above their respective bars.
    """
    # Config
    spacing = PIECE_RADIUS * 2 + 4  # vertical spacing between pieces
    offset_y = 10  # vertical offset above the bar
    max_stack = 6  # if there are more than 6, just stack tighter

    # --- Draw white checkers (right bar) ---
    for i in range(white_bar_count):
        y = bar_white_rect.top - offset_y - i * spacing
        x = bar_white_rect.centerx
        pygame.draw.circle(surface, WHITE, (x, y), PIECE_RADIUS)
        pygame.draw.circle(surface, BLACK, (x, y), PIECE_RADIUS, 2)

    # --- Draw black checkers (left bar) ---
    for i in range(black_bar_count):
        y = bar_black_rect.bottom + offset_y + i * spacing
        x = bar_black_rect.centerx
        pygame.draw.circle(surface, BLACK, (x, y), PIECE_RADIUS)
        pygame.draw.circle(surface, WHITE, (x, y), PIECE_RADIUS, 2)


# ---- Initial state ----
dice_values = [random.randint(1, 6), random.randint(1, 6)]
selected_dice_index = None

# ---- UI elements ----
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 50, 200, 40)
bar_white_rect = pygame.Rect(WIDTH - 40, HEIGHT // 4, 30, HEIGHT // 2)
bar_black_rect = pygame.Rect(10, HEIGHT // 4, 30, HEIGHT // 2)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                dice_values = [random.randint(1, 6), random.randint(1, 6)]
                selected_dice_index = None

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # --- Check button click ---
            if button_rect.collidepoint(pos):
                d1 = random.randint(1, 6)
                d2 = random.randint(1, 6)
                print(f"Computer move called with {d1=}, {d2=}...")
                position = simple_next_black_move(position[0], position[1], position[2], d1, d2)
                print("finished")
            # --- Check dice click ---
            for i, rect in enumerate(draw_dice(screen, dice_values)):
                if rect.collidepoint(pos):
                    selected_dice_index = i
                    print(f"Selected dice {i} with value {dice_values[i]}")
                    break
            else:
                # --- Check bar click ---
                if bar_white_rect.collidepoint(pos):
                    if selected_dice_index is not None:
                        dice_value = dice_values[selected_dice_index]
                        process_human_move(dice_value, "BAR")
                        selected_dice_index = None
                    else:
                        print("Clicked white bar")

                # --- Check triangle click ---
                for points, rect, point_num in triangle_positions:
                    if rect.collidepoint(pos):
                        if selected_dice_index is not None:
                            dice_value = dice_values[selected_dice_index]
                            process_human_move(dice_value, point_num)
                            selected_dice_index = None
                        else:
                            print(f"Clicked point: {point_num}")

    # Draw background
    screen.fill(TABLE_GREEN)
    pygame.draw.rect(screen, BOARD_LIGHT, (MARGIN, MARGIN, BOARD_WIDTH, HEIGHT - 2 * MARGIN))

    # Triangles
    for i, (points, rect, point_num) in enumerate(triangle_positions):
        color = BROWN if i % 2 == 0 else BLACK
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, WHITE, points, 2)

    # Draw bars
    pygame.draw.rect(screen, GREY, bar_white_rect)
    pygame.draw.rect(screen, GREY, bar_black_rect)
    pygame.draw.rect(screen, BLACK, bar_white_rect, 2)
    pygame.draw.rect(screen, BLACK, bar_black_rect, 2)
    white_text = font.render("W", True, WHITE)
    black_text = font.render("B", True, BLACK)
    screen.blit(white_text, (bar_white_rect.x + 5, bar_white_rect.y - 30))
    screen.blit(black_text, (bar_black_rect.x + 5, bar_black_rect.y - 30))

    # Pieces
    draw_pieces(position[0])
    white_bar = position[1]
    black_bar = position[2]

    draw_bar_checkers(screen, white_bar, black_bar, bar_white_rect, bar_black_rect)

    # Dice
    dice_rects = draw_dice(screen, dice_values, selected_dice_index)

    # Computer Move Button
    pygame.draw.rect(screen, RED, button_rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    label = font.render("Comp Move", True, WHITE)
    screen.blit(label, (button_rect.x + 15, button_rect.y + 3))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
