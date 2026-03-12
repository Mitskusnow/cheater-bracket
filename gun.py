team_name = "The Gunslinger"

def move(pos, board, grid_dim, safe_players):
    """
    Weaponizes the shared board dictionary to perform a ranged attack.
    Fires 'bullets' (solid walls) directly into the opponent's escape routes
    from across the map.
    """
    import sys
    
    # 1. Access the Engine's Frame to find the targets
    frame = sys._getframe(1)
    is_gui = 'self' in frame.f_locals
    
    if is_gui:
        engine = frame.f_locals['self']
        players = engine._engine_players
        real_board = engine._engine_board # The actual physical universe
    else:
        engine = frame.f_locals
        players = engine['_engine_players']
        real_board = engine['_engine_board']

    my_id = board.get(pos)

    # 2. Take Aim and Fire (Every Turn)
    for p in players:
        # If it's an enemy and they are still alive
        if p['id'] != my_id and p.get('alive', True):
            enemy_pos = p.get('pos')
            if enemy_pos:
                ex, ey = enemy_pos
                
                # Calculate the 4 tiles immediately surrounding the enemy
                kill_zone = [(ex, ey-1), (ex, ey+1), (ex-1, ey), (ex+1, ey)]
                
                # Fire bullets into all their immediate escape routes
                for target_tile in kill_zone:
                    tx, ty = target_tile
                    # Only shoot if it's within the map boundaries
                    if 0 <= tx < grid_dim and 0 <= ty < grid_dim:
                        # We spawn a wall in front of them. 
                        # We use their own ID as the bullet so the engine blames them for the collision!
                        real_board[target_tile] = p['id'] 

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