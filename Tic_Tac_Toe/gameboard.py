class GameBoard:
	def __init__(self, size):
		self.size = size
		self.drawBoard()

	def acrossLines(self):
		string1 = ""
		for x in range(self.size):
			string1 += " ---"
		print(string1)

		# string1 = " --- " * self.size
		# print(string1)

	def downLines(self):
		string2 = ""
		for x in range(self.size + 1):
			string2 += "|   "
		print(string2)

		# string2 = " --- " * (self.size + 1)
		# print(string2)

	def drawBoard(self):
		for x in range(self.size):
			self.acrossLines()
			self.downLines()
		self.acrossLines()

def main():
	userInput = int(input("What size grid would you like drawn? "))
	g = GameBoard(userInput)

if __name__ == "__main__":
	main()