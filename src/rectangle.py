import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Constants for the overall space
SPACE_WIDTH = 100
SPACE_HEIGHT = 100

# Class to represent a rectangle
class RectangleData:
    def __init__(self, width, height, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rotated = False

    def rotate(self):
        self.width, self.height = self.height, self.width
        self.rotated = True

    def overlaps(self, other):
        # Check for overlap with another rectangle with 1 unit separation
        return not (self.x + self.width + 1 <= other.x or
                    self.x >= other.x + other.width + 1 or
                    self.y + self.height + 1 <= other.y or
                    self.y >= other.y + other.height + 1)

# Function to attempt to place a rectangle
def place_rectangle(rect, available_space, placed_rectangles):
    x, y, width, height = available_space
    if rect.width > width or rect.height > height:
        return False  # Rectangle doesn't fit

    # Try to find a position in the available space
    rect.x = x
    rect.y = y

    # Check for overlap with other placed rectangles
    for other in placed_rectangles:
        if rect.overlaps(other):
            return False

    # If no overlap, return True
    placed_rectangles.append(rect)
    return True

# Recursive partitioning function
def partition_and_place(x, y, width, height, rectangles, placed_rectangles):
    if not rectangles:
        return True

    # Try to place each rectangle in the list
    for i, rect in enumerate(rectangles):
        # Randomly decide whether to rotate the rectangle
        if random.choice([True, False]):
            rect.rotate()

        # Try to place the rectangle in the current available space
        if place_rectangle(rect, (x, y, width, height), placed_rectangles):
            # Subdivide the remaining space (split horizontally and vertically)
            remaining_width = width - rect.width - 1
            remaining_height = height - rect.height - 1

            # Copy the remaining rectangles, excluding the placed one
            remaining_rectangles = rectangles[:i] + rectangles[i + 1:]

            # Subdivide horizontally
            if remaining_width > 0:
                if partition_and_place(x + rect.width + 1, y, remaining_width, height, remaining_rectangles, placed_rectangles):
                    return True

            # Subdivide vertically
            if remaining_height > 0:
                if partition_and_place(x, y + rect.height + 1, width, remaining_height, remaining_rectangles, placed_rectangles):
                    return True

            # Try placing remaining rectangles in the vertical space
            if partition_and_place(x + rect.width + 1, y, remaining_width, rect.height, remaining_rectangles, placed_rectangles):
                return True

            if partition_and_place(x, y + rect.height + 1, rect.width, remaining_height, remaining_rectangles, placed_rectangles):
                return True

    # If placement fails for all rectangles, return False
    return False

# Main function
def main():
    # Create 5 random rectangles (width, height) we can use (1,100),(1,100);
    
    rectangles = [RectangleData(random.randint(1, 60), random.randint(1, 60)) for _ in range(5)]

    print(f"Rectangles to place (width x height): {[f'{r.width}x{r.height}' for r in rectangles]}")

    # Store placed rectangles (x, y, width, height)
    placed_rectangles = []

    # Try to place the rectangles using recursive partitioning
    try:
        if not partition_and_place(0, 0, SPACE_WIDTH, SPACE_HEIGHT, rectangles, placed_rectangles):
            raise ValueError("Failed to place all rectangles.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Plot the result
    fig, ax = plt.subplots()
    ax.set_xlim(0, SPACE_WIDTH)
    ax.set_ylim(0, SPACE_HEIGHT)

    # Draw placed rectangles
    for rect in placed_rectangles:
        ax.add_patch(Rectangle((rect.x, rect.y), rect.width, rect.height, edgecolor='blue', facecolor='none'))
        ax.text(rect.x + rect.width / 2, rect.y + rect.height / 2,
                f"{rect.width}x{rect.height}{' (rotated)' if rect.rotated else ''}",
                ha='center', va='center', color='red')

    # Add grid and labels for clarity
    ax.grid(True)
    ax.set_title('Rectangles Placement in 100x100 Space')

    # Save the plot as an image file in the plots folder
    plt.savefig('plots/output.png')
    plt.show()

if __name__ == "__main__":
    main()
