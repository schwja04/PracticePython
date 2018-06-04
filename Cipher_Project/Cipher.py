upperletters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
lowerletters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def encrypt(string, num):
    encrypted_str = ""
    for char in string:
        if char in upperletters:
            encrypted_str += upperletters[(upperletters.index(char) + num)%26]
        elif char in lowerletters:
            encrypted_str += lowerletters[(lowerletters.index(char) + num)%26]
        else:
            encrypted_str += char
    return encrypted_str


def main():
    cypher_output = open('ciphertext_out.txt', 'w')
    shift = int(input('By what integer would you like to shift the message? \n'))
    with open('plaintext_in.txt', 'r+') as f:
        line = f.readline()
        while line != "":
            a = encrypt(line, shift)
            print(a)
            cypher_output.write(a)
            line = f.readline()
        f.seek(0)
        f.truncate()
        f.close()
        cypher_output.close()

    plaintext_out = open('plaintext_out.txt', 'w')
    shift = int(input('By what integer would you like to shift the message? \n'))
    with open('ciphertext_in.txt', 'r') as f:
        line = f.readline()
        while line != "":
            a = encrypt(line, shift)
            print(a)
            plaintext_out.write(a)
            line = f.readline()
        f.close()
        plaintext_out.close()

main()