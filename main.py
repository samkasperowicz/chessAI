import chess
import random
import chess.svg


board = chess.Board()

def findEval(board):
    whiteEval = 0
    blackEval = 0
    whitePawns = board.pieces(1, True)
    blackPawns = board.pieces(1, False)
    whiteKnights = board.pieces(2, True)
    blackKnights = board.pieces(2, False)
    whiteBishops = board.pieces(3, True)
    blackBishops = board.pieces(3, False)
    whiteRooks = board.pieces(4, True)
    blackRooks = board.pieces(4, False)
    whiteQueens = board.pieces(5, True)
    blackQueens = board.pieces(5, False)
    whiteKings = board.pieces(6, True)
    blackKings = board.pieces(6, False)
    whiteEval = len(whitePawns) + len(whiteKnights) * 3 + len(whiteBishops) * 3 + len(whiteRooks) * 5 + len(whiteQueens) * 9 + len(whiteKings) * 99
    blackEval = len(blackPawns) + len(blackKnights) * 3 + len(blackBishops) * 3 + len(blackRooks) * 5 + len(blackQueens) * 9 + len(blackKings) * 99
    eval = whiteEval - blackEval
    return eval

# Randomly selects move with best valuation.
def best_move(board, depth):
	best_moves = []
	high = -999
	for i in board.legal_moves:
		board.push(i)
		move_value = min(board, depth) + findEval(board)
		if (move_value == high):
			best_moves.append(i)
		elif (move_value > high):
			best_moves.clear()
			best_moves.append(i)
			high = move_value
		board.pop()
	board.push(random.choice(best_moves))

# Find min in tree.
def min(board,depth):
	low = 999
	for i in board.legal_moves:
		board.push(i)
		if (depth != 0):
			move_value = findEval(board) + max(board,depth - 1)
		else:
			board.pop()		
			return 0
		if (move_value < low):
			low = move_value		
		board.pop()
	return low

# Find max in tree.
def max(board,depth):
	high = -999
	for i in board.legal_moves:
		board.push(i)
		if (depth != 0):
			move_value = findEval(board) + min(board,depth - 1)
		else:
			board.pop()		
			return 0		
		if (move_value > high):
			high = move_value		
		board.pop()
	return high

# Main loop
print("Choose a depth for AI")
depth = int(input())
while (depth < 1):
	print("Invalid depth. Enter a depth >= 1")
	depth = int(input())
while (board.is_game_over() == False):	
	while(1):
		try: 
			print("Enter a move: ")
			move = input()
			board.push_san(move)			
			break			
		except:
			if (move == "q"):
				exit(1)
			print("Invalid Move!")
	print("------USER-----")
	print(board)		
	best_move(board, depth)
	print("------AI-------")
	print(board)
	print("Current Eval:", findEval(board))
	