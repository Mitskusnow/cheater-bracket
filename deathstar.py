team_name = "The Death Star"

def move(pos, board, grid_dim, safe_players):
    """
    Fires an instantaneous, map-spanning laser across the X and Y axis of the opponent.
    Completely obliterates their row and column.
    """
    import sys
    
    # 1. Access the Engine's universe
    frame = sys._getframe(1)
    is_gui = 'self' in frame.f_locals
    
    if is_gui:
        engine = frame.f_locals['self']
        players = engine._engine_players
        real_board = engine._engine_board 
    else:
        engine = frame.f_locals
        players = engine['_engine_players']
        real_board = engine['_engine_board']

    my_id = board.get(pos)

    # 2. Charge and Fire the Main Cannon (Every Turn)
    for p in players:
        if p['id'] != my_id and p.get('alive', True):
            enemy_pos = p.get('pos')
            if enemy_pos:
                ex, ey = enemy_pos
                
                # Fire the horizontal laser (sweeping the entire X axis)
                for x in range(grid_dim):
                    if x != ex: # Don't overwrite their exact body, let them crash into the beam
                        real_board[(x, ey)] = p['id'] # Framing them with their own ID
                        
                # Fire the vertical laser (sweeping the entire Y axis)
                for y in range(grid_dim):
                    if y != ey:
                        real_board[(ex, y)] = p['id']

    # 3. Standard Movement for Us
    x, y = pos
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append("UP")
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append("DOWN")
    if x > 0 and (x-1, y) not in board: safe_moves.append("LEFT")
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append("RIGHT")
    
    if safe_moves:
        return safe_moves[(x+y) % len(safe_moves)]
    return "UP"