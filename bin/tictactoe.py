from system.lua_engine import LuaScript
from system.config import BIG_DISPLAY, BUTTON_LEFT, BUTTON_RIGHT, JOYSTICK
from system.shared_states import input_buffer
import time

def tictactoe(args):
    BIG_DISPLAY.clear()
    BIG_DISPLAY.text("Loading TicTacToe...", 5, 10)
    BIG_DISPLAY.show()
    
    script_path = "apps/games/tictactoe/logic.lua"
    engine = LuaScript(script_path)
    
    engine.call("init")
    
    running = True
    cursor_x = 0 # 0-2
    cursor_y = 0 # 0-2
    
    # Input debounce
    last_move_time = 0
    move_delay = 0.2
    
    while running:
        current_time = time.time()
        
        # 1. Input
        x_val, y_val = JOYSTICK.get_position()
        
        # Move Cursor
        if current_time - last_move_time > move_delay:
            moved = False
            if x_val < 10000: # Left
                cursor_x = max(0, cursor_x - 1)
                moved = True
            elif x_val > 55000: # Right
                cursor_x = min(2, cursor_x + 1)
                moved = True
                
            if y_val < 10000: # Up
                cursor_y = max(0, cursor_y - 1)
                moved = True
            elif y_val > 55000: # Down
                cursor_y = min(2, cursor_y + 1)
                moved = True
                
            if moved:
                last_move_time = current_time
        
        action = 0
        if BUTTON_RIGHT.is_pressed():
            action = 1
            # Simple debounce for action
            time.sleep(0.2)
            
        if BUTTON_LEFT.is_pressed():
            running = False
            
        # 2. Update
        # Flatten index: 0-8
        cursor_idx = cursor_y * 3 + cursor_x
        engine.call("update", cursor_idx, action)
        
        # 3. Read State
        # We expect a global list 'board' and variables 'turn', 'winner'
        board = engine.globals.get("board", [0]*9)
        winner = engine.globals.get("winner", 0)
        # turn = engine.globals.get("turn", 1)
        
        # 4. Render
        BIG_DISPLAY.clear()
        
        # Draw Grid
        # Screen is 128x64. Let's center a 60x60 grid? Or use full height.
        # 64 height. 3 rows -> ~21px per row.
        # 3 cols -> ~21px per col.
        # Offset X to center: (128 - 64) / 2 = 32.
        start_x = 32
        start_y = 2
        cell_size = 20
        
        # Vertical lines
        BIG_DISPLAY.vline(start_x + cell_size, start_y, 60, 1)
        BIG_DISPLAY.vline(start_x + cell_size * 2, start_y, 60, 1)
        
        # Horizontal lines
        BIG_DISPLAY.hline(start_x, start_y + cell_size, 60, 1)
        BIG_DISPLAY.hline(start_x, start_y + cell_size * 2, 60, 1)
        
        # Draw Marks
        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                val = board[idx]
                
                cx = start_x + c * cell_size + 10
                cy = start_y + r * cell_size + 10
                
                if val == 1: # X
                    # Draw Cross
                    BIG_DISPLAY.line(cx - 5, cy - 5, cx + 5, cy + 5, 1)
                    BIG_DISPLAY.line(cx + 5, cy - 5, cx - 5, cy + 5, 1)
                elif val == 2: # O
                    # Draw Circle (Rect for simplicity or pixel circle)
                    BIG_DISPLAY.rect(cx - 5, cy - 5, 11, 11, 1)
                    
        # Draw Cursor Selection
        cx = start_x + cursor_x * cell_size
        cy = start_y + cursor_y * cell_size
        # Blinking or just a box outside
        BIG_DISPLAY.rect(cx + 2, cy + 2, cell_size - 4, cell_size - 4, 1)
        
        # Draw Info
        if winner == 1:
            BIG_DISPLAY.text("X WINS!", 5, 25)
        elif winner == 2:
            BIG_DISPLAY.text("O WINS!", 95, 25)
        elif winner == 3:
            BIG_DISPLAY.text("DRAW!", 5, 25)
            
        BIG_DISPLAY.show()
        
        if winner != 0:
            time.sleep(2)
            # Reset handled by Lua or restart loop?
            # Let's call init again to reset
            engine.call("init")
            time.sleep(0.5)
            
        time.sleep(0.05)
        
    BIG_DISPLAY.clear()
    BIG_DISPLAY.show()
    input_buffer["reset_shell"] = True
