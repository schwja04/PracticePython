class OrderedLinkedList:
    class Node:
        def __init__(self, item, next=None):
            self.item = item
            self.next = next

    def __init__(self):
        self.head = None

    # recursive helper function
    # add item to its proper place in the list and return the list
    # with the item added.
    def __add(node, item):
        # base case
        if node == None:
            return OrderedLinkedList.Node(item)

        # Recursive Cases
        if item <= node.item:
            return OrderedLinkedList.Node(item, node)

        # item must be greater than node.item
        node.next = OrderedLinkedList.__add(node.next, item)

        return node

    # add to the list in the order specified by the
    # items.
    def add(self, item):

        self.head = OrderedLinkedList.__add(self.head, item)

    # remove and return the first item in the list
    def remove(self):
        if self.head == None:
            raise Exception("Attempt to remove from empty OrderedLinkedList.")
        item = self.head.item
        self.head = self.head.next
        return item

    def __iter__(self):
        if self.head == None:
            return iter([])

        current = self.head

        while current != None:
            yield current.item
            current = current.next

    def __str__(self):
        s = "OrderedLinkedList("
        for i in self:
            s = s + str(i) + ','
        s = s[:-1]

        s += ')'

        return s

def main():
    ll = OrderedLinkedList()

    ll.add(6)
    ll.add(8)
    ll.add(10)
    ll.add(5)
    ll.add(7)
    ll.add(5.5)

    print(ll)

main()