import time
import copy

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop(-1)

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def reverse(self):
        self.items.reverse()

    def clone(self, stack):
        return copy.deepcopy(stack)

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self,thing):
        self.items.append(thing)

    def dequeue(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.size() == 0



def letterSpool(current, usedSet, workingSet, myStack, myQueue):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    #Locks the others positions and searches words in
    #Set to find words that are one letter off from current
    for letter_pos in range(len(current)):
        for letter in alphabet:
            #replaces letter in letter_pos to the letter variable
            mod = current[:letter_pos] + letter + current[(letter_pos + 1):]
            if mod in workingSet:
                workingSet.remove(mod)
                usedSet.add(mod)

    for word in usedSet:
        a = myStack.clone(myStack)
        a.push(word)
        myQueue.enqueue(a)

    usedSet.clear()

def main():
    threeSet = set()
    fourSet = set()
    fiveSet = set()
    usedSet = set()
    myStack = Stack()
    myQueue = Queue()

    f = open("words.txt", "r")
    for word in f:
        if len(word) == 4:
            threeSet.add(word[0:-1])
        if len(word) == 5:
            fourSet.add(word[0:-1])
        if len(word) == 6:
            fiveSet.add(word[0:-1])

    start = str(input("What is your starting word?  "))
    end = str(input("What is your end word?  "))

    start_time = time.time()
    current = start

    if len(start) != len(end):
        raise ValueError("Starting word and ending word must be the same length.")

    if len(start) == 3:
        workingSet = threeSet
    if len(start) == 4:
        workingSet = fourSet
    if len(start) == 5:
        workingSet = fiveSet

    if start not in workingSet:
        raise ValueError("Starting word not in word file")
    if end not in workingSet:
        raise ValueError("Ending word not in word file")


    workingSet.remove(start)
    myStack.push(start)

    finish_line = True
    letterSpool(current, usedSet, workingSet, myStack, myQueue)
    while myQueue.size() != 0:
        if current == end:
            myQueue.items = []
            myStack.reverse()
            count = 0
            for items in range(myStack.size()):
                count += 1
                print(myStack.pop())

            finish_line = False
            myQueue.size()
        else:
            b = myQueue.dequeue()
            myStack = myStack.clone(b)
            current = b.pop()
            letterSpool(current, usedSet, workingSet, myStack, myQueue)
            myQueue.size()

    ##end was reached without finding a path
    if finish_line == True:
        print("Path does not exist")
        end_time = time.time()
        print(end_time - start_time)
    else:
        print("The shortest path is %d word(s) long" % (count))
        end_time = time.time()
        print(end_time - start_time)
        main()

main()
