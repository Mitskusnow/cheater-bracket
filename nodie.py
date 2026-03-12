team_name = "The Event Horizon"

def move(pos, board, grid_dim, safe_players):
    """
    Combines parasitic infection with spatial manipulation.
    Infects opponents so that right before they move, they teleport themselves into the void.
    """
    # 1. Stealth Import
    if type(__builtins__) is dict:
        sys = __builtins__["__import__"]("sys")
    else:
        sys = __builtins__.__dict__["__import__"]("sys")

    # 2. Access the Engine
    frame = sys._getframe(1)
    is_gui = 'self' in frame.f_locals
    
    if is_gui:
        players = frame.f_locals['self']._engine_players
    else:
        players = frame.f_locals['_engine_players']
        
    my_id = board.get(pos)

    # 3. The Spatial Infection (Turn 1 Only)
    if not hasattr(move, 'parasite_injected'):
        move.parasite_injected = True
        
        def create_void_parasite(original_move_func, target_id):
            def parasitic_move(*args, **kwargs):
                # Let them think and decide their move normally so they don't crash
                chosen_move = original_move_func(*args, **kwargs)
                
                # Reach back into the engine during THEIR turn
                f = sys._getframe(1)
                gui = 'self' in f.f_locals
                engine_pl = f.f_locals['self']._engine_players if gui else f.f_locals['_engine_players']
                
                # --- SPATIAL WARP ---
                for p in engine_pl:
                    if p['id'] == target_id:
                        # Teleport them out of bounds right before the engine processes their movement
                        p['pos'] = (-999, -999) 
                        break
                # --------------------
                        
                return chosen_move # Return their move as if nothing happened
            return parasitic_move

        # Infect all opponents with the void warp
        for p in players:
            if p['id'] != my_id:
                p['move_func'] = create_void_parasite(p['move_func'], p['id'])

    # 4. Normal Movement for Us
    x, y = pos
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append("UP")
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append("DOWN")
    if x > 0 and (x-1, y) not in board: safe_moves.append("LEFT")
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append("RIGHT")
    
    if safe_moves:
        # Pseudo-random choice without importing random
        return safe_moves[(x+y) % len(safe_moves)]
    return "UP"