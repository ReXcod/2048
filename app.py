import streamlit as st
import numpy as np
import random

def initialize_board():
    board = np.zeros((4, 4), dtype=int)
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = 2 if random.random() < 0.9 else 4

def compress(board):
    new_board = np.zeros((4, 4), dtype=int)
    for row in range(4):
        pos = 0
        for col in range(4):
            if board[row][col] != 0:
                new_board[row][pos] = board[row][col]
                pos += 1
    return new_board

def merge(board):
    for row in range(4):
        for col in range(3):
            if board[row][col] == board[row][col + 1] and board[row][col] != 0:
                board[row][col] *= 2
                board[row][col + 1] = 0
    return board

def move_left(board):
    compressed_board = compress(board)
    merged_board = merge(compressed_board)
    final_board = compress(merged_board)
    return final_board

def move_right(board):
    return np.fliplr(move_left(np.fliplr(board)))

def move_up(board):
    return np.rot90(move_left(np.rot90(board, -1)), 1)

def move_down(board):
    return np.rot90(move_left(np.rot90(board, 1)), -1)

def is_game_over(board):
    if np.any(board == 0):
        return False
    for r in range(4):
        for c in range(3):
            if board[r][c] == board[r][c + 1]:
                return False
    for r in range(3):
        for c in range(4):
            if board[r][c] == board[r + 1][c]:
                return False
    return True

st.title("🎮 2048 Game")
st.markdown("### Use the buttons below to move the tiles!")

if "board" not in st.session_state:
    st.session_state.board = initialize_board()

def update_board(direction):
    new_board = st.session_state.board.copy()
    if direction == "Left":
        new_board = move_left(new_board)
    elif direction == "Right":
        new_board = move_right(new_board)
    elif direction == "Up":
        new_board = move_up(new_board)
    elif direction == "Down":
        new_board = move_down(new_board)
    
    if not np.array_equal(st.session_state.board, new_board):
        st.session_state.board = new_board
        add_new_tile(st.session_state.board)
    
    if is_game_over(st.session_state.board):
        st.warning("🚨 Game Over! Refresh to restart.")

def display_board():
    board_html = """<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 80px);
        gap: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .grid-item {
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #eee;
        border-radius: 10px;
    }
    </style>
    <div class='grid-container'>"""
    
    colors = {
        0: "#ccc", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
        256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
    }
    
    for row in st.session_state.board:
        for num in row:
            color = colors.get(num, "#3c3a32")
            board_html += f"<div class='grid-item' style='background-color: {color};'>{num if num > 0 else ''}</div>"
    board_html += "</div>"
    
    st.markdown(board_html, unsafe_allow_html=True)

display_board()

col1, col2, col3, col4 = st.columns(4)
if col1.button("⬅ Left"):
    update_board("Left")
if col2.button("➡ Right"):
    update_board("Right")
if col3.button("⬆ Up"):
    update_board("Up")
if col4.button("⬇ Down"):
    update_board("Down")
