import os

class Pay:
	def __init__(self, hourly=float(input("What is your hourly rate? ")), overtimeHours=float(input("How many hours of overtime are you working per week on average? "))):
		self.hourlyRate = hourly
		self.overtimeHours = overtimeHours
		self.overtimeRate = round(self.hourlyRate * 1.5, 2)

	def calcWeek(self):
		if self.hourlyRate == None:
			raise Exception("Failed to enter hourly rate.")
		return round(self.hourlyRate * 40 + self.overtimeRate * self.overtimeHours, 2)

	def calcMonth(self):
		return round(self.calcWeek() * 4.3, 2)

def pay(x):
	hr = x
	overtime = (1.5 * hr)
	week = hr * 40 + (overtime * 10)
	aweek = .7 * week
	year = 52 * week
	ayear = .7 * year
	month = year / 12
	amonth = .7 * month

	return "Hourly pay = {0} \nOvertime pay = {1} \nWeekly pay = {2} (With 10 hours of overtime) \nAfter taxes = {3} \nMonthly pay = {4} \nAfter taxes = {5} \nYearly pay = {6} \nAfter taxes = {7}".format(hr,overtime,week,aweek,month,amonth,year,ayear)

# def main():
# 	os.system("clear")
# 	rate = float(input("What is the hourly rate? \n"))
# 	os.system("clear")
# 	print(pay(rate))

def main():
	os.system("clear")
	pay = Pay()
	print("Your hourly pay is {} \
		\nYour overtime pay is {} \
		\nYour weekly pay is {} \
		\nYour monthly pay is {}".format(pay.hourlyRate, pay.overtimeRate, pay.calcWeek(), pay.calcMonth()))

if __name__ == '__main__':
	main()