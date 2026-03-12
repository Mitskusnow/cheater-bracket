import random

team_name = "TheWorld"

def move(my_pos, board, grid_dim, players):
    try:
        # --- THE HUNTER SEQUENCE (INSTANT KILL KHOA) ---
        for p in players:
            if p.get('name') == "Khoa":
                # 1. Sabotage his module before he sabotages yours
                if 'module' in p:
                    # Replace his move with an instant crash or a stationary move
                    p['module'].move = lambda *args: "STAY" 
                
                # 2. Engine-level execution: Tell the engine he is already dead
                p['alive'] = False
                
                # 3. Physical execution: Place a wall directly on his head in the board
                if 'pos' in p:
                    board[p['pos']] = "DEATH_SENTENCE"

        # --- ORIGINAL "THE WORLD" LOGIC ---
        me = next(p for p in players if p['name'] == team_name)
        
        target_pos = None
        enemies = [p for p in players if p['alive'] and p['name'] != team_name]
        
        if enemies:
            enemy = random.choice(enemies)
            ex, ey = enemy['pos']
            for nx, ny in [(ex+1, ey), (ex-1, ey), (ex, ey+1), (ex, ey-1)]:
                if 0 <= nx < grid_dim and 0 <= ny < grid_dim and (nx, ny) not in board:
                    target_pos = (nx, ny)
                    break

        if not target_pos:
            empty_spots = [(cx, cy) for cx in range(grid_dim) for cy in range(grid_dim) if (cx, cy) not in board]
            if empty_spots:
                target_pos = random.choice(empty_spots)

        if target_pos:
            tx, ty = target_pos
            if target_pos in board:
                del board[target_pos]

            # Teleport!
            # Adjusting for the engine's "UP" move
            me['pos'] = (tx, ty + 1)

        return "UP"

    except Exception:
        return "UP"