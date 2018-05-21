def ageCalc():
	name = str(input("What is your name? \n"))
	age = int(input("How old are you? \n"))
	birthday = str(input("What is your birthday? \n Ex: MM/DD \n"))

	print("{} {} {}".format(name, age, birthday))

def main():
	ageCalc()

if __name__ == "__main__":
	main()
