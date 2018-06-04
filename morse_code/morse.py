# Morse Code Encoder and Decoder
# Jacob Schwartz
# CS 160

class BinaryTree:
    # Node and Reference Binary Tree
    def __init__(self,rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self,newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
            return self.leftChild
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t
            return self.leftChild

    def insertRight(self,newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
            return self.rightChild
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t
            return self.rightChild

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self,obj):
        self.key = obj

    def getRootVal(self):
        return self.key

    def __str__(self):
        #To insure each root has the correct children
        return str(self.getRootVal()) + " has a (left child of " + str(self.getLeftChild()) + " and right child of " + str(self.getRightChild()) + ")"

class Morse:
    def __init__(self, root):
        self.root = open(root)
        self.morseList = []
        for line in self.root:
            line = line.strip().split()
            self.morseList.append(line)
        self.makeTree()

    def encode(self, message):
        encodedMessage = ""
        for ch in message:
            self._encode(ch, self.tree)
            encodedMessage = encodedMessage + " " + self.found

        return encodedMessage

    def _encode(self, letter, current, charstr=""):
        if current:
            if current.getRootVal() == letter:
                self.found = charstr
            else:
                self._encode(letter, current.getLeftChild(), charstr+".")
                self._encode(letter, current.getRightChild(), charstr+"-")

    def decode(self, message):
        stringList = message.split()
        hiddenMessage = ""
        for ch in stringList:
            hiddenMessage = hiddenMessage + self._decode(ch, self.tree)
        return hiddenMessage

    def _decode(self, str, current):
        if len(str) == 0:
            return current.getRootVal()
        else:
            if str[0] == ".":
                current = current.getLeftChild()
                return self._decode(str[1:], current)
            if str[0] == "-":
                current = current.getRightChild()
                return self._decode(str[1:], current)

    def makeTree(self):
        self.tree = BinaryTree("")
        for letter in self.morseList:
            current = self.tree
            for i in letter[1]:
                if i == ".":
                    if current.getLeftChild() == None:
                        current = current.insertLeft("")
                    else:
                        current = current.getLeftChild()
                if i == "-":
                    if current.getRightChild() == None:
                        current = current.insertRight("")
                    else:
                        current = current.getRightChild()
            current.setRootVal(letter[0])

if __name__ == '__main__':
    m = Morse('morse.dat')

    for ch in m.morseList:
         print(m.encode(ch[0]), ch[1], m.decode(ch[1]), ch[0])