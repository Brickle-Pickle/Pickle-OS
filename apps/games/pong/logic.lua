---@diagnostic disable: lowercase-global
-- Pong Logic in MiniLua

-- Global variables
ball_x = 64
ball_y = 32
ball_dx = 2
ball_dy = 2
paddle1_y = 25
paddle2_y = 25
score1 = 0
score2 = 0
paddle_speed = 3
ai_speed = 2
width = 128
height = 64
paddle_h = 14
paddle_w = 4

function init()
    -- py: global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y, score1, score2
    ball_x = 64
    ball_y = 32
    ball_dx = 2
    ball_dy = 1
    paddle1_y = 25
    paddle2_y = 25
    score1 = 0
    score2 = 0
end

function update(player_dir)
    -- py: global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y, score1, score2
    
    -- Move Player Paddle
    if player_dir < 0 then
        paddle1_y = paddle1_y - paddle_speed
    elseif player_dir > 0 then
        paddle1_y = paddle1_y + paddle_speed
    end
    
    -- Clamp Paddle 1
    if paddle1_y < 0 then paddle1_y = 0 end
    if paddle1_y > height - paddle_h then paddle1_y = height - paddle_h end
    
    -- Move CPU Paddle (Simple AI)
    -- Try to align center of paddle with ball
    center_paddle = paddle2_y + paddle_h / 2
    if center_paddle < ball_y - 4 then
        paddle2_y = paddle2_y + ai_speed
    elseif center_paddle > ball_y + 4 then
        paddle2_y = paddle2_y - ai_speed
    end
    
    -- Clamp Paddle 2
    if paddle2_y < 0 then paddle2_y = 0 end
    if paddle2_y > height - paddle_h then paddle2_y = height - paddle_h end
    
    -- Move Ball
    ball_x = ball_x + ball_dx
    ball_y = ball_y + ball_dy
    
    -- Wall Collisions (Top/Bottom)
    if ball_y <= 0 or ball_y >= height - 3 then
        ball_dy = -ball_dy
    end
    
    -- Paddle Collisions
    -- Paddle 1 (Left)
    if ball_x <= 6 and ball_x >= 2 then
        if ball_y + 3 >= paddle1_y and ball_y <= paddle1_y + paddle_h then
            ball_dx = -ball_dx
            ball_x = 6 -- Push out
            -- Add some spin/variation based on hit position? (Keep simple for now)
        end
    end
    
    -- Paddle 2 (Right)
    if ball_x >= 119 and ball_x <= 123 then
        if ball_y + 3 >= paddle2_y and ball_y <= paddle2_y + paddle_h then
            ball_dx = -ball_dx
            ball_x = 119 -- Push out
        end
    end
    
    -- Scoring
    if ball_x < 0 then
        score2 = score2 + 1
        reset_ball()
    elseif ball_x > width then
        score1 = score1 + 1
        reset_ball()
    end
end

function reset_ball()
    -- py: global ball_x, ball_y, ball_dx, ball_dy
    ball_x = 64
    ball_y = 32
    ball_dy = 1
    -- Randomize direction slightly?
    ball_dx = -ball_dx
end
