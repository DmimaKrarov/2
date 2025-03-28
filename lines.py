import pygame

class Board:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

                if self.grid[y][x] == "blue":
                    pygame.draw.circle(screen, (0, 0, 255), rect.center, self.cell_size // 2 - 1)
                elif self.grid[y][x] == "red":
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, self.cell_size // 2 - 1)

class Lines(Board):
    def __init__(self, width, height, cell_size):
        super().__init__(width, height, cell_size)
        self.selected = None

    def has_path(self, x1, y1, x2, y2):
        if self.grid[y2][x2] is not None:
            return False

        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        stack = [(x1, y1)]
        visited[y1][x1] = True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) == (x2, y2):
                return True

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and not visited[ny][nx] and self.grid[ny][nx] is None:
                    visited[ny][nx] = True
                    stack.append((nx, ny))

        return False

    def handle_click(self, x, y):
        if self.grid[y][x] is None:
            if self.selected is None:
                self.grid[y][x] = "blue"
            else:
                sx, sy = self.selected
                if self.has_path(sx, sy, x, y):
                    self.grid[sy][sx] = None
                    self.grid[y][x] = "blue"
                    self.selected = None
        elif self.grid[y][x] == "blue":
            self.selected = (x, y)
            self.grid[y][x] = "red"
        elif self.grid[y][x] == "red":
            self.grid[y][x] = "blue"
            self.selected = None

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Линеечки")
clock = pygame.time.Clock()

cell_size = 60
board_width, board_height = 10, 10
lines = Lines(board_width, board_height, cell_size)

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            x, y = mouse_x // cell_size, mouse_y // cell_size
            if 0 <= x < board_width and 0 <= y < board_height:
                lines.handle_click(x, y)

    lines.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()