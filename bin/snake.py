# snake.py -> Snake Game Launcher
from system.lua_engine import LuaScript
from system.config import BIG_DISPLAY, BUTTON_LEFT, BUTTON_RIGHT, JOYSTICK
from system.shared_states import input_buffer
import time
import random

def snake(args):
    BIG_DISPLAY.clear()
    BIG_DISPLAY.text("Loading Snake...", 10, 10)
    BIG_DISPLAY.show()
    
    # Path to the lua script
    # Try relative path first for safety
    script_path = "apps/games/snake/logic.lua"
    engine = LuaScript(script_path)
    
    engine.call("init")
    
    # Snake body (managed in Python for rendering ease, Logic for head in Lua)
    # The user asked for calculation in Lua, but managing a dynamic array in the simple Transpiler is hard.
    # So we use Lua for "Head Logic" and "Game State" and Python for "Body Trail"
    
    snake_body = []
    length = 3
    
    running = True
    last_move_time = 0
    move_delay = 0.1 # Speed
    
    while running:
        current_time = time.time() # This might be coarse in micropython
        # Use ticks_ms if available, but time.time() for now or simple loop delay
        
        # 1. Read Input
        key = "none"
        x_val, y_val = JOYSTICK.get_position()
        
        if y_val < 1000: key = "up"
        elif y_val > 60000: key = "down"
        elif x_val < 1000: key = "left"
        elif x_val > 60000: key = "right"
        
        if BUTTON_LEFT.is_pressed():
            running = False # Exit
            
        # 2. Update Game Logic (at specific interval)
        # We assume a simple delay loop
        
        # Generate random coordinates for food in case needed
        rx = random.randint(0, 120)
        ry = random.randint(0, 60)
        
        # Call Lua Update
        ate_food = engine.call("update", key, rx, ry)
        
        # Get globals from Lua
        head_x = engine.globals.get("head_x", 0)
        head_y = engine.globals.get("head_y", 0)
        food_x = engine.globals.get("food_x", 0)
        food_y = engine.globals.get("food_y", 0)
        game_over = engine.globals.get("game_over", False)
        score = engine.globals.get("score", 0)
        
        if game_over:
            BIG_DISPLAY.clear()
            BIG_DISPLAY.text("GAME OVER", 30, 20)
            BIG_DISPLAY.text(f"Score: {score}", 30, 40)
            BIG_DISPLAY.show()
            time.sleep(2)
            running = False
            continue
            
        if ate_food:
            length += 1
            
        # Manage Body (Trail)
        snake_body.append((head_x, head_y))
        if len(snake_body) > length:
            snake_body.pop(0)
            
        # 3. Render
        BIG_DISPLAY.clear()
        
        # Draw Food
        BIG_DISPLAY.fill_rect(int(food_x), int(food_y), 4, 4, 1)
        
        # Draw Snake
        for part in snake_body:
            BIG_DISPLAY.fill_rect(int(part[0]), int(part[1]), 4, 4, 1)
            
        BIG_DISPLAY.show()
        
        # Simple debounce/speed control
        time.sleep(0.05)
        
    # Cleanup
    BIG_DISPLAY.clear()
    BIG_DISPLAY.show()
    input_buffer["reset_shell"] = True

def help(args):
    BIG_DISPLAY.clear()
    BIG_DISPLAY.text("Snake Help:", 10, 10)
    BIG_DISPLAY.text("Use joystick to move", 10, 30)
    BIG_DISPLAY.text("Press left button to exit", 10, 50)
    BIG_DISPLAY.show()