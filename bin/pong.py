from system.lua_engine import LuaScript
from system.config import BIG_DISPLAY, BUTTON_LEFT, JOYSTICK
from system.shared_states import input_buffer
import time

def pong(args):
    BIG_DISPLAY.clear()
    BIG_DISPLAY.text("Loading Pong...", 10, 10)
    BIG_DISPLAY.show()
    
    # Path to the lua script
    script_path = "apps/games/pong/logic.lua"
    engine = LuaScript(script_path)
    
    engine.call("init")
    
    running = True
    
    while running:
        # 1. Read Input
        # Joystick Y for paddle movement (0-65535, center ~32768)
        # We'll normalize this in Python or pass raw to Lua.
        # Let's pass a simplified direction (-1, 0, 1) to Lua for consistency with Snake
        x_val, y_val = JOYSTICK.get_position()
        move_dir = 0
        
        # Deadzone check
        if y_val < 20000:
            move_dir = -1 # Up
        elif y_val > 45000:
            move_dir = 1 # Down
            
        if BUTTON_LEFT.is_pressed():
            running = False # Exit
            
        # 2. Update Game Logic
        try:
            engine.call("update", move_dir)
            # print(f"Called update with {move_dir}") # Debug
        except Exception as e:
            print(f"Error calling update: {e}")
        
        # Get globals from Lua
        ball_x = engine.globals.get("ball_x", 64)
        ball_y = engine.globals.get("ball_y", 32)
        paddle1_y = engine.globals.get("paddle1_y", 25)
        paddle2_y = engine.globals.get("paddle2_y", 25)
        score1 = engine.globals.get("score1", 0)
        score2 = engine.globals.get("score2", 0)
        
        # 3. Render
        BIG_DISPLAY.clear()
        
        # Draw Center Line (dotted)
        for i in range(0, 64, 4):
            BIG_DISPLAY.pixel(64, i, 1)
            
        # Draw Paddles (width 4, height 14)
        BIG_DISPLAY.fill_rect(2, int(paddle1_y), 4, 14, 1)
        BIG_DISPLAY.fill_rect(122, int(paddle2_y), 4, 14, 1)
        
        # Draw Ball (2x2)
        BIG_DISPLAY.fill_rect(int(ball_x), int(ball_y), 3, 3, 1)
        
        # Draw Scores
        BIG_DISPLAY.text(str(score1), 50, 5)
        BIG_DISPLAY.text(str(score2), 70, 5)
            
        BIG_DISPLAY.show()
        
        # Simple loop delay
        time.sleep(0.01)
        
    # Cleanup
    BIG_DISPLAY.clear()
    BIG_DISPLAY.show()
    input_buffer["reset_shell"] = True

def help():
    BIG_DISPLAY.clear()
    BIG_DISPLAY.show_info(["Pong Help", "Use joystick to move paddles. Press left button to exit."], 6)
    BIG_DISPLAY.show()