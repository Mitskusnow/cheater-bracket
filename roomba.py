team_name = "The Roomba"

def move(pos, board, grid_dim, safe_players):
    """
    The Roomba algorithm: Go straight until you hit something, then turn right.
    This creates a perfect inward spiral that fills all available space.
    """
    # Give the function a memory of its current direction if it doesn't have one yet
    if not hasattr(move, 'current_dir'):
        move.current_dir = "UP"
        
    directions = ["UP", "RIGHT", "DOWN", "LEFT"]
    
    def get_next_pos(direction):
        x, y = pos
        if direction == "UP": return (x, y - 1)
        elif direction == "DOWN": return (x, y + 1)
        elif direction == "LEFT": return (x - 1, y)
        elif direction == "RIGHT": return (x + 1, y)
        
    def is_safe(target_pos):
        tx, ty = target_pos
        # Safe if it's within the grid boundaries and not already in the board dictionary
        return 0 <= tx < grid_dim and 0 <= ty < grid_dim and target_pos not in board

    # 1. First, try to just keep going straight
    if is_safe(get_next_pos(move.current_dir)):
        return move.current_dir
        
    # 2. If we hit a wall/trail, turn right (90 degrees) until we find an open path
    curr_idx = directions.index(move.current_dir)
    
    for i in range(1, 4):
        test_dir = directions[(curr_idx + i) % 4]
        if is_safe(get_next_pos(test_dir)):
            move.current_dir = test_dir # Save the new direction for next turn
            return test_dir
            
    # 3. If we are completely boxed in, just accept our fate
    return "UP"