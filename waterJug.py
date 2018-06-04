class State:
    def __init__(self, initJug1, initJug2):
        self.jug1 = initJug1
        self.jug2 = initJug2

    def getJug1(self):
        return self.jug1

    def getJug2(self):
        return self.jug2

    def filljug1(self):
        self.jug1 = 4

    def filljug2(self):
        self.jug2 = 3

    def emptyjug1(self):
        self.jug1 = 0

    def emptyjug2(self):
        self.jug2 = 0

    def pourjug1jug2(self):
        if self.jug1 + self.jug2 <= 3:
            self.jug2 = self.jug1 + self.jug2
            self.jug1 = 0
        else:
            self.jug1 = self.jug1 + self.jug2 - 3
            self.jug2 = 3

    def pourjug2jug1(self):
        if self.jug1 + self.jug2 <= 4:
            self.jug1 = self.jug1 + self.jug2
            self.jug2 = 0
        else:
            self.jug2 = self.jug1 + self.jug2 - 4
            self.jug1 = 4

    def __eq__(self):
        if self.jug1 == self.jug2:
            return True, "Jug1 (%d) is equal to Jug2 (%d)" % (self.jug1, self.jug2)

    def __str__(self):
        return "State(%d,%d)" % (self.jug1, self.jug2)



w = State(0,0)


def run():

    print(w)
    w.getJug1()
    w.getJug2()

    if w.getJug1() == 4 or w.getJug1() == 1:
        w.emptyjug1()
        print(w)
    if w.getJug1() == 2 and w.getJug2() == 0:
        return
    else:

        if w.getJug2() == 2:
            if w.getJug1() == 4:
                w.emptyjug1()
                print(w)
                w.pourjug2jug1()
                print(w)
            else:
                w.pourjug2jug1()
                print(w)

        else:
            w.filljug2()
            print(w)
            w.getJug1()
            w.getJug2()

            w.pourjug2jug1()
            run()
run()