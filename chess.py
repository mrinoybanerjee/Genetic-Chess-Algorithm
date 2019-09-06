import numpy as np
import random
from datetime import datetime
random.seed(datetime.now())

BOARD_SIZE = 8

POSITIONS = [{
	"king": [[0, 4]],
	"queen": [[0, 3]],
	"rook": [[0, 0], [0, 7]],
	"bishop": [[0, 2], [0, 5]],
	"knight": [[0, 1], [0, 6]],
	"pawn": [[1, i] for i in range(BOARD_SIZE)],
},
{
	"king": [[7, 3]],
	"queen": [[7, 4]],
	"rook": [[7, 0], [7, 7]],
	"bishop": [[7, 2], [7, 5]],
	"knight": [[7, 1], [7, 6]],
	"pawn": [[6, i] for i in range(BOARD_SIZE)],
}]

MAPS = {
	"king": [
		[-3, -4, -4, -5, -5, -4, -4, -3],
		[-3, -4, -4, -5, -5, -4, -4, -3],
		[-3, -4, -4, -5, -5, -4, -4, -3],
		[-3, -4, -4, -5, -5, -4, -4, -3],
		[-2, -3, -3, -4, -4, -3, -3, -2],
		[-1, -2, -2, -3, -3, -2, -2, -1],
		[2, 2, 0, 0, 0, 0, 2, 2],
		[2, 3, 1, 0, 0, 1, 3, 2]
	], "queen": [
		[-2, -1, -1, -.5, -.5, -1, -1, -2],
		[-1, 0, 0, 0, 0, 0, 0, -1],
		[-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
		[-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
		[0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
		[-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
		[-1, 0, 0.5, 0, 0, 0, 0, -1],
		[-2, -1, -1, -.5, -.5, -1, -1, -2]
	], "rook": [
		[0, 0, 0, 0, 0, 0, 0, 0],
		[.5, 1, 1, 1, 1, 1, 1, .5],
		[-.5, 0, 0, 0, 0, 0, 0, -.5],
		[-.5, 0, 0, 0, 0, 0, 0, -.5],
		[-.5, 0, 0, 0, 0, 0, 0, -.5],
		[-.5, 0, 0, 0, 0, 0, 0, -.5],
		[-.5, 0, 0, 0, 0, 0, 0, -.5],
		[0, 0, 0, 0.5, 0.5, 0, 0, 0]
	], "bishop": [
		[-2, -1, -1, -1, -1, -1, -1, -2],
		[-1, 0, 0, 0, 0, 0, 0, -1],
		[-1, 0, 0.5, 1, 1, 0.5, 0, -1],
		[-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
		[-1, 0, 1, 1, 1, 1, 0, -1],
		[-1, 1, 1, 1, 1, 1, 1, -1],
		[-1, 0.5, 0, 0, 0, 0, 0.5, -1],
		[-2, -1, -1, -1, -1, -1, -1, -2]
	], "knight": [
		[-5, -4, -3, -3, -3, -3, -4, -5],
		[-4, -2, 0, 0, 0, 0, -2, -4],
		[-3, 0, 1, 1.5, 1.5, 1, 0, -3],
		[-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
		[-3, 0, 1.5, 2, 2, 1.5, 0, -3],
		[-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
		[-4, -2, 0, 0.5, 0.5, 0, -2, -4],
		[-5, -4, -3, -3, -3, -3, -4, -5]
	], "pawn": [
		[0, 0, 0, 0, 0, 0, 0, 0],
		[5, 5, 5, 5, 5, 5, 5, 5],
		[1, 1, 2, 3, 3, 2, 1, 1],
		[0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
		[0, 0, 0, 2, 2, 0, 0, 0],
		[0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
		[0.5, 1, 1, -2, -2, 1, 1, 0.5],
		[0, 0, 0, 0, 0, 0, 0, 0]
	]
}

WEIGHTS = {
	"pawn": 10,
	"knight": 30,
	"bishop": 30,
	"rook": 50,
	"queen": 90,
	"king": 900
}

class Piece:
	def __init__(self, value, type_, diag, hv, moveset, x, y, player, map_):
		self.value = value
		self.type_ = type_
		self.diag = diag
		self.hv = hv
		self.moveset = moveset
		self.x = x
		self.y = y
		self.testX = x
		self.testY = y
		self.alive = True
		self.testAlive = True
		self.player = player
		self.map = map_
		self.rawMap = map_

		if player == 0:
			if type_ == "king":
				self.icon = "♚"
			elif type_ == "queen":
				self.icon = "♛"
			elif type_ == "rook":
				self.icon = "♜"
			elif type_ == "bishop":
				self.icon = "♝"
			elif type_ == "knight":
				self.icon = "♞"
			else:
				self.icon = "♟"
		else:
			if type_ == "king":
				self.icon = "♔"
			elif type_ == "queen":
				self.icon = "♕"
			elif type_ == "rook":
				self.icon = "♖"
			elif type_ == "bishop":
				self.icon = "♗"
			elif type_ == "knight":
				self.icon = "♘"
			else:
				self.icon = "♙"

	def getMoves(self, board):
		moves = set([])
		killMoves = set([])
		if self.diag:
			for i in range(1, BOARD_SIZE):
				if self.testY + i < BOARD_SIZE and self.testX + i < BOARD_SIZE:
					tempPiece = board[self.testY + i][self.testX + i]
					if tempPiece == False:
						moves.add((self.testX + i, self.testY + i))
					elif tempPiece.player != self.player:
						killMoves.add((self.testX + i, self.testY + i))
						break
					else:
						break
				else:
					break
			for i in range(1, BOARD_SIZE):
				if self.testY + i < BOARD_SIZE and self.testX - i >= 0:
					tempPiece = board[self.testY + i][self.testX - i]
					if tempPiece == False:
						moves.add((self.testX - i, self.testY + i))
					elif tempPiece.player != self.player:
						killMoves.add((self.testX - i, self.testY + i))
						break
					else:
						break
				else:
					break
			for i in range(1, BOARD_SIZE):
				if self.testY - i >= 0 and self.testX + i < BOARD_SIZE:
					tempPiece = board[self.testY - i][self.testX + i]
					if tempPiece == False:
						moves.add((self.testX + i, self.testY - i))
					elif tempPiece.player != self.player:
						killMoves.add((self.testX + i, self.testY - i))
						break
					else:
						break
				else:
					break
			for i in range(1, BOARD_SIZE):
				if self.testY - i >= 0 and self.testX - i >= 0:
					tempPiece = board[self.testY - i][self.testX - i]
					if tempPiece == False:
						moves.add((self.testX - i, self.testY - i))
					elif tempPiece.player != self.player:
						killMoves.add((self.testX - i, self.testY - i))
						break
					else:
						break
				else:
					break
		if self.hv:
			for i in range(1, BOARD_SIZE):
				if self.testY + i < BOARD_SIZE:
					tempPiece = board[self.testY + i][self.testX]
					if tempPiece == False:
						moves.add((self.testX, self.testY + i))
					elif tempPiece.player != self.player:
						killMoves.add((self.testX, self.testY + i))
						break
					else:
						break
				else:
					break
			for i in range(1, BOARD_SIZE):
				if self.testY - i >= 0:
					tempPiece = board[self.testY - i][self.testX]
					if tempPiece == False:
						moves.add((self.testX, self.testY - i))
					elif tempPiece.player != self.player:
						killMoves.add((self.testX, self.testY - i))
						break
					else:
						break
				else:
					break
			for i in range(1, BOARD_SIZE):
				if self.testX + i < BOARD_SIZE:
					tempPiece = board[self.testY][self.testX + i]
					if tempPiece == False:
						moves.add((self.testX + i, self.testY))
					elif tempPiece.player != self.player:
						killMoves.add((self.testX + i, self.testY))
						break
					else:
						break
				else:
					break
			for i in range(1, BOARD_SIZE):
				if self.testX - i >= 0:
					tempPiece = board[self.testY][self.testX - i]
					if tempPiece == False:
						moves.add((self.testX - i, self.testY))
					elif tempPiece.player != self.player:
						killMoves.add((self.testX - i, self.testY))
						break
					else:
						break
				else:
					break
		if len(self.moveset) > 0:
			for move in self.moveset:
				if 0 <= self.testX + move[0] < BOARD_SIZE and 0 <= self.testY + move[1] < BOARD_SIZE:
					if self.type_ == "pawn":
						tempPiece = board[self.testY + move[1]][self.testX + move[0]]
						tempPiece1 = False
						if self.testX + 1 < BOARD_SIZE:
							tempPiece1 = board[self.testY + move[1]][self.testX + 1]
						tempPiece2 = False
						if self.testX - 1 >= 0:
							tempPiece2 = board[self.testY + move[1]][self.testX - 1]
						if tempPiece == False:
							moves.add((self.testX + move[0], self.testY + move[1]))
						if tempPiece1 and tempPiece1.player != self.player:
							killMoves.add((self.testX + 1, self.testY + move[1]))
						if tempPiece2 and tempPiece2.player != self.player:
							killMoves.add((self.testX - 1, self.testY + move[1]))
					else:
						tempPiece = board[self.testY + move[1]][self.testX + move[0]]
						if tempPiece == False:
							moves.add((self.testX + move[0], self.testY + move[1]))
						elif tempPiece.player != self.player:
							killMoves.add((self.testX + move[0], self.testY + move[1]))

		return [moves, killMoves]

class King(Piece):
	def __init__(self, value, x, y, player, map_):
		Piece.__init__(self, value, "king", False, False, [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]], x, y, player, map_)

class Queen(Piece):
	def __init__(self, value, x, y, player, map_):
		Piece.__init__(self, value, "queen", True, True, [], x, y, player, map_)

class Rook(Piece):
	def __init__(self, value, x, y, player, map_):
		Piece.__init__(self, value, "rook", False, True, [], x, y, player, map_)

class Bishop(Piece):
	def __init__(self, value, x, y, player, map_):
		Piece.__init__(self, value, "bishop", True, False, [], x, y, player, map_)

class Knight(Piece):
	def __init__(self, value, x, y, player, map_):
		Piece.__init__(self, value, "knight", False, False, [[-2, -1], [-1, -2], [1, -2], [2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1]], x, y, player, map_)

class Pawn(Piece):
	def __init__(self, value, x, y, player, map_):
		Piece.__init__(self, value, "pawn", False, False, [[0, 1 * (-1 * player)]], x, y, player, map_)

class Player():
	def __init__(self, board, side, pawnVal = 10, knightVal = 30, bishopVal = 30, rookVal = 50, queenVal = 90, kingVal = 900, maps = MAPS):
		self.board = board
		self.side = side
		self.pieces = []
		self.maps = MAPS
		self.weights = {
			"pawn": pawnVal,
			"knight": knightVal,
			"bishop": bishopVal,
			"rook": rookVal,
			"queen": queenVal,
			"king": kingVal
		}

		for piece in POSITIONS[side].keys():
			if piece == "king":
				for i in range(len(POSITIONS[side][piece])):
					self.pieces.append(King(kingVal, POSITIONS[side][piece][i][1], POSITIONS[side][piece][i][0], side, maps[piece]))
			elif piece == "queen":
				for i in range(len(POSITIONS[side][piece])):
					self.pieces.append(Queen(queenVal, POSITIONS[side][piece][i][1], POSITIONS[side][piece][i][0], side, maps[piece]))
			elif piece == "rook":
				for i in range(len(POSITIONS[side][piece])):
					self.pieces.append(Rook(rookVal, POSITIONS[side][piece][i][1], POSITIONS[side][piece][i][0], side, maps[piece]))
			elif piece == "bishop":
				for i in range(len(POSITIONS[side][piece])):
					self.pieces.append(Bishop(bishopVal, POSITIONS[side][piece][i][1], POSITIONS[side][piece][i][0], side, maps[piece]))
			elif piece == "knight":
				for i in range(len(POSITIONS[side][piece])):
					self.pieces.append(Knight(knightVal, POSITIONS[side][piece][i][1], POSITIONS[side][piece][i][0], side, maps[piece]))
			elif piece == "pawn":
				for i in range(len(POSITIONS[side][piece])):
					self.pieces.append(Pawn(pawnVal, POSITIONS[side][piece][i][1], POSITIONS[side][piece][i][0], side, maps[piece]))
			else:
				print("ERROR: " + piece)

	def evaluateBoard(self):
		score = 0
		otherPieces = []
		if self.side == 0:
			otherPieces = self.board.p2.pieces
		else:
			otherPieces = self.board.p1.pieces

		for piece in self.pieces:
			score += piece.value + piece.map[piece.y][piece.x]
		for piece in otherPieces:
			score -= piece.value + piece.map[piece.y][piece.x]

		return score

	def generateBoard(self):
		board = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
		otherPieces = []
		if self.side == 0:
			otherPieces = self.board.p2.pieces
		else:
			otherPieces = self.board.p1.pieces

		for piece in self.pieces:
			if piece.testAlive:
				board[piece.testY][piece.testX] = piece
		for piece in otherPieces:
			if piece.testAlive:
				board[piece.testY][piece.testX] = piece
		return board

	def move(self):
		otherPieces = None
		if self.side == 0:
			otherPieces = self.board.p2.pieces
		else:
			otherPieces = self.board.p1.pieces
		baseVal = self.evaluateBoard()
		maxVal = -100000
		maxMove = (0, 0)
		maxPiece = None
		maxKill = None
		for piece in self.pieces:
			if piece.testAlive:
				board = self.generateBoard()
				moves = piece.getMoves(board)
				newScore = baseVal - piece.map[piece.y][piece.x]
				for killMove in moves[1]:
					killPiece = board[killMove[1]][killMove[0]]
					newScore1 = newScore + killPiece.value + killPiece.map[killMove[1]][killMove[0]] + piece.map[killMove[1]][killMove[0]]
					killPiece.testAlive = False
					piece.testX = killMove[0]
					piece.testY = killMove[1]
					minVal = 100000
					for otherPiece in otherPieces:
						if otherPiece.testAlive:
							board1 = self.generateBoard()
							moves1 = otherPiece.getMoves(board1)
							newScore2 = newScore1 + otherPiece.map[otherPiece.y][otherPiece.x]
							for killMove1 in moves1[1]:
								killPiece1 = board1[killMove1[1]][killMove1[0]]
								newScore3 = newScore2 - killPiece1.value - killPiece1.map[killMove1[1]][killMove1[0]] - otherPiece.map[killMove1[1]][killMove1[0]]
								minVal = min(newScore3, minVal)
							for move1 in moves1[0]:
								newScore3 = newScore2 - otherPiece.map[move1[1]][move1[0]]
								minVal = min(newScore3, minVal)
					piece.testX = piece.x
					piece.testY = piece.y
					killPiece.testAlive = True
					if minVal > maxVal:
						maxVal = minVal
						maxMove = killMove
						maxPiece = piece
						maxKill = killPiece
				for move in moves[0]:
					newScore1 = newScore + piece.map[move[1]][move[0]]
					piece.testX = move[0]
					piece.testY = move[1]
					minVal = 100000
					for otherPiece in otherPieces:
						if otherPiece.testAlive:
							board1 = self.generateBoard()
							moves1 = otherPiece.getMoves(board1)
							newScore2 = newScore1 + otherPiece.map[otherPiece.y][otherPiece.x]
							for killMove1 in moves1[1]:
								killPiece1 = board1[killMove1[1]][killMove1[0]]
								newScore3 = newScore2 - killPiece1.value - killPiece1.map[killMove1[1]][killMove1[0]] - otherPiece.map[killMove1[1]][killMove1[0]]
								minVal = min(newScore3, minVal)
							for move1 in moves1[0]:
								newScore3 = newScore2 - otherPiece.map[move1[1]][move1[0]]
								minVal = min(newScore3, minVal)
					piece.testX = piece.x
					piece.testY = piece.y
					if minVal > maxVal:
						maxVal = minVal
						maxMove = move
						maxPiece = piece
						maxKill = None
		if maxKill is not None:
			maxKill.testAlive = False
			maxKill.alive = False
			if maxKill.player == self.side:
				for p in range(len(self.pieces)):
					if self.pieces[p] is maxKill:
						del self.pieces[p]
						break
			else:
				for p in range(len(otherPieces)):
					if otherPieces[p] is maxKill:
						del otherPieces[p]
						break
		maxPiece.map[maxPiece.y][maxPiece.x] -= 3
		maxPiece.x = maxMove[0]
		maxPiece.y = maxMove[1]
		maxPiece.testX = maxMove[0]
		maxPiece.testY = maxMove[1]


class Board:
	def __init__(self, w1 = WEIGHTS, w2 = WEIGHTS, m1 = MAPS, m2 = MAPS, printMoves = True):
		self.printMoves = printMoves
		self.board = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
		self.p1 = Player(self, 0, pawnVal = w1["pawn"], knightVal = w1["knight"], bishopVal = w1["bishop"], rookVal = w1["rook"], queenVal = w1["queen"], kingVal = w1["king"], maps = m1)
		self.p2 = Player(self, 1, pawnVal = w2["pawn"], knightVal = w2["knight"], bishopVal = w2["bishop"], rookVal = w2["rook"], queenVal = w2["queen"], kingVal = w2["king"], maps = m2)

	def updateBoard(self):
		self.board = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
		for piece in self.p1.pieces:
			self.board[piece.y][piece.x] = piece
		for piece in self.p2.pieces:
			self.board[piece.y][piece.x] = piece

	def printBoard(self):
		for row in self.board:
			printStr = ""
			for piece in row:
				if piece == False:
					printStr += "  | "
				else:
					printStr += piece.icon + " | "
			print(printStr[:-3])

	def getWinner(self):
		moveCount = 0
		while moveCount < 1000:
			moveCount += 1
			hasKing = False
			for piece in self.p1.pieces:
				if piece.type_ == "king":
					hasKing = True
					break
			if hasKing:
				self.p1.move()
				self.updateBoard()
			else:
				if self.printMoves:
					print("Moves: " + str(moveCount))
				return self.p2
			hasKing = False
			for piece in self.p2.pieces:
				if piece.type_ == "king":
					hasKing = True
					break
			if hasKing:
				self.p2.move()
				self.updateBoard()
			else:
				if self.printMoves:
					print("Moves: " + str(moveCount))
				return self.p1
		if self.printMoves:
			print("Moves: " + str(moveCount))
		return self.p2

class World:
	def __init__(self, genSize):
		self.size = genSize
		self.generations = {}
		self.genCount = 0

	def generateFirst(self):
		childWeights = {}
		childMaps = {}
		for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
			childWeights[piece] = WEIGHTS[piece] * np.random.normal(1, 0.1)
			childMaps[piece] = [[MAPS[piece][i][j] * np.random.normal(1, 0.1) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
		return [childWeights, childMaps]

	def reproduce(self, i):
		p1 = self.generations[self.genCount - 1][i]
		p2 = self.generations[self.genCount - 1][i]
		childWeights = {}
		childMaps = {}
		for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
			childWeights[piece] = ((p1.weights[piece] + p2.weights[piece]) / 2) * np.random.normal(1, 0.1)
			childMaps[piece] = [[((p1.maps[piece][i][j] + p2.maps[piece][i][j]) / 2) * np.random.normal(1, 0.1) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
		return [childWeights, childMaps]

	def runGeneration(self):
		self.generations[self.genCount] = []
		for i in range(self.size):
			c1 = None
			c2 = None
			if self.genCount == 0:
				c1 = self.generateFirst()
				c2 = self.generateFirst()
			else:
				c1 = self.reproduce(i)
				c2 = [self.generations[self.genCount - 1][i].weights, self.generations[self.genCount - 1][i].maps]
			self.generations[self.genCount].append(Board(w1 = c1[0], w2 = c2[0], m1 = c1[1], m2 = c2[1]).getWinner())
		self.genCount += 1

	def compareGenerations(self, g1, g2):
		wins = 0
		for i in range(self.size):
			c1 = [self.generations[g1][i].weights, self.generations[g1][i].maps]
			c2 = [self.generations[g2][i].weights, self.generations[g2][i].maps]
			board = Board(w1 = c1[0], w2 = c2[0], m1 = c1[1], m2 = c2[1], printMoves = False)
			if board.getWinner() is board.p2:
				wins += 1
		return [wins, self.size, wins / self.size]

	def runGenerations(self, count):
		for i in range(count):
			self.runGeneration()
			if i > 0:
				print(self.compareGenerations(0, i))
			if i > 1:
				del self.generations[i - 1]

world = World(5)
world.runGenerations(20)






















		