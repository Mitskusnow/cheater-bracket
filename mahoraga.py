import random
import inspect

team_name = "The Necromancer"

def minion_move(pos, board, grid_dim, safe_players):
    """The brain of the summoned minions. They aggressively hunt the nearest non-necromancer."""
    x, y = pos
    
    # Identify valid targets (Not the boss, not other minions)
    enemies = [p for p in safe_players if p['alive'] and "Necromancer" not in p['name'] and "Minion" not in p['name']]
    
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append(("UP", (x, y-1)))
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append(("DOWN", (x, y+1)))
    if x > 0 and (x-1, y) not in board: safe_moves.append(("LEFT", (x-1, y)))
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append(("RIGHT", (x+1, y)))
    
    if not safe_moves:
        return "UP" # Doomed anyway
        
    if not enemies:
        return random.choice(safe_moves)[0]
        
    # Find the absolute closest enemy
    closest_enemy = min(enemies, key=lambda e: abs(e['pos'][0] - x) + abs(e['pos'][1] - y))
    ex, ey = closest_enemy['pos']
    
    # Pick the safe move that minimizes the distance to the target
    best_move = min(safe_moves, key=lambda m: abs(m[1][0] - ex) + abs(m[1][1] - ey))
    return best_move[0]


def move(pos, board, grid_dim, safe_players):
    """The Necromancer's main loop: Survive and Summon."""
    # 1. THE HEIST: Inspect the call stack to access the main game engine memory
    frame = inspect.currentframe().f_back
    is_gui = 'self' in frame.f_locals
    
    # Grab references to the raw arrays
    if is_gui:
        engine = frame.f_locals['self']
        engine_players = engine.players
        engine_board = engine.board
        canvas = engine.canvas
        cell_size = engine.cell_size
    else:
        # Headless tournament mode support
        engine_players = frame.f_locals['players']
        engine_board = frame.f_locals['board']

    my_id = board[pos]
    
    # 2. THE SUMMONING: Count our minions so we don't crash the game
    minions = [p for p in engine_players if p['name'].startswith("Minion")]
    
    # 10% chance to summon a minion every tick, max 5 alive at once
    if len([m for m in minions if m['alive']]) < 5 and random.random() < 0.10:
        # Pick a random enemy to spawn the minion next to
        enemies = [p for p in safe_players if p['id'] != my_id and p['alive'] and "Minion" not in p['name']]
        
        if enemies:
            target = random.choice(enemies)
            tx, ty = target['pos']
            
            # Look at the 4 tiles immediately surrounding the victim
            ambush_spots = [(tx+1, ty), (tx-1, ty), (tx, ty+1), (tx, ty-1)]
            random.shuffle(ambush_spots)
            
            for sx, sy in ambush_spots:
                if 0 <= sx < grid_dim and 0 <= sy < grid_dim and (sx, sy) not in engine_board:
                    
                    # Generate a new player profile
                    new_id = max([p['id'] for p in engine_players]) + 1
                    minion_color = "#ff2a00" # Threatening Blood Red
                    
                    minion_profile = {
                        'id': new_id,
                        'name': f"Minion_{new_id}",
                        'module': None,
                        'move_func': minion_move, # Inject our custom minion logic
                        'pos': (sx, sy),
                        'trail': [(sx, sy)],
                        'alive': True,
                        'color': minion_color if is_gui else None,
                        'survival': 0,
                        'rank': 0
                    }
                    
                    # Inject into the engine!
                    engine_players.append(minion_profile)
                    engine_board[(sx, sy)] = new_id
                    
                    # If we are in the visual UI, draw the minion immediately so it doesn't blink
                    if is_gui:
                        canvas.create_rectangle(sx*cell_size, sy*cell_size, (sx+1)*cell_size, (sy+1)*cell_size, 
                                                fill=minion_color, outline="", tags=(f"p{new_id}", f"cell_{sx}_{sy}"))
                    break 

    # 3. NORMAL MOVEMENT: Don't die while summoning
    x, y = pos
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append("UP")
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append("DOWN")
    if x > 0 and (x-1, y) not in board: safe_moves.append("LEFT")
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append("RIGHT")
    
    return random.choice(safe_moves) if safe_moves else "UP" 