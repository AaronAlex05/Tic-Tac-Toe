import pygame
import sys
from game_logic import TicTacToe

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
BOARD_SIZE = 450
CELL_SIZE = BOARD_SIZE // 3
OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
OFFSET_Y = (SCREEN_HEIGHT - BOARD_SIZE) // 2 - 50
LINE_WIDTH = 10

# Theme Colors (Cyberpunk Edition)
LINE_COLOR = (20, 20, 40)          # Deep cyberpunk navy
BG_COLOR = (10, 10, 20)            # Darkest space (fallback)
X_COLOR = (0, 255, 255)            # Neon Cyan
O_COLOR = (255, 0, 255)            # Neon Magenta
TEXT_COLOR = (255, 255, 255)       # Pure white
BUTTON_COLOR = (40, 20, 80)        # Deep Cyber Purple
BUTTON_HOVER_COLOR = (60, 30, 120)  # Lighter Cyber Purple

# States
STATE_MENU = "MENU"
STATE_MODE_SELECTION = "MODE_SELECTION"
STATE_GAME = "GAME"
STATE_GAMEOVER = "GAMEOVER"
STATE_HOW_TO_PLAY = "HOW_TO_PLAY"

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Cyberpunk Edition")
font = pygame.font.SysFont("Arial", 40, bold=True)
small_font = pygame.font.SysFont("Arial", 28, bold=True)
title_font = pygame.font.SysFont("Arial", 80, bold=True)
result_font = pygame.font.SysFont("Arial", 60, bold=True)
 
# Initialize Audio
try:
    pygame.mixer.init()
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
except Exception as e:
    print(f"Warning: Could not load background music: {e}")

# Load Background
try:
    # Try multiple common extensions
    background_raw = None
    for ext in ['jpg', 'png', 'jpeg']:
        try:
            background_raw = pygame.image.load(f"background.{ext}").convert()
            break
        except:
            continue
            
    if background_raw:
        BACKGROUND_IMG = pygame.transform.scale(background_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        BACKGROUND_IMG = None
except:
    BACKGROUND_IMG = None

def draw_background():
    if BACKGROUND_IMG:
        screen.blit(BACKGROUND_IMG, (0, 0))
    else:
        screen.fill(BG_COLOR)

def draw_menu():
    draw_background()
    
    # Title with subtle shadow for readability
    title_shadow = title_font.render("TIC TAC TOE", True, (50, 50, 50))
    title_label = title_font.render("TIC TAC TOE", True, TEXT_COLOR)
    
    title_rect = title_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
    screen.blit(title_label, title_rect)
    
    mouse_pos = pygame.mouse.get_pos()
    
    # List of buttons to draw
    buttons = [
        ("START GAME", 0),
        ("HOW TO PLAY", 90),
        ("EXIT GAME", 180)
    ]
    
    button_rects = []
    
    for text, offset in buttons:
        btn_rect = pygame.Rect(0, 0, 300, 70)
        btn_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + offset)
        color = BUTTON_HOVER_COLOR if btn_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        
        pygame.draw.rect(screen, color, btn_rect, border_radius=15)
        pygame.draw.rect(screen, TEXT_COLOR, btn_rect, 3, border_radius=15)
        
        btn_label = font.render(text, True, TEXT_COLOR)
        btn_text_rect = btn_label.get_rect(center=btn_rect.center)
        screen.blit(btn_label, btn_text_rect)
        button_rects.append(btn_rect)
    
    return button_rects[0], button_rects[1], button_rects[2]

def draw_how_to_play():
    draw_background()
    
    # Overlay for text readability
    overlay = pygame.Surface((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (50, 100))
    
    title_label = result_font.render("HOW TO PLAY", True, TEXT_COLOR)
    title_rect = title_label.get_rect(center=(SCREEN_WIDTH // 2, 160))
    screen.blit(title_label, title_rect)
    
    instructions = [
        "1. Select a game mode: PvP or PvC.",
        "2. Players take turns placing X and O.",
        "3. First to get 3 in a row, col, or diagonal wins!",
        "4. Computer (PvC) uses Minimax algorithm.",
        "5. It is unbeatable - try to get a draw!",
        "",
        "Press any key or click to return to Menu"
    ]
    
    y_offset = 240
    for line in instructions:
        line_label = small_font.render(line, True, TEXT_COLOR)
        line_rect = line_label.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(line_label, line_rect)
        y_offset += 50

def draw_mode_selection():
    draw_background()
    
    # Title
    title_label = result_font.render("CHOOSE MODE", True, TEXT_COLOR)
    title_rect = title_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    # Shadow
    title_shadow = result_font.render("CHOOSE MODE", True, (50, 50, 50))
    screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
    screen.blit(title_label, title_rect)
    
    mouse_pos = pygame.mouse.get_pos()
    
    # PvP Button
    pvp_rect = pygame.Rect(0, 0, 360, 70)
    pvp_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    color_pvp = BUTTON_HOVER_COLOR if pvp_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color_pvp, pvp_rect, border_radius=15)
    pygame.draw.rect(screen, TEXT_COLOR, pvp_rect, 3, border_radius=15)
    
    pvp_label = font.render("VS PLAYER", True, TEXT_COLOR)
    pvp_text_rect = pvp_label.get_rect(center=pvp_rect.center)
    screen.blit(pvp_label, pvp_text_rect)
    
    # PvC Button
    pvc_rect = pygame.Rect(0, 0, 360, 70)
    pvc_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    color_pvc = BUTTON_HOVER_COLOR if pvc_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color_pvc, pvc_rect, border_radius=15)
    pygame.draw.rect(screen, TEXT_COLOR, pvc_rect, 3, border_radius=15)
    
    pvc_label = font.render("VS COMPUTER", True, TEXT_COLOR)
    pvc_text_rect = pvc_label.get_rect(center=pvc_rect.center)
    screen.blit(pvc_label, pvc_text_rect)
    
    return pvp_rect, pvc_rect

def draw_game_over(game):
    draw_background()
    
    # Result Title
    if game.winner:
        if game.mode == "PvC" and game.winner == "O":
            text = "COMPUTER WINS!"
        else:
            text = f"PLAYER {game.winner} WINS!"
    else:
        text = "IT'S A DRAW!"
    
    result_label = result_font.render(text, True, TEXT_COLOR)
    result_rect = result_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    # Shadow
    result_shadow = result_font.render(text, True, (50, 50, 50))
    screen.blit(result_shadow, (rect.x + 3, rect.y + 3) if 'rect' in locals() else (result_rect.x + 3, result_rect.y + 3))
    screen.blit(result_label, result_rect)
    
    # Buttons
    mouse_pos = pygame.mouse.get_pos()
    
    # New Round Button
    new_round_rect = pygame.Rect(0, 0, 280, 70)
    new_round_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    color_nr = BUTTON_HOVER_COLOR if new_round_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color_nr, new_round_rect, border_radius=15)
    pygame.draw.rect(screen, TEXT_COLOR, new_round_rect, 3, border_radius=15)
    
    nr_label = font.render("NEW ROUND", True, TEXT_COLOR)
    nr_rect = nr_label.get_rect(center=new_round_rect.center)
    screen.blit(nr_label, nr_rect)
    
    # Exit Button
    exit_rect = pygame.Rect(0, 0, 280, 70)
    exit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    color_exit = BUTTON_HOVER_COLOR if exit_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color_exit, exit_rect, border_radius=15)
    pygame.draw.rect(screen, TEXT_COLOR, exit_rect, 3, border_radius=15)
    
    exit_label = font.render("EXIT GAME", True, TEXT_COLOR)
    exit_rect_text = exit_label.get_rect(center=exit_rect.center)
    screen.blit(exit_label, exit_rect_text)
    
    return new_round_rect, exit_rect

def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (OFFSET_X, OFFSET_Y + CELL_SIZE), (OFFSET_X + BOARD_SIZE, OFFSET_Y + CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET_X, OFFSET_Y + 2 * CELL_SIZE), (OFFSET_X + BOARD_SIZE, OFFSET_Y + 2 * CELL_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (OFFSET_X + CELL_SIZE, OFFSET_Y), (OFFSET_X + CELL_SIZE, OFFSET_Y + BOARD_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET_X + 2 * CELL_SIZE, OFFSET_Y), (OFFSET_X + 2 * CELL_SIZE, OFFSET_Y + BOARD_SIZE), LINE_WIDTH)

def draw_figures(game):
    for row in range(3):
        for col in range(3):
            center_x = OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
            center_y = OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
            
            if game.board[row][col] == "X":
                # Draw X with shadow for pop
                offset = 40
                pygame.draw.line(screen, LINE_COLOR, (center_x - CELL_SIZE // 2 + offset + 2, center_y - CELL_SIZE // 2 + offset + 2), 
                                 (center_x + CELL_SIZE // 2 - offset + 2, center_y + CELL_SIZE // 2 - offset + 2), LINE_WIDTH + 5)
                pygame.draw.line(screen, X_COLOR, (center_x - CELL_SIZE // 2 + offset, center_y - CELL_SIZE // 2 + offset), 
                                 (center_x + CELL_SIZE // 2 - offset, center_y + CELL_SIZE // 2 - offset), LINE_WIDTH + 5)
                                 
                pygame.draw.line(screen, LINE_COLOR, (center_x - CELL_SIZE // 2 + offset + 2, center_y + CELL_SIZE // 2 - offset + 2), 
                                 (center_x + CELL_SIZE // 2 - offset + 2, center_y - CELL_SIZE // 2 + offset + 2), LINE_WIDTH + 5)
                pygame.draw.line(screen, X_COLOR, (center_x - CELL_SIZE // 2 + offset, center_y + CELL_SIZE // 2 - offset), 
                                 (center_x + CELL_SIZE // 2 - offset, center_y - CELL_SIZE // 2 + offset), LINE_WIDTH + 5)
            elif game.board[row][col] == "O":
                # Draw O with shadow
                pygame.draw.circle(screen, LINE_COLOR, (center_x + 2, center_y + 2), CELL_SIZE // 2 - 40, LINE_WIDTH + 5)
                pygame.draw.circle(screen, O_COLOR, (center_x, center_y), CELL_SIZE // 2 - 40, LINE_WIDTH + 5)

def display_status(game, ai_thinking=False):
    if game.winner:
        text = f"Player {game.winner} Wins!"
        draw_winning_line(game)
    elif game.is_draw:
        text = "It's a Draw!"
    elif ai_thinking:
        text = "Computer is thinking..."
    else:
        text = f"Player {game.current_player}'s Turn"
    
    # Shadow text for readability on image
    label_shadow = font.render(text, True, (50, 50, 50))
    label = font.render(text, True, TEXT_COLOR)
    
    rect = label.get_rect(center=(SCREEN_WIDTH // 2, OFFSET_Y + BOARD_SIZE + 70))
    screen.blit(label_shadow, (rect.x + 2, rect.y + 2))
    screen.blit(label, rect)

def draw_winning_line(game):
    if not game.winning_line:
        return
    
    (r1, c1), (r2, c2) = game.winning_line
    
    start_pos = (OFFSET_X + c1 * CELL_SIZE + CELL_SIZE // 2, OFFSET_Y + r1 * CELL_SIZE + CELL_SIZE // 2)
    end_pos = (OFFSET_X + c2 * CELL_SIZE + CELL_SIZE // 2, OFFSET_Y + r2 * CELL_SIZE + CELL_SIZE // 2)
    
    # Use dark purple for the winning line to make it clearly visible
    pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, LINE_WIDTH + 15)
    color = X_COLOR if game.winner == "X" else O_COLOR
    pygame.draw.line(screen, color, start_pos, end_pos, LINE_WIDTH + 5)

def main():
    game = TicTacToe()
    current_state = STATE_MENU
    game_over_timer = 0
    ai_timer = 0
    clock = pygame.time.Clock()
    
    # Initialize button rects to avoid NameError during state transitions
    start_btn = pygame.Rect(0, 0, 0, 0)
    how_btn = pygame.Rect(0, 0, 0, 0)
    exit_btn = pygame.Rect(0, 0, 0, 0)
    pvp_rect = pygame.Rect(0, 0, 0, 0)
    pvc_rect = pygame.Rect(0, 0, 0, 0)
    new_round_rect = pygame.Rect(0, 0, 0, 0)
    exit_rect = pygame.Rect(0, 0, 0, 0)
    
    while True:
        if current_state == STATE_MENU:
            start_btn, how_btn, exit_btn = draw_menu()
        elif current_state == STATE_MODE_SELECTION:
            pvp_rect, pvc_rect = draw_mode_selection()
        elif current_state == STATE_HOW_TO_PLAY:
            draw_how_to_play()
        elif current_state == STATE_GAMEOVER:
            new_round_rect, exit_rect = draw_game_over(game)
        else:
            draw_background()
            
            # Semi-transparent overlay behind the grid
            overlay = pygame.Surface((BOARD_SIZE + 20, BOARD_SIZE + 20), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 100))  # Semi-transparent white
            screen.blit(overlay, (OFFSET_X - 10, OFFSET_Y - 10))
            
            draw_lines()
            draw_figures(game)
            display_status(game, ai_thinking=(ai_timer > 0))
            
            # Handle AI turn with delay
            if game.mode == "PvC" and game.current_player == "O" and not game.winner and not game.is_draw:
                if ai_timer == 0:
                    ai_timer = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - ai_timer > 1000:  # 1 second thinking time
                    game.ai_move()
                    ai_timer = 0
            
            # Auto-redirect to Game Over screen after delay
            if game.winner or game.is_draw:
                if game_over_timer == 0:
                    game_over_timer = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - game_over_timer > 1500:  # 1.5 seconds delay
                    current_state = STATE_GAMEOVER
                    game_over_timer = 0
                    ai_timer = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if current_state == STATE_HOW_TO_PLAY:
                    current_state = STATE_MENU
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                
                if current_state == STATE_MENU:
                    if start_btn.collidepoint(mouseX, mouseY):
                        current_state = STATE_MODE_SELECTION
                    elif how_btn.collidepoint(mouseX, mouseY):
                        current_state = STATE_HOW_TO_PLAY
                    elif exit_btn.collidepoint(mouseX, mouseY):
                        pygame.quit()
                        sys.exit()
                elif current_state == STATE_HOW_TO_PLAY:
                    current_state = STATE_MENU
                elif current_state == STATE_MODE_SELECTION:
                    if pvp_rect.collidepoint(mouseX, mouseY):
                        game.mode = "PvP"
                        current_state = STATE_GAME
                    elif pvc_rect.collidepoint(mouseX, mouseY):
                        game.mode = "PvC"
                        current_state = STATE_GAME
                elif current_state == STATE_GAMEOVER:
                    if new_round_rect.collidepoint(mouseX, mouseY):
                        game.reset()
                        ai_timer = 0
                        game_over_timer = 0
                        current_state = STATE_GAME
                    elif exit_rect.collidepoint(mouseX, mouseY):
                        pygame.quit()
                        sys.exit()
                else:
                    if not game.winner and not game.is_draw:
                        if (game.mode == "PvP" or game.current_player == "X") and ai_timer == 0:
                            if OFFSET_X <= mouseX < OFFSET_X + BOARD_SIZE and OFFSET_Y <= mouseY < OFFSET_Y + BOARD_SIZE:
                                clicked_row = (mouseY - OFFSET_Y) // CELL_SIZE
                                clicked_col = (mouseX - OFFSET_X) // CELL_SIZE
                                game.make_move(clicked_row, clicked_col)
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
