import pygame
import random

# Initialize Pygame
pygame.init()

# Set the window dimensions
width = 800
height = 600

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
orange = (255, 165, 0)
yellow = (255, 255, 0)
purple = (128, 0, 128)

# Set the Tetris grid dimensions
grid_size = 50
grid_width = width // grid_size
grid_height = height // grid_size

# Set the Tetris shape types and their corresponding colors
tetris_shapes = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1], [1, 1]],  # O-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1, 0], [0, 1, 1]],  # S-shape
    [[0, 1, 1], [1, 1, 0]],  # Z-shape
    [[1, 1, 1], [1, 0, 0]],  # J-shape
    [[1, 1, 1], [0, 0, 1]],  # L-shape
]

# Create the Tetris window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris Game')

clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)


def draw_grid():
    for x in range(0, width, grid_size):
        pygame.draw.line(window, white, (x, 0), (x, height))
    for y in range(0, height, grid_size):
        pygame.draw.line(window, white, (0, y), (width, y))


def draw_tetromino(tetromino, x, y, color):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                pygame.draw.rect(window, color, (x + col * grid_size, y + row * grid_size, grid_size, grid_size))


def check_collision(tetromino, x, y, grid):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                if x + col < 0 or x + col >= grid_width or y + row >= grid_height or grid[y + row][x + col]:
                    return True
    return False


def rotate_tetromino(tetromino):
    return list(zip(*reversed(tetromino)))


def clear_rows(grid):
    full_rows = [row for row in range(grid_height) if all(grid[row])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [0] * grid_width)


def game_over_screen(score):
    game_over_text = font_style.render("Game Over", True, red)
    score_text = score_font.render("Score: " + str(score), True, white)
    window.blit(game_over_text, (width / 2 - game_over_text.get_width() / 2, height / 3))
    window.blit(score_text, (width / 2 - score_text.get_width() / 2, height / 2))


def game_loop():
    grid = [[0] * grid_width for _ in range(grid_height)]
    score = 0

    tetromino = random.choice(tetris_shapes)
    tetromino_color = random.choice([cyan, orange, yellow, purple, green, blue, red])
    tetromino_x = grid_width // 2 - len(tetromino[0]) // 2
    tetromino_y = 0

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(tetromino, tetromino_x - 1, tetromino_y, grid):
                        tetromino_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(tetromino, tetromino_x + 1, tetromino_y, grid):
                        tetromino_x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(tetromino, tetromino_x, tetromino_y + 1, grid):
                        tetromino_y += 1
                elif event.key == pygame.K_UP:
                    rotated_tetromino = rotate_tetromino(tetromino)
                    if not check_collision(rotated_tetromino, tetromino_x, tetromino_y, grid):
                        tetromino = rotated_tetromino

        if not check_collision(tetromino, tetromino_x, tetromino_y + 1, grid):
            tetromino_y += 1
        else:
            for row in range(len(tetromino)):
                for col in range(len(tetromino[row])):
                    if tetromino[row][col]:
                        grid[tetromino_y + row][tetromino_x + col] = 1

            clear_rows(grid)
            score += 10

            tetromino = random.choice(tetris_shapes)
            tetromino_color = random.choice([cyan, orange, yellow, purple, green, blue, red])
            tetromino_x = grid_width // 2 - len(tetromino[0]) // 2
            tetromino_y = 0

            if check_collision(tetromino, tetromino_x, tetromino_y, grid):
                game_over = True

        window.fill(black)

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col]:
                    pygame.draw.rect(window, white, (col * grid_size, row * grid_size, grid_size, grid_size))

        draw_tetromino(tetromino, tetromino_x * grid_size, tetromino_y * grid_size, tetromino_color)

        draw_grid()

        pygame.display.update()

        clock.tick(5)

    game_over_screen(score)
    pygame.display.update()
    pygame.time.wait(2000)

    pygame.quit()


# Start the game
game_loop()
