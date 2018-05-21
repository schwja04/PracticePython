import os

class numFacts:
	def __init__(self):
		self.num = int(input("Provide a whole number that you would like information on: "))
		self.check = int(input("Provide a whole number you want to know if it evenly goes into the previous number: "))
		self.even = self.oddOrEven()
		self.four = self.div4()
		self.divsibleByX = self.divX()

	def oddOrEven(self):
		if self.num % 2 == 0:
			return True
		return False

	def div4(self):
		if self.num % 4 == 0:
			return True
		return False

	def divX(self):
		if self.num % self.check == 0:
			return True
		return False

def main():
	os.system("clear")
	n = numFacts()

	print("Number: {}".format(n.num))
	print("Check: {}".format(n.check))
	print("The number ({}) is even: {}".format(n.num, n.even))
	print("The number ({}) divdes evenly by 4: {}".format(n.num, n.four))
	print("The number ({}) divide evenly by your {}: {}".format(n.num, n.check, n.divsibleByX))

if __name__ == "__main__":
	main()