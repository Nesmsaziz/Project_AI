import pygame
from collections import deque
import random


rows, cols = 12, 12
tile_size = 50


treasure_count = 5


pygame.init()
win_width = cols * tile_size
win_height = rows * tile_size + 100
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption(" BFS Treasures Hunt")


try:
    player_img = pygame.transform.scale(pygame.image.load('player.jpg'), (tile_size, tile_size))
    treasure_img = pygame.transform.scale(pygame.image.load('treasure.jpg'), (tile_size, tile_size))
    wall_img = pygame.transform.scale(pygame.image.load('wall.jpg'), (tile_size, tile_size))
    empty_img = pygame.transform.scale(pygame.image.load('background.jpeg'), (tile_size, tile_size))
    has_images = True
except:
    has_images = False
    print("Images not found, using shapes instead")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
GRASS = (100, 200, 100)

font = pygame.font.SysFont(None, 36)

def generate_random_grid():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    # Place walls randomly
    for i in range(rows):
        for j in range(cols):
            if random.random() < 0.2:
                grid[i][j] = 1  # Wall
    # Place treasures randomly
    placed = 0
    while placed < treasure_count:
        i, j = random.randrange(rows), random.randrange(cols)
        if grid[i][j] == 0:
            grid[i][j] = 2  # Treasure
            placed += 1
    # Ensure start position is empty
    grid[0][0] = 0
    return grid


def draw(grid, path=set(), current=None, message=None):
    # Clear game area
    win.fill(WHITE)
    # Draw grid
    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
            bg = empty_img if has_images else None
            if bg:
                win.blit(bg, rect)
            else:
                pygame.draw.rect(win, GRASS, rect)

            val = grid[i][j]
            if has_images:
                if val == 1:
                    win.blit(wall_img, rect)
                elif val == 2:
                    win.blit(treasure_img, rect)
            else:
                if val == 1:
                    pygame.draw.rect(win, GREY, rect)
                elif val == 2:
                    pygame.draw.rect(win, YELLOW, rect)

            if (i, j) in path:
                pygame.draw.rect(win, BLUE, rect, 3)

    # Draw player
    if current:
        pr, pc = current
        rect = pygame.Rect(pc * tile_size, pr * tile_size, tile_size, tile_size)
        if has_images:
            win.blit(player_img, rect)
        else:
            pygame.draw.circle(win, BLUE, rect.center, tile_size // 3)

    # Draw message box
    if message:
        box_w = win_width * 0.8
        box_h = 60
        box_x = (win_width - box_w) / 2
        box_y = rows * tile_size + 20
        # semi-transparent background
        s = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        win.blit(s, (box_x, box_y))
        # border
        pygame.draw.rect(win, YELLOW, (box_x, box_y, box_w, box_h), 3, border_radius=10)
        # text
        text = font.render(message, True, YELLOW)
        txt_x = box_x + (box_w - text.get_width()) / 2
        txt_y = box_y + (box_h - text.get_height()) / 2
        win.blit(text, (txt_x, txt_y))

    pygame.display.flip()


def bfs(grid, start):
    queue = deque([(start, [start])])
    visited = set([start])
    while queue:
        (r, c), path = queue.popleft()
        if grid[r][c] == 2:
            return path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid[nr][nc] != 1:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
    return None


def main():
    clock = pygame.time.Clock()
    grid = generate_random_grid()
    player = (0, 0)
    path = bfs(grid, player)
    running = True
    game_over = False
    treasures_collected = 0

    while running:
        clock.tick(5)
        # Move player along path
        if not game_over:
            if path:
                player = path.pop(0)
            if player and grid[player[0]][player[1]] == 2:
                treasures_collected += 1
                grid[player[0]][player[1]] = 0
                if treasures_collected == treasure_count:
                    game_over = True
                else:
                    path = bfs(grid, player)
            elif not path:
                game_over = True

        message = None
        if game_over and treasures_collected == treasure_count:
            message = "You Win! Press R to Restart"
        elif game_over:
            message = "No Path Found. Press R to Restart"

        draw(grid, path if path else set(), current=player, message=message)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                grid = generate_random_grid()
                player = (0, 0)
                path = bfs(grid, player)
                treasures_collected = 0
                game_over = False

    pygame.quit()

if __name__ == "__main__":
    main()
