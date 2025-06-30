import streamlit as st
import random
import time
from typing import List, Optional, Tuple

st.set_page_config(
    page_title="Tic-Tac-Toe Pro",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def load_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3), transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3), transparent 50%),
            radial-gradient(ellipse at top, #1e1b4b 0%, #0f0f23 50%, #000000 100%);
        font-family: 'Space Grotesk', sans-serif;
        color: #ffffff;
        min-height: 100vh;
    }
    
    .main-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.2rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #60a5fa 0%, #c084fc 30%, #f59e0b 70%, #ef4444 100%);
        -webkit-background-clip: text;
        # -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        letter-spacing: -2px;
        text-shadow: 0 0 30px rgba(96, 165, 250, 0.3);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: brightness(1) drop-shadow(0 0 5px rgba(96, 165, 250, 0.3)); }
        to { filter: brightness(1.1) drop-shadow(0 0 15px rgba(192, 132, 252, 0.4)); }
    }
    
    .game-arena {
        background: 
            linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 32px;
        padding: 3rem;
        margin: 2rem auto;
        box-shadow: 
            0 32px 64px -12px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        max-width: 520px;
        position: relative;
        overflow: hidden;
    }
    
    .game-arena::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(96, 165, 250, 0.1), rgba(192, 132, 252, 0.1));
        border-radius: 32px;
        pointer-events: none;
        opacity: 0.5;
    }
    
    .board-container {
        background: 
            linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        border-radius: 24px;
        padding: 32px;
        margin: 32px 0;
        border: 2px solid rgba(100, 116, 139, 0.2);
        box-shadow: 
            inset 0 2px 8px rgba(0, 0, 0, 0.4),
            0 8px 32px rgba(96, 165, 250, 0.1);
        position: relative;
        z-index: 1;
    }
    
    .board-container::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            rgba(96, 165, 250, 0.3), 
            rgba(192, 132, 252, 0.3), 
            rgba(245, 158, 11, 0.3)
        );
        border-radius: 24px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .board-container:hover::before {
        opacity: 1;
    }
    
    .status-bar {
        text-align: center;
        font-size: 1.4rem;
        font-weight: 600;
        padding: 20px 32px;
        background: rgba(30, 41, 59, 0.9);
        border-radius: 16px;
        border: 2px solid rgba(100, 116, 139, 0.3);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .status-bar::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.8s ease;
    }
    
    .status-bar:hover::before {
        left: 100%;
    }
    
    .status-bar.winning {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(6, 182, 212, 0.15));
        border-color: rgba(34, 197, 94, 0.5);
        color: #22c55e;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.2);
        animation: winPulse 1.5s ease-in-out infinite;
    }
    
    .status-bar.losing {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(249, 115, 22, 0.15));
        border-color: rgba(239, 68, 68, 0.5);
        color: #ef4444;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
        animation: losePulse 1.5s ease-in-out infinite;
    }
    
    @keyframes winPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(34, 197, 94, 0.2); }
        50% { transform: scale(1.02); box-shadow: 0 0 30px rgba(34, 197, 94, 0.4); }
    }
    
    @keyframes losePulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(239, 68, 68, 0.2); }
        50% { transform: scale(1.02); box-shadow: 0 0 30px rgba(239, 68, 68, 0.4); }
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 32px 0;
    }
    
    .stat-card {
        background: rgba(30, 41, 59, 0.7);
        border: 2px solid rgba(100, 116, 139, 0.2);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: rgba(148, 163, 184, 0.5);
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-number {
        font-size: 2.4rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 8px;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover .stat-number {
        transform: scale(1.1);
    }
    
    .stat-label {
        font-size: 0.95rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .wins .stat-number { 
        color: #22c55e; 
        text-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
    }
    .draws .stat-number { 
        color: #f59e0b; 
        text-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
    }
    .losses .stat-number { 
        color: #ef4444; 
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 16px 28px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid rgba(255, 255, 255, 0.1);
        width: 100%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.4);
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #9333ea);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Enhanced Game Cell Styling */
    div[data-testid="column"] > div > div > button {
        height: 90px !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important;
        background: linear-gradient(145deg, #334155, #1e293b) !important;
        border: 3px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 20px !important;
        color: white !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 
            0 4px 15px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }
    
    div[data-testid="column"] > div > div > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.1), rgba(192, 132, 252, 0.1)) !important;
        opacity: 0 !important;
        transition: opacity 0.3s ease !important;
        border-radius: 17px !important;
    }
    
    div[data-testid="column"] > div > div > button:hover:not(:disabled) {
        border-color: rgba(96, 165, 250, 0.8) !important;
        background: linear-gradient(145deg, #3730a3, #1e1b4b) !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 
            0 12px 30px rgba(96, 165, 250, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    div[data-testid="column"] > div > div > button:hover:not(:disabled)::before {
        opacity: 1 !important;
    }
    
    div[data-testid="column"] > div > div > button:disabled {
        opacity: 1 !important;
        cursor: default !important;
    }
    
    /* X and O styling with animations */
    div[data-testid="column"] > div > div > button:disabled {
        animation: cellAppear 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
    }
    
    @keyframes cellAppear {
        0% {
            transform: scale(0) rotate(180deg);
            opacity: 0;
        }
        100% {
            transform: scale(1) rotate(0deg);
            opacity: 1;
        }
    }
    
    /* X symbol styling */
    div[data-testid="column"] > div > div > button[disabled]:contains("✕") {
        color: #ef4444 !important;
        text-shadow: 
            0 0 15px rgba(239, 68, 68, 0.6),
            0 0 30px rgba(239, 68, 68, 0.3) !important;
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.1), rgba(185, 28, 28, 0.1)) !important;
        border-color: rgba(239, 68, 68, 0.4) !important;
    }
    
    /* O symbol styling */
    div[data-testid="column"] > div > div > button[disabled]:contains("◯") {
        color: #3b82f6 !important;
        text-shadow: 
            0 0 15px rgba(59, 130, 246, 0.6),
            0 0 30px rgba(59, 130, 246, 0.3) !important;
        background: linear-gradient(145deg, rgba(59, 130, 246, 0.1), rgba(29, 78, 216, 0.1)) !important;
        border-color: rgba(59, 130, 246, 0.4) !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 2px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(148, 163, 184, 0.5) !important;
        box-shadow: 0 4px 15px rgba(96, 165, 250, 0.1) !important;
    }
    
    .difficulty-indicator {
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
        margin-top: 8px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .easy { 
        background: rgba(34, 197, 94, 0.2); 
        color: #22c55e; 
        border-color: rgba(34, 197, 94, 0.3);
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.2);
    }
    .medium { 
        background: rgba(251, 191, 36, 0.2); 
        color: #fbbf24; 
        border-color: rgba(251, 191, 36, 0.3);
        box-shadow: 0 0 10px rgba(251, 191, 36, 0.2);
    }
    .hard { 
        background: rgba(239, 68, 68, 0.2); 
        color: #ef4444; 
        border-color: rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
    }
    
    /* Winning line animation */
    .winning-line {
        position: absolute;
        background: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.8), transparent);
        height: 4px;
        border-radius: 2px;
        animation: winningLineGlow 2s ease-in-out infinite;
    }
    
    @keyframes winningLineGlow {
        0%, 100% { opacity: 0.6; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
            letter-spacing: -1px;
        }
        
        .game-arena {
            padding: 2rem;
            margin: 1rem;
        }
        
        .board-container {
            padding: 20px;
        }
        
        div[data-testid="column"] > div > div > button {
            height: 75px !important;
            font-size: 2.2rem !important;
        }
        
        .stats-grid {
            gap: 12px;
        }
        
        .stat-card {
            padding: 16px;
        }
        
        .stat-number {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

class GameAI:
    def __init__(self, difficulty="Hard"):
        self.difficulty = difficulty
        self.winning_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
    
    def evaluate_position(self, board, depth, maximizing):
        winner = self.find_winner(board)
        if winner == 'O':
            return 10 - depth
        elif winner == 'X':
            return depth - 10
        elif not self.has_empty_cells(board):
            return 0
        
        if maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.evaluate_position(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.evaluate_position(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(best_score, score)
            return best_score
    
    def find_winner(self, board):
        for pattern in self.winning_patterns:
            if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != '':
                return board[pattern[0]]
        return None
    
    def has_empty_cells(self, board):
        return '' in board
    
    def get_move(self, board):
        empty_positions = [i for i in range(9) if board[i] == '']
        
        if self.difficulty == "Easy":
            return random.choice(empty_positions) if random.random() < 0.7 else self.calculate_best_move(board)
        elif self.difficulty == "Medium":
            return self.calculate_best_move(board) if random.random() < 0.8 else random.choice(empty_positions)
        else:
            return self.calculate_best_move(board)
    
    def calculate_best_move(self, board):
        best_move = 0
        best_score = float('-inf')
        
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = self.evaluate_position(board, 0, False)
                board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move

class GameEngine:
    def __init__(self):
        self.init_session_state()
        self.winning_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
    
    def init_session_state(self):
        if 'game_data' not in st.session_state:
            st.session_state.game_data = {
                'board': [''] * 9,
                'active': True,
                'winner': None,
                'winning_cells': [],
                'stats': {'wins': 0, 'draws': 0, 'losses': 0},
                'move_number': 0,
                'ai_level': 'Hard'
            }
        
        # Initialize AI with current difficulty level
        if 'ai' not in st.session_state:
            st.session_state.ai = GameAI(st.session_state.game_data['ai_level'])
    
    def reset_board(self):
        current_stats = st.session_state.game_data['stats']
        current_ai_level = st.session_state.game_data['ai_level']
        st.session_state.game_data = {
            'board': [''] * 9,
            'active': True,
            'winner': None,
            'winning_cells': [],
            'stats': current_stats,
            'move_number': 0,
            'ai_level': current_ai_level
        }
    
    def check_game_end(self):
        board = st.session_state.game_data['board']
        
        for pattern in self.winning_patterns:
            if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != '':
                st.session_state.game_data['winner'] = board[pattern[0]]
                st.session_state.game_data['winning_cells'] = pattern
                st.session_state.game_data['active'] = False
                
                if board[pattern[0]] == 'X':
                    st.session_state.game_data['stats']['wins'] += 1
                else:
                    st.session_state.game_data['stats']['losses'] += 1
                return True
        
        if '' not in board:
            st.session_state.game_data['active'] = False
            st.session_state.game_data['stats']['draws'] += 1
            return True
        
        return False
    
    def execute_move(self, position):
        if (st.session_state.game_data['board'][position] == '' and 
            st.session_state.game_data['active']):
            
            st.session_state.game_data['board'][position] = 'X'
            st.session_state.game_data['move_number'] += 1
            
            if self.check_game_end():
                return
            
            time.sleep(0.1)
            ai_position = st.session_state.ai.get_move(st.session_state.game_data['board'])
            st.session_state.game_data['board'][ai_position] = 'O'
            st.session_state.game_data['move_number'] += 1
            
            self.check_game_end()
    
    def get_status_message(self):
        if not st.session_state.game_data['active']:
            winner = st.session_state.game_data['winner']
            if winner == 'X':
                return "🎉 Outstanding Victory! You conquered the AI!"
            elif winner == 'O':
                return "🤖 AI Triumphs! Challenge accepted?"
            else:
                return "🤝 Epic Draw! Perfectly matched skills!"
        return f"🎯 Your Turn - Make it count!"
    
    def get_status_class(self):
        if not st.session_state.game_data['active']:
            winner = st.session_state.game_data['winner']
            if winner == 'X':
                return "winning"
            elif winner == 'O':
                return "losing"
        return ""
    
    def get_cell_symbol(self, cell_value):
        if cell_value == 'X':
            return "✕"
        elif cell_value == 'O':
            return "◯"
        return ""
    
    def render_game_board(self):
        board = st.session_state.game_data['board']
        winning_cells = st.session_state.game_data['winning_cells']
        
        st.markdown('<div class="board-container">', unsafe_allow_html=True)
        
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                cell_idx = row * 3 + col
                cell_value = board[cell_idx]
                is_disabled = cell_value != '' or not st.session_state.game_data['active']
                
                with cols[col]:
                    cell_symbol = self.get_cell_symbol(cell_value)
                    
                    if st.button(
                        cell_symbol,
                        key=f"cell_{cell_idx}",
                        disabled=is_disabled,
                        use_container_width=True
                    ):
                        self.execute_move(cell_idx)
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    load_styles()
    
    st.markdown('<h1 class="main-title">TIC-TAC-TOE PRO</h1>', unsafe_allow_html=True)
    
    game = GameEngine()
    
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    
    with col1:
        if st.button("🎮 New Game", use_container_width=True):
            game.reset_board()
            st.rerun()
    
    with col2:
        difficulty = st.selectbox(
            "🤖 AI Difficulty Level",
            ["Easy", "Medium", "Hard"],
            index=["Easy", "Medium", "Hard"].index(st.session_state.game_data['ai_level']),
            key="difficulty_selector"
        )
        
        if difficulty != st.session_state.game_data['ai_level']:
            st.session_state.game_data['ai_level'] = difficulty
            st.session_state.ai = GameAI(difficulty)
        
        difficulty_class = difficulty.lower()
        difficulty_emojis = {"Easy": "😊", "Medium": "🤔", "Hard": "😈"}
        st.markdown(f'<div class="difficulty-indicator {difficulty_class}">{difficulty_emojis[difficulty]} {difficulty} Mode</div>', 
                   unsafe_allow_html=True)
    
    with col3:
        if st.button("📊 Reset Stats", use_container_width=True):
            st.session_state.game_data['stats'] = {'wins': 0, 'draws': 0, 'losses': 0}
            st.rerun()
    
    st.markdown('<div class="game-arena">', unsafe_allow_html=True)
    
    status_class = game.get_status_class()
    status_message = game.get_status_message()
    st.markdown(f'<div class="status-bar {status_class}">{status_message}</div>', 
               unsafe_allow_html=True)
    
    game.render_game_board()
    
    stats = st.session_state.game_data['stats']
    total_games = stats['wins'] + stats['draws'] + stats['losses']
    win_rate = (stats['wins'] / total_games * 100) if total_games > 0 else 0
    
    st.markdown(f'''
    <div class="stats-grid">
        <div class="stat-card wins">
            <div class="stat-number">{stats['wins']}</div>
            <div class="stat-label">🏆 Victories</div>
        </div>
        <div class="stat-card draws">
            <div class="stat-number">{stats['draws']}</div>
            <div class="stat-label">🤝 Draws</div>
        </div>
        <div class="stat-card losses">
            <div class="stat-number">{stats['losses']}</div>
            <div class="stat-label">💪 Challenges</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    if total_games > 0:
        st.markdown(f'''
        <div style="text-align: center; margin-top: 16px; padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; border: 1px solid rgba(100, 116, 139, 0.2);">
            <span style="font-size: 1.1rem; font-weight: 600; color: #60a5fa;">
                🎯 Win Rate: {win_rate:.1f}% ({total_games} games played)
            </span>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()