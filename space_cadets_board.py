### Space Cadets: June 3, 2015
### An implementation of the server's board class

# Consider changing member functions of boards to function
# as static member functions.  See:
# https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
# (Only one board will ever exist - no need for multiple instances)

(N, E, S, W) = (0, 1, 2, 3)
#=======================================================#
#dummy class to allow for creation of Ship objects
class Ship:
    def __init__(self, x, y, heading = N):
        self.x = x
        self.y = y
        self.heading = heading
        self.damage = 0
        self.lockon = 0
        self.spaceJam = 0

    def stepForward(self):
        if self.heading == N:
            self.y -= 1
        if self.heading == S:
            self.y += 1
        if self.heading == W:
            self.x -= 1
        if self.heading == E:
            self.x += 1

    def getView(self):
        ShipView(ship)

class ShipView():
    def __init__(self, ship):
        self.x = ship.x
        self.y = ship.y
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
    height = 10
    width = 10
    #self.crystals = set() #crystals begins as an empty set of locations

    ship1 = Ship(1, 5)
    ship2 = Ship(8, 5)

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

    #this methods creates a dictionary of all points of interest on the board
    #the keys are (x,y) tuples, and the values are refrences to the object of interest
    def POIs(self):
        d = {}
        d[(self.ship1.x, self.ship1.y)] = self.ship1
        d[(self.ship2.x, self.ship2.y)] = self.ship2
        #for pos in setOfCrystalPositions:
        #    d[pos] = 'c'
        #for pos in setOfMinePositions:
        #    d[pos] = 'm'
        return d

    # changes the position of the ship on the board based
    # on the given moves
    # assumes moves will be given as a string of characters
    # 'f', 'l', 'r', 'u' for forward, left turn, right turn, u turn
    def executeMoveCommand(self, ship, moveString):
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
            ## later on, we will send the ship view to clients so
            ## that they see each step taken

    # the following function determines whether or not ship2 is
    # in *either* firing cone of ship1
    # (each ship has a forward and backward firing arc)
    def canTarget(self, ship1, ship2):
        rowDiff = abs(ship1.y - ship2.y)
        colDiff = abs(ship1.x - ship2.x)
        if ship1.heading in [N, S]:
            if rowDiff < colDiff:
                return True
        if ship1.heading in [E, W]:
            if rowDiff > colDiff:
                return True
        return False

    def canLock(self, ship1, ship2):
        rowDiff = abs(ship1.y - ship2.y)
        colDiff = abs(ship1.x - ship2.x)
        if rowDiff + colDiff + ship2.spaceJam < ship1.lockon:
            return True
        else:
            return False

    #returns true if a ship is on a border square and facing the
    #edge of the board
    def onTheEdge(self, ship):
        if (ship.x == 0) and (ship.pos == N):
            return True
        if (ship.x == ServerBoard.height - 1) and (ship.pos == S):
            return True
        if (ship.y == 0) and (ship.pos == W):
            return True
        if (ship.y == ServerBoard.width - 1) and (ship.pos == E):
            return True
        return False

    def rotate(self, ship, move):
        # a left turn is negative, a right turn is positive
        moves = {'l': -1, 'r': 1, 'u': 2}
        ship.heading = (ship.heading + moves[move]) % 4


#==============================================================#
### main ###

b = ServerBoard()
print b

