import chess
import random
from collections import defaultdict

# Tree data structure for holding all possible moves at certain depth (done)
class Tree:
    def __init__(self, board, moveList, parent):
        self.children = []
        self.board = board
        self.moveList = moveList
        self.parent = parent

# Function that finds current board evaluation given board (done)
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

# Create the move tree at depth 2 given board
def createMoveTree(board):
    root = Tree(board, [], None)
    legalMoves = list(board.legal_moves)
    for i in range(len(legalMoves)):
        boardChild = board.copy()
        boardChildMoveList = root.moveList[:]
        boardChildMoveList.append(str(legalMoves[i]))
        boardChild.push_san(str(legalMoves[i]))
        root.children.append(Tree(boardChild, boardChildMoveList, root))
    for i in range(len(root.children)):
        legalMovesC = list(root.children[i].board.legal_moves)
        currChild = root.children[i]
        for j in range(len(legalMovesC)):
            boardChild = currChild.board.copy()
            boardChildMoveList = currChild.moveList[:]
            boardChildMoveList.append(str(legalMovesC[j]))
            boardChild.push_san(str(legalMovesC[j]))
            currChild.children.append(Tree(boardChild, boardChildMoveList, currChild))
    return root

# Find the best move given tree
# To do: Implement minimax for tree of depth 2
def findBest(boardTree):
    bestEval = 1000
    equalMoveIndexes = []
    for i in range(len(boardTree.children)):
        currEval = findEval(boardTree.children[i].board)
        if currEval == bestEval:
            bestEval = currEval
            equalMoveIndexes.append(i)
        if currEval < bestEval:
            bestEval = currEval
            equalMoveIndexes = [i]
    chosenMoveIndex = equalMoveIndexes[random.randint(0, len(equalMoveIndexes) - 1)]
    bestMove = boardTree.children[chosenMoveIndex].moveList[0]
    return bestMove

# Code to be run (main)
# To do: End of game detection
board = chess.Board()
while True:
    print(board)
    userMove = input("\nEnter a move: ")
    print("\n")
    userMoveCheck = chess.Move.from_uci(userMove)
    while userMoveCheck not in board.legal_moves:
        userMove = input("Invalid, enter a new move: ")
        userMoveCheck = chess.Move.from_uci(userMove)
    board.push_san(userMove)
    print(board)
    print("\nNext Turn\n")
    boardTree = createMoveTree(board)
    compMove = findBest(boardTree)
    board.push_san(compMove)