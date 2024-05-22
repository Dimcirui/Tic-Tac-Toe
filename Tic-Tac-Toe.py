import random

##  棋盘布局
##  0 1 2
##  3 4 5
##  6 7 8

##  设定获胜的组合方式
WINNING_TRIADS = [(0,1,2), (3,4,5), (6,7,8),
                  (0,3,6), (1,4,7), (2,5,8),
                  (0,4,8), (2,4,6)]

##  棋盘按一行三个打印
PRINTTING_TRIADS = [(0,1,2), (3,4,5), (6,7,8)]

##  初始化棋盘
SLOTS = [0,1,2,3,4,5,6,7,8]

##  定义：X为玩家，值为-1；O为电脑，值为1
X_token, Open_token, O_token = -1, 0, 1

MARKERS =  ['_', 'O', 'X']

##  显示棋盘
def print_board(board):
    for row in PRINTTING_TRIADS:
        r = ''
        for col in row:
            r += MARKERS[board[col]] + ''
        print(r)
    print()

##  判断当前是否有一方获胜
def winner(board):
    for triad in WINNING_TRIADS:
        if board[triad[0]] == board[triad[1]] == board[triad[2]] != Open_token:
            return board[triad[0]]

    if not legal_move_left(board):
        return 0

    return None

##  判断当前能否继续下棋子
def legal_move_left(board):
    return Open_token in board

##  递归计算最佳分值，使用AB剪枝算法进行优化
def alpha_beta_pruning(board, depth, alpha, beta, is_maximizing):
    win = winner(board)
    if win is not None:
        return win * (10 - depth)
    
    if not legal_move_left(board):
        return 0
    
    if is_maximizing:
        max_eval = -float('inf')
        for move in SLOTS:
            if board[move] == Open_token:
                board[move] = O_token
                eval = alpha_beta_pruning(board, depth + 1, alpha, beta, False)
                board[move] = Open_token
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for move in SLOTS:
            if board[move] == Open_token:
                board[move] = X_token
                eval = alpha_beta_pruning(board, depth + 1, alpha, beta, True)
                board[move] = Open_token
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

##  计算电脑的最优走法
def best_move(board, player):
    best_val = -float('inf')
    good_move = None

    for move in SLOTS:
        if board[move] == Open_token:
            board[move] = player
            move_val = alpha_beta_pruning(board, 0, -float('inf'), float('inf'), False)
            board[move] = Open_token

            if move_val > best_val:
                best_val = move_val
                good_move = move

    return good_move

def play_game():
    board = [Open_token] * 9
    cur_player = X_token
    
    while winner(board) is None and legal_move_left(board):
        print_board(board)

        if cur_player == X_token:
            move = int(input('X玩家，请输入你要下的位置（1~9）:')) - 1
            if not 0 <= move < 9:
                print('输入的不是合法位置（1~9），请重试！')
                continue
        else:
            move = best_move(board, O_token)

        if board[move] == Open_token:
            board[move] = cur_player
            cur_player = O_token if cur_player == X_token else X_token
        else:
            print('要下的位置已经有棋子了，请重试！')
            
    print_board(board)

    win = winner(board)
    if win == 0:
        print('游戏结束！平局。')
    elif win == O_token:
        print('游戏结束！电脑获胜。')
    else:
        print('游戏结束！你赢了！')

if __name__ == "__main__":
    play_game()