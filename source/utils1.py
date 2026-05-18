BOARD_SIZE = 9
WIN_LENGTH = 4

EMPTY = 0
HUMAN = 1
AI = -1


def create_board():
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def inside(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def board_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True


def get_empty_cells_near(board):
    candidates = set()
    has_piece = False

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:
                has_piece = True
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr = r + dr
                        nc = c + dc
                        if inside(nr, nc) and board[nr][nc] == EMPTY:
                            candidates.add((nr, nc))

    if not has_piece:
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

    return list(candidates)


def check_win(board, player):
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != player:
                continue

            for dr, dc in directions:
                count = 0
                for i in range(WIN_LENGTH):
                    nr = r + dr * i
                    nc = c + dc * i
                    if inside(nr, nc) and board[nr][nc] == player:
                        count += 1
                    else:
                        break

                if count >= WIN_LENGTH:
                    return True

    return False


def create_pattern_dict():
  
    patterns = {
        (AI, AI, AI, AI): 1000000,
        (HUMAN, HUMAN, HUMAN, HUMAN): -1000000,

        # Chuỗi 3 quân nguy hiểm - Ưu tiên chặn/hoàn thành cực cao
        (AI, AI, AI, EMPTY): 80000,
        (EMPTY, AI, AI, AI): 80000,
        (AI, EMPTY, AI, AI): 75000,
        (AI, AI, EMPTY, AI): 75000,

        (HUMAN, HUMAN, HUMAN, EMPTY): -85000,  # AI sợ người chơi có 3 quân nên điểm phòng thủ cao hơn tấn công
        (EMPTY, HUMAN, HUMAN, HUMAN): -85000,
        (HUMAN, EMPTY, HUMAN, HUMAN): -80000,
        (HUMAN, HUMAN, EMPTY, HUMAN): -80000,

        # Chuỗi 2 quân tạo đà
        (EMPTY, AI, AI, EMPTY): 10000,
        (EMPTY, HUMAN, HUMAN, EMPTY): -15000, # Tăng cường chặn đứng chuỗi 2 quân thoáng của người chơi từ sớm

        (AI, AI, EMPTY, EMPTY): 1200,
        (EMPTY, EMPTY, AI, AI): 1200,
        (HUMAN, HUMAN, EMPTY, EMPTY): -2000,
        (EMPTY, EMPTY, HUMAN, HUMAN): -2000,

        (AI, EMPTY, AI, EMPTY): 1000,
        (EMPTY, AI, EMPTY, AI): 1000,
        (HUMAN, EMPTY, HUMAN, EMPTY): -1500,
        (EMPTY, HUMAN, EMPTY, HUMAN): -1500,
    }
    return patterns


PATTERN_SCORES = create_pattern_dict()


def evaluate_line(line):
    line = tuple(line)
    if line in PATTERN_SCORES:
        return PATTERN_SCORES[line]
    return 0


def evaluate_board(board):
    if check_win(board, AI):
        return 1000000
    if check_win(board, HUMAN):
        return -1000000

    score = 0
    # ngang
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - 3):
            line = [board[r][c+i] for i in range(4)]
            score += evaluate_line(line)

    # dọc
    for c in range(BOARD_SIZE):
        for r in range(BOARD_SIZE - 3):
            line = [board[r+i][c] for i in range(4)]
            score += evaluate_line(line)

    # chéo \
    for r in range(BOARD_SIZE - 3):
        for c in range(BOARD_SIZE - 3):
            line = [board[r+i][c+i] for i in range(4)]
            score += evaluate_line(line)

    # chéo /
    for r in range(BOARD_SIZE - 3):
        for c in range(3, BOARD_SIZE):
            line = [board[r+i][c-i] for i in range(4)]
            score += evaluate_line(line)

    return score


def evaluate_move(board, r, c, player, current_score):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    old_local_score = 0
    new_local_score = 0

    # 1. Tính toán điểm số vùng trước khi đặt quân
    for dr, dc in directions:
        for shift in range(4):
            start_r = r - dr * shift
            start_c = c - dc * shift
            if inside(start_r, start_c) and inside(start_r + dr * 3, start_c + dc * 3):
                line = [board[start_r + dr * i][start_c + dc * i] for i in range(4)]
                old_local_score += evaluate_line(line)


    board[r][c] = player

    for dr, dc in directions:
        for shift in range(4):
            start_r = r - dr * shift
            start_c = c - dc * shift
            if inside(start_r, start_c) and inside(start_r + dr * 3, start_c + dc * 3):
                line = [board[start_r + dr * i][start_c + dc * i] for i in range(4)]
                new_local_score += evaluate_line(line)

     board[r][c] = EMPTY

    return current_score + new_local_score - old_local_score
