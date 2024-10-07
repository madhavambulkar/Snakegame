import tkinter as tk
import random

# Constants
GAME_WIDTH = 600
GAME_HEIGHT = 400
SNAKE_SIZE = 20
SPEED = 100
BG_COLOR = "#000000"
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        # Create a canvas for the game
        self.canvas = tk.Canvas(self.root, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        # Set initial direction for snake (moving right)
        self.direction = "Right"

        # Create snake and food
        self.snake = [(100, 100), (80, 100), (60, 100)]  # Starting snake body (3 blocks)
        self.food = self.create_food()

        # Draw snake and food on canvas
        self.snake_blocks = [
            self.canvas.create_rectangle(*self.snake[0], self.snake[0][0] + SNAKE_SIZE, self.snake[0][1] + SNAKE_SIZE,
                                         fill=SNAKE_COLOR)]
        for block in self.snake[1:]:
            self.snake_blocks.append(
                self.canvas.create_rectangle(*block, block[0] + SNAKE_SIZE, block[1] + SNAKE_SIZE, fill=SNAKE_COLOR))
        self.food_block = self.canvas.create_rectangle(*self.food, self.food[0] + SNAKE_SIZE, self.food[1] + SNAKE_SIZE,
                                                       fill=FOOD_COLOR)

        # Start the game
        self.update()
        self.root.bind("<KeyPress>", self.on_key_press)

    def create_food(self):
        while True:
            x = random.randint(0, (GAME_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - SNAKE_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + SNAKE_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - SNAKE_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + SNAKE_SIZE, head_y)

        # Add new head and remove last block of the snake
        self.snake = [new_head] + self.snake[:-1]

    def update(self):
        if self.check_collision():
            self.end_game()
            return

        self.move_snake()

        # Check if snake has eaten food
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])  # Grow the snake
            self.canvas.delete(self.food_block)  # Remove the food
            self.food = self.create_food()  # Create new food
            self.food_block = self.canvas.create_rectangle(*self.food, self.food[0] + SNAKE_SIZE,
                                                           self.food[1] + SNAKE_SIZE, fill=FOOD_COLOR)

        self.redraw_snake()
        self.root.after(SPEED, self.update)

    def redraw_snake(self):
        # Delete old snake blocks
        for block in self.snake_blocks:
            self.canvas.delete(block)

        # Draw new snake blocks
        self.snake_blocks = []
        for block in self.snake:
            self.snake_blocks.append(
                self.canvas.create_rectangle(*block, block[0] + SNAKE_SIZE, block[1] + SNAKE_SIZE, fill=SNAKE_COLOR))

    def check_collision(self):
        head_x, head_y = self.snake[0]

        # Check for wall collisions
        if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
            return True

        # Check for collisions with self
        if len(self.snake) > 1 and (head_x, head_y) in self.snake[1:]:
            return True

        return False

    def on_key_press(self, event):
        new_direction = event.keysym
        all_directions = ["Up", "Down", "Left", "Right"]
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

        if new_direction in all_directions and new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def end_game(self):
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="GAME OVER", fill="red", font=("Arial", 24))
        self.root.unbind("<KeyPress>")


# Create the root window
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
