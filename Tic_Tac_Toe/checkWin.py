# STILL IN PROGRESS
class Outcome:
	def __init__(self, board):
		self.board = board
		self.players = {0 : "nobody", 1 : "player 1", 2 : "player 2"}

	def check(self):
		for i in [1, 2]:
			# if self.board[0] == [i, i, i] or self.board[1] == [i, i, i] or self.board[2] == [i, i, i]:
			# 	return self.players[i]
			for row in self.board:
				if row == [i] * 3:
					return self.players[i]

			for row in self.board:
				lst = []
				for col in self.board[row]:
					lst.append(self.board[row][col])
				if lst == [i] * 3:
					return self.players[i]

			for row in range(self.board):
				for col in self.board:

# WORKING THROUGH THE THOUGHT PROCESS OF DIFFERENT CASES WITH FOR LOOPS
# WILL BREAK INTO METHODS INSTEAD WHEN I HAVE FINISHED BUILDING CASES



def main():
	check = Outcome([[0,1,2],[0,1,2],[0,1,2]])
	check.check()

if __name__ == "__main__":
	main()