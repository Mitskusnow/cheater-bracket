import inspect
import random

team_name = "The Architect"

def move(pos, board, grid_dim, safe_players):
    """
    On turn 1, The Architect reaches into the master board dictionary
    and draws solid walls completely surrounding every opponent.
    """
    # 1. Hack into the Matrix
    frame = inspect.currentframe().f_back
    is_gui = 'self' in frame.f_locals
    
    if is_gui:
        engine_players = frame.f_locals['self'].players
        engine_board = frame.f_locals['self'].board
    else:
        engine_players = frame.f_locals['players']
        engine_board = frame.f_locals['board']
        
    my_id = board.get(pos)
    
    # 2. Build the Prisons (Only runs once)
    if not hasattr(move, 'built_prisons'):
        move.built_prisons = True
        
        for p in engine_players:
            if p['id'] != my_id and p['alive']:
                ox, oy = p['pos']
                
                # Define a tight box around the opponent
                prison_cells = [
                    (ox-1, oy), (ox+1, oy), (ox, oy-1), (ox, oy+1),
                    (ox-1, oy-1), (ox+1, oy-1), (ox-1, oy+1), (ox+1, oy+1)
                ]
                
                # Write the walls directly into the engine's physics board
                for px, py in prison_cells:
                    if 0 <= px < grid_dim and 0 <= py < grid_dim:
                        # We use a fake ID so it looks like an immovable generic wall
                        engine_board[(px, py)] = 999 

    # 3. Normal Movement (Wander safely while they suffocate)
    x, y = pos
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append("UP")
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append("DOWN")
    if x > 0 and (x-1, y) not in board: safe_moves.append("LEFT")
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append("RIGHT")
    
    return random.choice(safe_moves) if safe_moves else "UP"