# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes
class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = width * height
        self.cleantiles = 0
        self.dict = {}
        for i in range(width):
            for d in range(height):
                self.dict[i,d] = 1
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        
        y= pos.getY()
        x= pos.getX()
        if self.isTileCleaned(int(x), int(y)) == False:
            self.cleantiles += 1
        self.dict[(int(x), int(y))] = 0
        

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.dict[(m, n)] == 0
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.tiles

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return self.cleantiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        random_width = random.randint(0,self.width -1)
        random_height = random.randint(0,self.height -1)
        return Position(random_width, random_height)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if pos.getY() < self.height and pos.getY() >= 0:
            if pos.getX() < self.width and pos.getX() >= 0:
                return True
            
        return False


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        assert speed > 0
        self.pos = room.getRandomPosition()
        self.rec = room
        self.dir = random.randint(0,359)
        self.speed = speed
        room.cleanTileAtPosition(self.pos)
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        width = position.getX()
        heigth = postition.getY()
        self.pos = Position(width, heigth)

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.pos = self.pos.getNewPosition(self.dir, self.speed)
        self.rec.cleanTileAtPosition(self.pos)


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        isin = False
        while isin == False:
            if self.rec.isPositionInRoom(self.pos.getNewPosition(self.dir, self.speed)):
                self.pos = self.pos.getNewPosition(self.dir, self.speed)
                isin = True
            else:
                self.setRobotDirection(random.randint(0,359))
        self.rec.cleanTileAtPosition(self.pos)
            

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    
    
    totalsteps = 0
    trials = num_trials
    while trials > 0:
        step = 0
        rec = RectangularRoom(width, height)
        robo_list = list()
        for i in range(num_robots):
            robo_list.append(robot_type(rec, speed))
        anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        while min_coverage*100 > ((100.0 * rec.getNumCleanedTiles()) / (width * height)):
            for robo in robo_list:
                robo.updatePositionAndClean()
            step += 1
            anim.update(rec, robo_list)
        totalsteps += step
        trials -= 1
    anim.done()
    return totalsteps / float(num_trials)
        


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    avg_list = list()
    for i in range(0,10):
        avg = runSimulation(i+1, 1.0, 20, 20, 0.8, 40, StandardRobot)
        avg_list.append(avg)

    pylab.plot([1,2,3,4,5,6,7,8,9,10],avg_list)
    
    pylab.title('80% cleared, 1-10 robots.')
    pylab.xlabel('Number of robots')
    pylab.ylabel('Mean time')

    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    avg_list = list()
    ratio_list = [[20,20], [25,16], [40,10], [50,8], [80,5], [100,4]]
    for i in range(6):
        avg = runSimulation(2, 1.0, ratio_list[i][0], ratio_list[i][1], 0.8, 100, StandardRobot)
        avg_list.append(avg)
        print avg
    
    pylab.xlim(0,6)
    pylab.plot([1,2,3,4,5,6],avg_list)
    pylab.title('80% cleared, 2 robots, diffrent w/h')
    pylab.xlabel('width to heigth ratio')
    pylab.ylabel('Mean time')

    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        isin = False
        while isin == False:
            if self.rec.isPositionInRoom(self.pos.getNewPosition(self.dir, self.speed)):
                self.pos = self.pos.getNewPosition(self.dir, self.speed)
                isin = True
            else:
                self.setRobotDirection(random.randint(0,359))
        self.setRobotDirection(random.choice([90,180,270,0]))
        self.rec.cleanTileAtPosition(self.pos)


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    avg_list = list()
    for i in range(0,10):
        avg = runSimulation(i+1, 1.0, 20, 20, 0.8, 40, StandardRobot)
        avg_list.append(avg)

    pylab.plot([1,2,3,4,5,6,7,8,9,10],avg_list)
    
    avg_list = list()
    for i in range(0,10):
        avg = runSimulation(i+1, 1.0, 20, 20, 0.8, 40, RandomWalkRobot)
        avg_list.append(avg)
    
    pylab.plot([1,2,3,4,5,6,7,8,9,10],avg_list)
    pylab.title('80% cleared, 1-10 robots.')
    pylab.xlabel('Number of robots')
    pylab.ylabel('Mean time')

    pylab.show()
    
    
avg = runSimulation(1, 0.1, 5, 5, 1, 1, StandardRobot)
#runSimulation(2, 1.0, 10, 10, 0.8, 1, RandomWalkRobot)



    
#pos = Position(4,5)
#rec = RectangularRoom(10,10)
#robo = Robot(rec, 1.0)
