import os

class RPS:
	def __init__(self, user1, user2):
		self.choicesDict = {"rock": 1, "paper": 2, "scissors": 3}

		self.user1 = user1
		self.user2 = user2

		self.u1_ans = str(input("{} Pick rock, paper or scissors: ".format(self.user1))).lower()
		os.system("clear")
		self.u2_ans = str(input("{} Pick rock, paper or scissors: ".format(self.user2))).lower()

	def compare(self):	
		diff = self.choicesDict[self.u1_ans] - self.choicesDict[self.u2_ans]

		if diff % 3 == 2:
			return "{} wins".format(self.user2)

		elif diff % 3 == 1:
			return "{} wins".format(self.user1)

		return "It's a draw"

def main():
	user1 = str(input("What is your name Player1? : "))
	user2 = str(input("And what is your name Player2? : "))

	keepPlaying = True
	while keepPlaying == True:
		game = RPS(user1, user2)
		print(game.compare())
		playOn = str(input("Would you like to keep playing? (yes/no): "))
		if playOn == "yes":
			keepPlaying = True
		else:
			keepPlaying = False

	print("Hopefully you had fun, {} and {}!".format(user1, user2))

if __name__ == "__main__":
	main()