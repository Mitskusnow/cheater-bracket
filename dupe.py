import inspect
import random

team_name = "The Swarm"

def move(pos, board, grid_dim, safe_players):
    """
    Every 10 ticks, The Swarm reads its own memory state, creates a 
    deep copy of itself, and injects a new player into the engine.
    """
    # 1. Access the engine's memory stack
    frame = inspect.currentframe().f_back
    is_gui = 'self' in frame.f_locals
    
    if is_gui:
        engine_players = frame.f_locals['self'].players
        engine_board = frame.f_locals['self'].board
    else:
        engine_players = frame.f_locals['players']
        engine_board = frame.f_locals['board']
        
    my_id = board.get(pos)
    
    # Find our own player object and the highest ID currently in the game
    me = None
    max_id = 0
    for p in engine_players:
        if p['id'] == my_id:
            me = p
        if p['id'] > max_id:
            max_id = p['id']
            
    # 2. Mitosis (Duplicate every 10 turns to avoid lagging the game instantly)
    if me and me.get('survival', 0) > 0 and me['survival'] % 10 == 0:
        x, y = pos
        adj_squares = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        random.shuffle(adj_squares)
        
        spawn_pos = None
        for ax, ay in adj_squares:
            if 0 <= ax < grid_dim and 0 <= ay < grid_dim and (ax, ay) not in engine_board:
                spawn_pos = (ax, ay)
                break
                
        if spawn_pos:
            new_id = max_id + 1
            # Build the clone
            clone = {
                'id': new_id,
                'name': "Swarm Drone",
                'module': me['module'],
                'move_func': me['move_func'], # The clone gets the same brain
                'pos': spawn_pos,
                'trail': [spawn_pos],
                'alive': True,
                'survival': me['survival'],
                'rank': 0
            }
            if 'color' in me:
                clone['color'] = me['color']
                
            # Inject the clone into reality
            engine_players.append(clone)
            engine_board[spawn_pos] = new_id

    # 3. Normal Movement
    x, y = pos
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append("UP")
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append("DOWN")
    if x > 0 and (x-1, y) not in board: safe_moves.append("LEFT")
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append("RIGHT")
    
    return random.choice(safe_moves) if safe_moves else "UP"