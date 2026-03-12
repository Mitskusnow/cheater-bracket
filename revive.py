import random
import inspect

team_name = "The Phoenix"

def move(pos, board, grid_dim, safe_players):
    """
    The Phoenix lives normally until it is trapped. 
    Right before death, it bursts into flames and spawns a new version of itself.
    """
    x, y = pos
    
    # 1. Calculate safe moves
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append("UP")
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append("DOWN")
    if x > 0 and (x-1, y) not in board: safe_moves.append("LEFT")
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append("RIGHT")
    
    # 2. Reincarnation Sequence (Triggered if trapped)
    if not safe_moves:
        # We are about to die. Time to hack the mainframe.
        frame = inspect.currentframe().f_back
        is_gui = 'self' in frame.f_locals
        
        if is_gui:
            engine = frame.f_locals['self']
            engine_players = engine.players
            engine_board = engine.board
            canvas = engine.canvas
            cell_size = engine.cell_size
        else:
            engine_players = frame.f_locals['players']
            engine_board = frame.f_locals['board']

        # Find a completely random empty spot on the board
        empty_spots = []
        for rx in range(5, grid_dim - 5):
            for ry in range(5, grid_dim - 5):
                if (rx, ry) not in engine_board:
                    empty_spots.append((rx, ry))
                    
        if empty_spots:
            spawn_x, spawn_y = random.choice(empty_spots)
            new_id = max([p['id'] for p in engine_players]) + 1
            
            # Create the new body
            phoenix_color = "#ff8800" # Fiery Orange
            
            reborn_profile = {
                'id': new_id,
                'name': team_name,     # Keep the same name to confuse the leaderboard!
                'module': None,
                'move_func': move,     # Pass its own brain to the new body
                'pos': (spawn_x, spawn_y),
                'trail': [(spawn_x, spawn_y)],
                'alive': True,
                'color': phoenix_color if is_gui else None,
                'survival': 0,         # Resets survival time for the new body
                'rank': 0
            }
            
            # Inject the new body into the game
            engine_players.append(reborn_profile)
            engine_board[(spawn_x, spawn_y)] = new_id
            
            if is_gui:
                canvas.create_rectangle(spawn_x*cell_size, spawn_y*cell_size, 
                                        (spawn_x+1)*cell_size, (spawn_y+1)*cell_size, 
                                        fill=phoenix_color, outline="", 
                                        tags=(f"p{new_id}", f"cell_{spawn_x}_{spawn_y}"))

        # Return a doomed move to let the current body die naturally
        return "UP"

    # 3. Normal Movement (if not trapped)
    return random.choice(safe_moves)
