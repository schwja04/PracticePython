from collections import Counter
from heapq import heapify, heappop, heappush
from binaryTree import BinaryTree


def doOneBook(title):
    with open(title) as book:
        c = Counter(book.read())

    return c

allBooks = Counter()
for book in ['Alice.txt', 'HuckFinn.txt', 'TheAwakening.txt', 'TheStrangeCase.txt']:
    allBooks.update(doOneBook(book))

print(allBooks)

class QueueableBinaryTree(BinaryTree):

    def __init__(self, priority, value):
        super().__init__(priority)
        self.value = value

    def __lt__(self, other):
        if self.key < other.key:
            return True
        return False

treequeue = [QueueableBinaryTree(x[1], x[0]) for x in allBooks.items()]
heapify(treequeue)

def buildHuffmanCode(pq):
    while len(pq) > 1:
        a = heappop(pq)
        b = heappop(pq)
        newkey = a.key + b.key
        t = QueueableBinaryTree(newkey, 'internal')
        t.insertLeft(a)
        t.insertRight(b)
        heappush(pq, t)
    return heappop(pq)

root = buildHuffmanCode(treequeue)

huffmanTable = {}

def makeTable(tree, p):
    if tree:
        if tree.value != 'internal':
            huffmanTable[tree.value] = p
        else:
            makeTable(tree.leftChild, p + "1")
            makeTable(tree.rightChild, p + "0")

makeTable(root, "")

for k,v in sorted(huffmanTable.items(), key=lambda x: len(x[1])):
    print(k.replace('\n','\\n').replace('\t','\\t'),v)

res=""
with open('Alice.txt', 'r') as f:
    for ch in f.read():
        res += huffmanTable[ch]

print(res[:100])
print(len(res))
print(len(res)//8)

