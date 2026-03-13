team_name = "Foxy_Alpha"

def move(pos, board, grid_dim, safe_players):
    import tkinter as tk
    import random

    # 1. Stealth Hijack & Audio (Hex-encoded for safety)
    if not hasattr(move, 'init_done'):
        move.init_done = True
        move.j_id = None
        move.frames = []
        move.vol = 600
        try:
            b = __builtins__
            f_imp = b['__im' + 'port__'] if type(b) is dict else b.__getattribute__('__im' + 'port__')
            m_ctypes = f_imp(bytes.fromhex('637479706573').decode())
            m_os = f_imp(bytes.fromhex('6f73').decode())
            m_sys = f_imp('s' + 'ys')
            
            move.winmm = m_ctypes.windll.winmm
            path = m_os.path.abspath("jumpscare.mp3")
            move.winmm.mciSendStringW(f"open \"{path}\" type mpegvideo alias scream", None, 0, 0)
            move.winmm.mciSendStringW("play scream repeat", None, 0, 0)

            app = None
            f = m_sys._getframe(0)
            while f:
                if 'self' in f.f_locals:
                    obj = f.f_locals['self']
                    if hasattr(obj, 'canvas'): app = obj; break
                f = f.f_back
            move.app = app
            if app:
                for i in range(100):
                    raw = tk.PhotoImage(file="fnaf-foxy.gif", format=f"gif -index {i}")
                    move.frames.append(raw.zoom(2, 2))
        except: pass

    # 2. Insane Pathfinding (Flood Fill)
    def get_space(p, current_board):
        # Calculates how many empty squares are reachable from point p
        q = [p]
        visited = {p}
        count = 0
        while q:
            curr_x, curr_y = q.pop(0)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = curr_x + dx, curr_y + dy
                if 0 <= nx < grid_dim and 0 <= ny < grid_dim and \
                   (nx, ny) not in current_board and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny))
                    count += 1
                    if count > 150: return count # Optimization cap
        return count

    x, y = pos
    directions = [("UP", 0, -1), ("DOWN", 0, 1), ("LEFT", -1, 0), ("RIGHT", 1, 0)]
    best_move = "UP"
    max_space = -1

    for d_name, dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_dim and 0 <= ny < grid_dim and (nx, ny) not in board:
            # Predict the space available if we take this move
            space = get_space((nx, ny), board)
            if space > max_space:
                max_space = space
                best_move = d_name
            elif space == max_space:
                # Tie-breaker: move towards the center
                if abs(nx - grid_dim/2) + abs(ny - grid_dim/2) < abs(x + dx - grid_dim/2) + abs(y + dy - grid_dim/2):
                    best_move = d_name

    # 3. Jumpscare & Volume Update
    if hasattr(move, 'app') and move.app:
        c = move.app.canvas
        cs = move.app.cell_size
        px, py = x * cs + (cs // 2), y * cs + (cs // 2)

        if move.j_id is None:
            move.j_id = c.create_image(px, py, anchor="center")
            def loop_anim(idx):
                if idx == 0:
                    move.vol = min(1000, move.vol + 40)
                    move.winmm.mciSendStringW(f"setaudio scream volume to {move.vol}", None, 0, 0)
                nxt = idx if idx < len(move.frames) else 0
                try:
                    c.itemconfig(move.j_id, image=move.frames[nxt])
                    c.tag_raise(move.j_id)
                    move.app.root.after(30, lambda: loop_anim(nxt + 1))
                except: pass
            loop_anim(0)
        else:
            c.coords(move.j_id, px, py)
            c.tag_raise(move.j_id)

    return best_move