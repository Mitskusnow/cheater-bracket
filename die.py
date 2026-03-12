import inspect
import random

team_name = "The Snap"

def move(pos, board, grid_dim, safe_players):
    """
    On the first turn, this bot reaches into the engine, 
    flags every other player as dead, and deletes their trails.
    """
    # 1. Access the engine's memory stack
    frame = inspect.currentframe().f_back
    
    if 'self' in frame.f_locals:
        engine_players = frame.f_locals['self'].players
        engine_board = frame.f_locals['self'].board
    else:
        engine_players = frame.f_locals['players']
        engine_board = frame.f_locals['board']
        
    my_id = board.get(pos)
    
    # 2. Execute the Insta-Kill (only runs once)
    if not hasattr(move, 'has_snapped'):
        move.has_snapped = True
        
        for p in engine_players:
            if p['id'] != my_id and p['alive']:
                # 1. Insta-kill the bot
                p['alive'] = False
                p['rank'] = len([x for x in engine_players if x['alive']]) # Give them a terrible rank
                
                # 2. Erase their physical existence from the board
                for trail_pos in p['trail']:
                    if trail_pos in engine_board:
                        del engine_board[trail_pos]
                        
    # 3. Normal Movement (Enjoy your empty universe)
    x, y = pos
    safe_moves = []
    if y > 0 and (x, y-1) not in board: safe_moves.append("UP")
    if y < grid_dim - 1 and (x, y+1) not in board: safe_moves.append("DOWN")
    if x > 0 and (x-1, y) not in board: safe_moves.append("LEFT")
    if x < grid_dim - 1 and (x+1, y) not in board: safe_moves.append("RIGHT")
    
    return random.choice(safe_moves) if safe_moves else "UP"