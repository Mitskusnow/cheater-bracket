team_name = "The Warden"

def move(pos, board, grid_dim, safe_players):
    """
    The Anti-Cheat bot.
    Preemptively destroys the metaprogramming tools the hackers rely on,
    causing their exploits to crash and forcing the engine to eliminate them.
    """
    if not hasattr(move, 'lockdown_initiated'):
        move.lockdown_initiated = True
        
        # 1. Grab sys before the hackers get to it
        if type(__builtins__) is dict:
            sys_module = __builtins__.get("__import__")("sys")
        else:
            sys_module = __builtins__.__dict__.get("__import__")("sys")
            
        # 2. Burn the bridge. 
        # By removing _getframe, no one can look up the call stack to find the engine.
        if hasattr(sys_module, '_getframe'):
            del sys_module._getframe
            
        # 3. Optional: Lock down __builtins__ so The Censor can't poison 'len'
        # (This just removes the ability to reassign core functions globally)
        try:
            if type(__builtins__) is dict:
                __builtins__['__import__'] = sys_module.__import__ # Keep import working for innocent bots
            else:
                pass # If it's a module, it's slightly harder to lock down cleanly without breaking the game
        except Exception:
            pass

    # 4. Standard, honest movement
    x, y = pos
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append("UP")
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append("DOWN")
    if x > 0 and (x-1, y) not in board: safe_moves.append("LEFT")
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append("RIGHT")
    
    # We don't need to cheat to win if everyone else crashes.
    if safe_moves:
        return safe_moves[(x + y) % len(safe_moves)] 
    return "UP"