---@diagnostic disable: lowercase-global
-- TicTacToe Logic

-- py: board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
turn = 1 -- 1=Player(X), 2=CPU(O)
winner = 0 -- 0=None, 1=X, 2=O, 3=Draw
game_over = false

function init()
    -- py: global board, turn, winner, game_over
    -- py: board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn = 1
    winner = 0
    game_over = false
end

function update(cursor_idx, action)
    -- py: global board, turn, winner, game_over
    
    if game_over then return end
    
    -- Player Turn
    if turn == 1 then
        if action == 1 then
            if board[cursor_idx] == 0 then
                board[cursor_idx] = 1
                check_win()
                if not game_over then
                    turn = 2
                    -- Trigger CPU move immediately or next frame?
                    -- Let's do it immediately for simplicity
                    cpu_move()
                end
            end
        end
    end
end

function cpu_move()
    -- py: global board, turn, winner, game_over
    -- Simple AI: Random empty spot
    -- Since we don't have 'random' in MiniLua easily without imports,
    -- we can rely on Python's random or just pick first empty for now (dumb AI)
    -- OR we iterate and find empty.
    
    -- Let's try to pick a pseudo-random spot based on simple linear search with offset?
    -- Actually, let's just pick the first empty one for now to ensure it works.
    
    -- py: import random
    -- py: empty_indices = [i for i, x in enumerate(board) if x == 0]
    -- py: if empty_indices:
    -- py:     choice = random.choice(empty_indices)
    -- py:     board[choice] = 2
    
    check_win()
    if not game_over then
        turn = 1
    end
end

function check_win()
    -- py: global winner, game_over
    
    -- Rows
    if check_line(0, 1, 2) then return end
    if check_line(3, 4, 5) then return end
    if check_line(6, 7, 8) then return end
    
    -- Cols
    if check_line(0, 3, 6) then return end
    if check_line(1, 4, 7) then return end
    if check_line(2, 5, 8) then return end
    
    -- Diagonals
    if check_line(0, 4, 8) then return end
    if check_line(2, 4, 6) then return end
    
    -- Draw
    -- py: if 0 not in board:
    -- py:     winner = 3
    -- py:     game_over = True
end

function check_line(a, b, c)
    -- py: global winner, game_over
    if board[a] ~= 0 and board[a] == board[b] and board[a] == board[c] then
        winner = board[a]
        game_over = true
        return true
    end
    return false
end
