import datetime

def ageCalc():
	name = str(input("What is your name? \n"))
	age = int(input("How old are you? \n"))
	birthday = str(input("What is your birthday? \nEx: MM/DD \n")).split("/")

	hundredthBday = hundredthBirthday(age, birthday)

	return "Hey {}, Did you know you will turn one hundred in {}".format(name, hundredthBday)

def hundredthBirthday(age, bday):
	currentYear = datetime.date.today().year
	today = datetime.date.today()
	thisBday = datetime.date(int(currentYear), int(bday[0]), int(bday[1]))
	
	# if your birthday has occured today or before in the current year adding (100 - age) to the current year will be your hundredth birthday year
	if today >= thisBday:
		return currentYear + 100 - age
	
	# if your birthday has not occured yet today, adding (99 - age) will be your hundredth birthday year
	return currentYear + 99 - age

def main():
	print(ageCalc())

if __name__ == "__main__":
	main()
