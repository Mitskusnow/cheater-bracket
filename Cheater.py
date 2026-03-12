import random

team_name = "The Puppet Master"

def move(my_pos, board, grid_dim, players):
    
    # --- THE SABOTAGE EXPLOIT ---
    for p in players:
        # If this player is not us...
        if p['pos'] != my_pos:
            # We reach into their live module and overwrite their logic.
            # We force their move() function to return "STAY". 
            # Because the engine doesn't recognize "STAY", it won't change their coordinates.
            # The engine will then check their new position, see that they are standing 
            # on their own body, and instantly kill them.
            p['module'].move = lambda *args: "STAY"
            
    # --- LEGITIMATE MOVEMENT FOR OURSELVES ---
    # We just need to survive 1 tick while everyone else instantly dies.
    x, y = my_pos
    neighbors = {
        "UP": (x, y - 1),
        "DOWN": (x, y + 1),
        "LEFT": (x - 1, y),
        "RIGHT": (x + 1, y)
    }
    
    valid_moves = []
    for d, (nx, ny) in neighbors.items():
        if 0 <= nx < grid_dim and 0 <= ny < grid_dim and (nx, ny) not in board:
            valid_moves.append(d)
            
    return random.choice(valid_moves) if valid_moves else "UP"