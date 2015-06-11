### Space Cadets: June 3, 2015
### An implementation of the server's board class

# Consider changing member functions of boards to function
# as static member functions.  See:
# https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
# (Only one board will ever exist - no need for multiple instances)

import random
import graphics as gr
import time

(N, E, S, W) = (0, 1, 2, 3)
(F, R, B, L) = (0, 1, 2, 3)
#=======================================================#
#dummy class to allow for creation of Ship objects
class Ship:
    def __init__(self, x, y, heading = W):
        self.x = x
        self.y = y
        self.heading = heading
        self.frontTube = 0
        self.backTube = 0
        self.damage = 0
        self.lockon = 0
        self.spaceJam = 0
        self.shields = {F: 0, R: 0, B: 0, L: 0}

    def stepForward(self):
        if self.heading == N:
            self.y -= 1
        if self.heading == S:
            self.y += 1
        if self.heading == W:
            self.x -= 1
        if self.heading == E:
            self.x += 1

    #returns the relative orientation for a given cardinal direction
    #for example, eastern shields of a south facing ship
    #would be (E - S) % 4 -> (1 - 2) % 4 -> -1 % 4 -> 3 (or it's left shields)
    def cardinalShields(self, direction):
        return (direction - self.heading) % 4

    #returns the strength of shields in a given cardinal direction
    #for example, eastern shields of a south facing ship
    #would be self.shields[self.cardinalShields]
    def cardinalStrength(self,direction):
        return self.shields[self.cardinalShields(direction)]

    def img(self):
        center = gr.Point(50*self.x+25,50*self.y+25)
        if self.heading == N:
            triangle = gr.Polygon([gr.Point(center.x,center.y-20),gr.Point(center.x-10,center.y+10),gr.Point(center.x+10,center.y+10)])
        if self.heading == E:
            triangle = gr.Polygon([gr.Point(center.x+20,center.y),gr.Point(center.x-10,center.y-10),gr.Point(center.x-10,center.y+10)])
        if self.heading == S:
            triangle = gr.Polygon([gr.Point(center.x,center.y+20),gr.Point(center.x-10,center.y-10),gr.Point(center.x+10,center.y-10)])
        if self.heading == W:
            triangle = gr.Polygon([gr.Point(center.x-20,center.y),gr.Point(center.x+10,center.y-10),gr.Point(center.x+10,center.y+10)])
        damage = {0: 'blue', 1: 'yellow', 2: 'red'}
        triangle.setFill(damage[self.damage])
        return triangle

    #this means that the ship accidentially fired some missles
    #without the enemy in their firing cone/correct firing cone
    #this function causes the ship to lose a front missle (if existant)
    #or a back missle (if existant).
    def loseAccidentalMissle(self, numMissles):
        for x in range(numMissles):
            if self.frontTube > 0:
                self.frontTube -= 1
            elif self.backTube > 0:
                self.backTube -= 1
#=======================================================#

# A board will only exist on the server machine
# It is responsible for board state logic such as 
# distances and firing cones
# It communicates with clients by recieving moves, fire commands, and
# tractor beam and mine commends.
# It sends out views of ships and boards.

#giving directions values so that we can do rotations without nested
#logical checks i.e. "u-turn" is simply add 2.

class ServerBoard:

    def __init__(self):
        self.height = 10
        self.width = 10
        self.crystals = set([(1,3),(2,6)]) #crystals begins as an empty set of locations
        self.mines = set([(2,2), (8,8)])

        self.ship1 = Ship(1, 5, N)
        self.ship2 = Ship(8, 5, N)
        self.win = gr.GraphWin("board", 500, 500)
        for x in range(10):
            l = gr.Line(gr.Point(50*x,0), gr.Point(50*x,500))
            l.draw(self.win)
        for y in range(10):
            l = gr.Line(gr.Point(0,50*y), gr.Point(500, 50*y))
            l.draw(self.win)
        self.drawnObjects = set()
        self.refreshView()


    def __repr__(self):
        pointsOfInterest = self.POIs()
        representation = ''
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) in pointsOfInterest:
                    representation += self.getSymbol(pointsOfInterest[(x,y)])
                else:
                    representation += '-'
            representation += '\n'
        return representation

    def getSymbol(self, obj):
        if isinstance(obj, Ship):
            return ['^', '>', 'v', '<'][obj.heading]
        else:
            return '?'

    def otherShip(self, ship):
        return self.ship1 if ship == self.ship2 else self.ship2

    #this methods creates a dictionary of all points of interest on the board
    #the keys are (x,y) tuples, and the values are refrences to the object of interest
    def POIs(self):
        d = {}
        d[(self.ship1.x, self.ship1.y)] = self.ship1
        d[(self.ship2.x, self.ship2.y)] = self.ship2
        for pos in self.crystals:
            d[pos] = 'c'
        for pos in self.mines:
            d[pos] = 'm'
        return d

    # changes the position of the ship on the board based
    # on the given moves
    # assumes moves will be given as a string of characters
    # 'f', 'l', 'r', 'u' for forward, left turn, right turn, u turn
    def executeMoveCommand(self, ship, moveString):
        print "Executing move sequence"
        for command in moveString:
            if command == 'f':
                if not self.onTheEdge(ship):
                    #we only move the ship if it won't fall off the edge
                    ship.stepForward()
                    #check for collision!!!!
                    #handle ship collision (decide how we want to)
                    #deduct health for mine collision, remove mine
                    #handle crystal collision (does anything happen?)
            else:
                self.rotate(ship, command)
            time.sleep(0.07)
            self.refreshView()
            ## later on, we will send the ship view to clients so
            ## that they see each step taken
        print "Move sequence complete"

    #assumes that numMissles will be checked outside this function
    #(that call will only made with numMissles == 2 if the firing ship
    # has 2 missles loaded *on the same side*)
    def executeFireCommand(self, ship, numMissles):
        if numMissles < (ship.frontTube + ship.backTube):
            print "Insufficient Missles"
            return
        print "Executing fire command"
        other = self.otherShip(ship)
        if self.canTarget(ship, other):
            arc = self.determineArc(ship, other)
            if (arc == 1) and (ship.frontTube < numMissles):
                print "Missles not in Front Tubes"
                ship.loseAccidentalMissle(numMissles)
            elif arc == 0 and ship.backTube < numMissles:
                print "Missles not in Back Tubes"
                ship.loseAccidentalMissle(numMissles)
            else: #enemy in firing arc and missle(s) in appropriate tube
                self.removeTorpedos(ship, numMissles, arc)
                if self.canHit(ship, other):
                    shieldSide = self.otherShieldSide(ship, other)
                    dam = self.calculateDamage(other, numMissles, shieldSide)
                    other.damage += dam
                    print "Ship takes", dam, "damage!"
                    other.shields[shieldSide] = 0
                    #tell other ship to lose power dice, if appropriate
                    #tell other ship to free its dice from "shieldSide"
                else:
                    print "Insufficient lockon."
                other.spaceJam = 0
                #tell other to free its jamming dice
        else:
            print "Enemy ship not in firing cone.",numMissles,"missles lost."
            ship.loseAccidentalMissle(numMissles) #they shot without the enemy in their firing arc
        ship.lockon = 0
        #tell ship to lose its lockon dice
        self.refreshView()

    # the following function determines whether or not ship2 is
    # in *either* firing cone of ship1
    # (each ship has a forward and backward firing arc)
    def canTarget(self, ship1, ship2):
        rowDiff = abs(ship1.y - ship2.y)
        colDiff = abs(ship1.x - ship2.x)
        if ship1.heading in [N, S]:
            if rowDiff >= colDiff:
                return True
        if ship1.heading in [E, W]:
            if rowDiff <= colDiff:
                return True
        return False

    #given that ship2 is in one of ship1's firing arcs, determines which
    #a return value of 1 means front arc, 0 means back arc
    def determineArc(self, ship1, ship2):
        if ship1.heading == N:
            return ship2.y < ship1.y
        if ship1.heading == S:
            return ship2.y > ship1.y
        if ship1.heading == E:
            return ship2.x > ship1.x
        if ship1.heading == W:
            return ship2.x < ship2.x

    #assumes ship2 is in ship1's firing cone, determines whether
    #ship1 has sufficient lockon to hit ship2 (encountering shields)
    def canHit(self, ship1, ship2):
        rowDiff = abs(ship1.y - ship2.y)
        colDiff = abs(ship1.x - ship2.x)
        if rowDiff + colDiff + ship2.spaceJam < ship1.lockon:
            return True
        else:
            return False

    def otherShieldSide(self, ship, other):
        if abs(ship.y - other.y) > abs(ship.x - other.x):
            if ship.y < other.y:
                #North side of other
                return other.cardinalShields(N)
            if ship.y > other.y:
                #South side of other
                return other.cardinalShields(S)
        if abs(ship.y - other.y) < abs(ship.x - other.x):
            if ship.x < other.x:
                #West side of other
                return other.cardinalShields(W)
            if ship.x > other.x:
                #East side of other
                return other.cardinalShields(E)
        #tiebreaking positive diagonal
        if (ship.y - other.y) == (ship.x - other.x):
            if ship.y < other.y:
                #tiebreak between other's North and East shields
                if other.cardinalStrength(N) > other.cardinalStrength(E):
                    return other.cardinalShields(N)
                else:
                    return other.cardinalShields(E)
            if ship.y > other.y:
                #tiebreak between other's South and West shields
                if other.cardinalStrength(S) > other.cardinalStrength(W):
                    return other.cardinalShields(S)
                else:
                    return other.cardinalShields(W)
        #tiebreaking negative diagonal
        if (ship.y - other.y) == (other.x - ship.x):
            if ship.x < other.x:
                #tiebreak between other's North and West shields
                if other.cardinalStrength(N) > other.cardinalStrength(W):
                    return other.cardinalShields(N)
                else:
                    return other.cardinalShields(W)
            if ship.x > other.x:
                #tiebreak between other's South and East shields
                if other.cardinalStrength(S) > other.cardinalStrength(E):
                    return other.cardinalShields(S)
                else:
                    return other.cardinalShields(E)

    def calculateDamage(self, ship, numMissles, shieldSide):
        shieldStrength = ship.shields[shieldSide]
        damage = 0
        for missle in range(numMissles):
            if random.choice([0,0,0,1,1,2]) >= shieldStrength:
                damage += 1
        return damage

    #returns true if a ship is on a border square and facing the
    #edge of the board
    def onTheEdge(self, ship):
        if (ship.x == 0) and (ship.heading == N):
            return True
        if (ship.x == self.height - 1) and (ship.heading == S):
            return True
        if (ship.y == 0) and (ship.heading == W):
            return True
        if (ship.y == self.width - 1) and (ship.heading == E):
            return True
        return False

    def rotate(self, ship, move):
        # a left turn is negative, a right turn is positive
        moves = {'l': -1, 'r': 1, 'u': 2}
        ship.heading = (ship.heading + moves[move]) % 4

    def removeTorpedos(self, ship, numMissles, arc):
        if arc:
            ship.frontTube -= numMissles
        else:
            ship.backTube -= numMissles
        assert(ship.frontTube >= 0)
        assert(ship.backTube >= 0)

    def refreshView(self):
        for x in self.drawnObjects:
            x.undraw()
        pois = self.POIs()
        for point in pois.keys():
            obj = pois[point]
            if isinstance(obj, Ship):
                img = obj.img()
                img.draw(self.win)
                self.drawnObjects.add(img)
            if obj in ['m', 'c']:
                center = gr.Point(50*point[0]+25,50*point[1]+25)
                circ = gr.Circle(center, 20)
                if obj == 'm':
                    circ.setFill('red')
                if obj == 'c':
                    circ.setFill('CadetBlue4')
                circ.draw(self.win)
                self.drawnObjects.add(circ)


#==============================================================#
### main ###

b = ServerBoard()
time.sleep(.5)
b.executeMoveCommand(b.ship1, 'frff')

END = raw_input("\n")
