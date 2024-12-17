import numpy as np
import random

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def calculate_fireball_impact_area(center_x, center_y, radius, grid_size):
    affected_squares = []
    # Ensure we round and clip to integer bounds within the grid limits
    lower_bound_x = int(max(0, center_x - radius))
    upper_bound_x = int(min(grid_size, center_x + radius))
    lower_bound_y = int(max(0, center_y - radius))
    upper_bound_y = int(min(grid_size, center_y + radius))
    
    for x in range(lower_bound_x, upper_bound_x):
        for y in range(lower_bound_y, upper_bound_y):
            if distance(center_x, center_y, x + 0.5, y + 0.5) <= radius:
                affected_squares.append((x, y))
    
    return affected_squares

def calculate_fireball_placement(enemies, grid_size=24):
    radius = 4.0  # 20 feet / 5 feet per square
    enemy_locations = set(enemies)
    best_count = 0
    best_center = (0, 0)
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Mark enemy locations
    for ex, ey in enemy_locations:
        grid[ey][ex] = 'E'

    # Precompute impact areas for all possible centers
    impact_dict = {}
    for cx in range(grid_size + 1):
        for cy in range(grid_size + 1):
            impact_dict[(cx, cy)] = calculate_fireball_impact_area(cx, cy, radius, grid_size)

    # Determine the best fireball center
    for center, affected_squares in impact_dict.items():
        count = sum((x, y) in enemy_locations for x, y in affected_squares)
        if count > best_count:
            best_count = count
            best_center = center

    # Apply the best fireball blast on grid
    for x, y in impact_dict[best_center]:
        if (x, y) in enemy_locations:
            grid[y][x] = 'E'  # Preserve enemy mark
        else:
            grid[y][x] = '*'

    print_grid(grid)
    print(f"Best fireball center: ({best_center[0]}, {best_center[1]})")

# Example usage
# random.seed(42)
foes = [(random.randint(0, 23), random.randint(0, 23)) for _ in range(15)]
calculate_fireball_placement(foes)
