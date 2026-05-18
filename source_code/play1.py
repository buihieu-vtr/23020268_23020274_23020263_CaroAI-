import pygame
import utils1 as utils
import AI1 as AI

CELL_SIZE = 60
MARGIN = 40

WIDTH = (utils.BOARD_SIZE - 1) * CELL_SIZE + MARGIN * 2
HEIGHT = WIDTH + 60

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro AI")

font = pygame.font.SysFont(None, 45)
small_font = pygame.font.SysFont(None, 30)
menu_font = pygame.font.SysFont(None, 32)

board = utils.create_board()

game_over = False
winner = None

# Hệ thống quản lý màn hình: 
# 'MENU_ALGO' (Chọn thuật toán) -> 'MENU_TURN' (Chọn lượt đi) -> 'PLAYING' (Trong trận)
game_state = 'MENU_ALGO' 


def draw_menu_algo():
    """Bước 1: Vẽ màn hình chọn thuật toán xử lý"""
    screen.fill((220, 220, 220))
    
    title_text = font.render("CHOOSE AI ALGORITHM", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Nút bấm 1: Chỉ chạy Minimax thuần túy
    pygame.draw.rect(screen, (100, 150, 200), (WIDTH // 2 - 160, HEIGHT // 2 - 50, 320, 50))
    algo1_text = menu_font.render("1. MINIMAX ONLY (Slower)", True, (0, 0, 0))
    algo1_rect = algo1_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25))
    screen.blit(algo1_text, algo1_rect)

    # Nút bấm 2: Chạy Minimax tích hợp cắt tỉa Alpha-Beta
    pygame.draw.rect(screen, (100, 200, 150), (WIDTH // 2 - 160, HEIGHT // 2 + 30, 320, 50))
    algo2_text = menu_font.render("2. MINIMAX + ALPHA-BETA", True, (0, 0, 0))
    algo2_rect = algo2_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 55))
    screen.blit(algo2_text, algo2_rect)


def draw_menu_turn():
    """Bước 2: Vẽ màn hình chọn ai là người đi trước"""
    screen.fill((220, 220, 220))
    
    title_text = font.render("CHOOSE WHO GOES FIRST", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Nút bấm 1: Người đi trước
    pygame.draw.rect(screen, (240, 200, 80), (WIDTH // 2 - 140, HEIGHT // 2 - 50, 280, 50))
    p_text = menu_font.render("1. PLAYER FIRST", True, (0, 0, 0))
    p_rect = p_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25))
    screen.blit(p_text, p_rect)

    # Nút bấm 2: Máy đi trước
    pygame.draw.rect(screen, (200, 100, 100), (WIDTH // 2 - 140, HEIGHT // 2 + 30, 280, 50))
    ai_text = menu_font.render("2. AI FIRST", True, (0, 0, 0))
    ai_rect = ai_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 55))
    screen.blit(ai_text, ai_rect)


def draw_board():
    screen.fill((245, 222, 179))

    # 1. Vẽ các đường dọc trên bàn cờ
    for i in range(utils.BOARD_SIZE):
        x = MARGIN + i * CELL_SIZE
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (x, MARGIN),
            (x, MARGIN + CELL_SIZE * (utils.BOARD_SIZE - 1)),
            2
        )

    # 2. Vẽ các đường ngang trên bàn cờ (ĐÃ SỬA LỖI TỌA ĐỘ TẠI ĐÂY)
    for i in range(utils.BOARD_SIZE):
        y = MARGIN + i * CELL_SIZE
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (MARGIN, y),
            (MARGIN + CELL_SIZE * (utils.BOARD_SIZE - 1), y),
            2
        )

    # 3. Vẽ quân cờ X và O
    for r in range(utils.BOARD_SIZE):
        for c in range(utils.BOARD_SIZE):
            x = MARGIN + c * CELL_SIZE
            y = MARGIN + r * CELL_SIZE

            if board[r][c] == utils.HUMAN:
                text = font.render("X", True, (0, 0, 0))
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)

            elif board[r][c] == utils.AI:
                text = font.render("O", True, (139, 0, 0))
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)

    if game_over:
        if winner == utils.HUMAN:
            msg = "PLAYER WIN! Press R to Reset"
        elif winner == utils.AI:
            msg = "AI WIN! Press R to Reset"
        else:
            msg = "DRAW! Press R to Reset"

        text = small_font.render(msg, True, (0, 0, 0))
        screen.blit(text, (20, HEIGHT - 40))


running = True

while running:
    if game_state == 'MENU_ALGO':
        draw_menu_algo()
    elif game_state == 'MENU_TURN':
        draw_menu_turn()
    else:
        draw_board()
        
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board = utils.create_board()
                game_over = False
                winner = None
                game_state = 'MENU_ALGO'  # Quay về màn hình chọn thuật toán ban đầu

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Xử lý Click tại màn hình chọn thuật toán
            if game_state == 'MENU_ALGO':
                if WIDTH // 2 - 160 <= mx <= WIDTH // 2 + 160 and HEIGHT // 2 - 50 <= my <= HEIGHT // 2:
                    AI.USE_ALPHA_BETA = False  # Tắt cắt tỉa Alpha-Beta
                    game_state = 'MENU_TURN'
                elif WIDTH // 2 - 160 <= mx <= WIDTH // 2 + 160 and HEIGHT // 2 + 30 <= my <= HEIGHT // 2 + 80:
                    AI.USE_ALPHA_BETA = True   # Bật cắt tỉa Alpha-Beta
                    game_state = 'MENU_TURN'

            # Xử lý Click tại màn hình chọn lượt đi
            elif game_state == 'MENU_TURN':
                if WIDTH // 2 - 140 <= mx <= WIDTH // 2 + 140 and HEIGHT // 2 - 50 <= my <= HEIGHT // 2:
                    game_state = 'PLAYING'
                elif WIDTH // 2 - 140 <= mx <= WIDTH // 2 + 140 and HEIGHT // 2 + 30 <= my <= HEIGHT // 2 + 80:
                    game_state = 'PLAYING'
                    AI.ai_move(board)

            # Xử lý sự kiện đánh cờ trong trận đấu
            elif game_state == 'PLAYING' and not game_over:
                col = round((mx - MARGIN) / CELL_SIZE)
                row = round((my - MARGIN) / CELL_SIZE)

                if utils.inside(row, col) and board[row][col] == utils.EMPTY:
                    board[row][col] = utils.HUMAN

                    if utils.check_win(board, utils.HUMAN):
                        game_over = True
                        winner = utils.HUMAN
                        continue

                    if utils.board_full(board):
                        game_over = True
                        winner = 0
                        continue

                    AI.ai_move(board)

                    if utils.check_win(board, utils.AI):
                        game_over = True
                        winner = utils.AI
                    elif utils.board_full(board):
                        game_over = True
                        winner = 0

pygame.quit()