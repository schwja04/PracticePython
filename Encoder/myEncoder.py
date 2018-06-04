from collections import Counter

def stripChar(title):
	with open(title) as book:
		c = book.read().lower()
		lst = ["'m", "'re", "'ve", "'s", "'ll", "'d", "n't"]

		for aps in lst:
			c.replace(aps, "")

		for char in c:
			if (ord(char) > 122 or ord(char) < 97) and ord(char) != 32 and ord(char) != 10:
				c = c.replace(char, "")
	return c


def main():
	#a = stripChar('Alice.txt')
	print(a)

main()