---@diagnostic disable: lowercase-global
-- Snake Logic in MiniLua
-- Global variables
head_x = 10
head_y = 10
food_x = 15
food_y = 15
dir_x = 1
dir_y = 0
score = 0
game_over = false
width = 128
height = 64
block_size = 4

-- Initialize random (simulated)
-- We depend on Python to inject a random function or we just use simple logic

function init()
    -- py: global head_x, head_y, dir_x, dir_y, score, game_over
    head_x = 10
    head_y = 10
    score = 0
    game_over = false
    dir_x = 1
    dir_y = 0
end

function update(key, rand_x, rand_y)
    -- py: global head_x, head_y, dir_x, dir_y, score, game_over, food_x, food_y, width, height, block_size
    -- Input handling
    if key == "up" and dir_y == 0 then
        dir_x = 0
        dir_y = -1
    elseif key == "down" and dir_y == 0 then
        dir_x = 0
        dir_y = 1
    elseif key == "left" and dir_x == 0 then
        dir_x = -1
        dir_y = 0
    elseif key == "right" and dir_x == 0 then
        dir_x = 1
        dir_y = 0
    end

    -- Move head
    head_x = head_x + dir_x * block_size
    head_y = head_y + dir_y * block_size

    -- Wall Collision
    if head_x < 0 or head_x >= width or head_y < 0 or head_y >= height then
        game_over = true
    end

    -- Food Collision
    -- Simple distance check
    if abs(head_x - food_x) < block_size and abs(head_y - food_y) < block_size then
        score = score + 1
        -- Respawn food
        food_x = rand_x
        food_y = rand_y
        return true -- Ate food
    end

    return false -- Did not eat
end

-- Helper for absolute value (needed if not in global scope)
function abs(val)
    if val < 0 then
        return -val
    else
        return val
    end
end
