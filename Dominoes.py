import random
from datetime import datetime
from collections import Counter

STOCK = [[0,0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
         [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
         [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
         [3, 3], [3, 4], [3, 5], [3, 6],
         [4, 4], [4, 5], [4, 6],
         [5, 5], [5, 6],
         [6, 6]]

DOUBLES = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]

random.seed(datetime.now().timestamp())

def create_hand(stock, player):
    for _ in range(7):
        player.append(stock.pop(random.randint(0, len(stock)-1)))
    return player

def check_doubles(player_hand):
    doubles = [0]
    for i in player_hand:
        if i in DOUBLES:
            doubles = max([doubles, i])
    return doubles

def who_first(player1, player2):
    doubles1 = check_doubles(player1)
    doubles2 = check_doubles(player2)
    if doubles1 == doubles2:
        return True
    else:
        max_double = max(doubles1, doubles2)
    if max_double in player1:
        first_player = "player"
        player1.remove(max_double)
    else:
        first_player = "computer"
        player2.remove(max_double)
    return first_player, max_double

def info_print(stock, player1_hand, player2_hand, snake, status):
    print("======================================================================")
    print("Stock size:", len(stock))
    print("Computer pieces:", len(player1_hand), '\n')
    if len(snake) <= 6:
        for i in snake:
            print(i, sep='', end='')
    else:
        for i in range(3):
            print(snake[i], sep='', end='')
        print('...',  sep='', end='')
        for i in range(-3, 0, 1):
            print(snake[i], sep='', end='')
    print('\n')
    print("Your pieces:")
    for i in range(1, len(player2_hand)+1):
        print(i, ':', player2_hand[i-1], sep="")
    print()
    if status == "computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    elif status == "playerwon":
        print("Status: The game is over. You won!")
    elif status == "computerwon":
        print("Status: The game is over. The computer won!")
    elif status == "draw":
        print("Status: The game is over. It's a draw!")

def check_move(player, snake, status, count_nums):
    if status == "computer":
        move_dict = dict()
        for i in player:
            move_dict.update({(i[0], i[1]): count_nums[i[0]] + count_nums[i[1]]})
        move_list = [k for k, v in sorted(move_dict.items(), key=lambda x: x[1], reverse=True)]
        for i in move_list:
            if i[0] == snake[-1][1] or i[1] == snake[-1][1]:
                return player.index([i[0], i[1]]) + 1
            elif i[0] == snake[0][0] or i[1] == snake[0][0]:
                return -(player.index([i[0], i[1]]) + 1)
        move = 0
        return move
    while True:
        move = input()
        try:
            move = int(move)
        except ValueError:
            print("Invalid input. Please try again.")
        else:
            if move > len(player) or -(move) > len(player):
                if status == "computer":
                    continue
                print("Invalid input. Please try again.")
                continue
            else:
                if move > 0:
                    buffer_move = move
                    side = -1
                    last = 1
                elif move < 0:
                    buffer_move = -move
                    side = 0
                    last = 0
                else:
                    return move
                if player[buffer_move-1][0] == snake[side][last] or player[buffer_move-1][1] == snake[side][last]:
                    return move
                else:
                    print("Illegal move. Please try again.")
                    continue
                break

def make_move(player, snake, status, count_nums = 0):
    move = check_move(player, snake, status, count_nums)
    if move > 0:
        if player[move-1][1] == snake[-1][1]:
            player[move-1][0], player[move-1][1] = player[move-1][1], player[move-1][0]
        snake.append(player.pop(move-1))
    elif move < 0:
        if player[-(move+1)][0] == snake[0][0]:
            player[-(move+1)][0], player[-(move+1)][1] = player[-(move+1)][1], player[-(move+1)][0]
        snake.insert(0, player.pop(-(move+1)))
    elif move == 0:
        if len(stock) != 0:
            player.append(stock.pop(random.randint(0, len(stock)-1)))

def win_check(snake, player, computer):
    if len(player) == 0:
        return "playerwon"
    elif len(computer) == 0:
        return 'computerwon'
    else:
        count_nums = Counter(elem for sublist in snake for elem in sublist)
        for i in count_nums:
            if count_nums[i] == 8:
                return 'draw'
    return True

stock = STOCK
computer = []
player = []
shuffle_is_ok = True
while True:
    create_hand(stock, computer)
    create_hand(stock, player)
    start_info = who_first(computer, player)
    if start_info != True:
        break
snake = [start_info[1]]
status = start_info[0]
win = True
while win == True:
    if status == "player":
        info_print(stock, computer, player, snake, status)
        make_move(player, snake, status)
        status = "computer"
    elif status == "computer":
        info_print(stock, computer, player, snake, status)
        list_for_ai = snake + computer
        count_nums = Counter(elem for sublist in list_for_ai for elem in sublist)
        make_move(computer, snake, status, count_nums)
        status = "player"
        input()
    win = win_check(snake, player, computer)
else:
    status = win
    info_print(stock, computer, player, snake, status)




