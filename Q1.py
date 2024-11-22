import copy

# Define the target state
TARGET_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Calculate Manhattan Distance Heuristic
def heuristic_manhattan(board):
    total_distance = 0
    for row in range(3):
        for col in range(3):
            value = board[row][col]
            if value != 0:
                goal_row, goal_col = divmod(value - 1, 3)
                total_distance += abs(goal_row - row) + abs(goal_col - col)
    return total_distance

# Locate the empty tile
def find_empty(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                return row, col

# Generate all valid moves
def generate_moves(board):
    possible_boards = []
    empty_row, empty_col = find_empty(board)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dx, dy in moves:
        new_row, new_col = empty_row + dx, empty_col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_board = copy.deepcopy(board)
            new_board[empty_row][empty_col], new_board[new_row][new_col] = (
                new_board[new_row][new_col],
                new_board[empty_row][empty_col],
            )
            possible_boards.append(new_board)
    return possible_boards

# Solve the puzzle using Hill Climbing
def hill_climb_solver(start_state):
    current_board = start_state
    moves = 0

    while True:
        moves += 1
        current_score = heuristic_manhattan(current_board)
        print(f"\nMove {moves}:")
        print(f"Current Board (h={current_score}):")
        for line in current_board:
            print(line)
        
        if current_score == 0:  # Check if target state is reached
            print("\nTarget state achieved!")
            return current_board, moves
        
        next_boards = generate_moves(current_board)
        best_board = None
        lowest_score = float('inf')

        print("\nEvaluating Neighbors:")
        for neighbor in next_boards:
            neighbor_score = heuristic_manhattan(neighbor)
            for line in neighbor:
                print(line)
            print(f"Heuristic: {neighbor_score}")
            
            if neighbor_score < lowest_score:
                best_board = neighbor
                lowest_score = neighbor_score

        if lowest_score >= current_score:  # Check for local maxima or plateau
            print("\nStuck at a local maxima or plateau.")
            return current_board, moves

        current_board = best_board

if __name__ == "__main__":
    start_state = [
        [1, 3, 0],
        [4, 2, 6],
        [7, 5, 8]
    ]
    
    print("Starting Board:")
    for line in start_state:
        print(line)
    
    final_board, move_count = hill_climb_solver(start_state)

    print("\nFinal Board:")
    for line in final_board:
        print(line)
    print(f"Total Moves: {move_count}")
