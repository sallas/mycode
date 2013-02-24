import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    startState = False
    def getNextValues(self, state, inp):
        
        if state == False and not atObstacle(inp):
            return (state, io.Action(fvel = 0.30, rvel = 0.00))
        elif state == False:
            state = True
            return (state, io.Action(fvel = 0.00, rvel = 0.00))
        elif blocked(inp):
            return (state, io.Action(fvel = 0.00, rvel = 0.30))
        elif inp.sonars[7] > 0.5:
            return (state, io.Action(fvel = 0.10, rvel = -0.30))
        
        
            

        
        #if inp.sonars[3] < 0.5 or inp.sonars[4] < 0.5:
            #return (state, io.Action(fvel = -0.10, rvel = 0.10))
        return (state, io.Action(fvel = 0.30, rvel = 0.00))

mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def blocked(inp):
    if  inp.sonars[3] < 0.4 or inp.sonars[4] < 0.4:
        return True
    elif inp.sonars[2] < 0.4 or inp.sonars[5] < 0.4:
        return True
    return False
    

def atObstacle(inp):
    for reading in inp.sonars:
        if reading < 0.3:
            return True
    return False

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=True) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    #print '2: ', inp.sonars[2]
    #print '3: ', inp.sonars[3]
    #print '4: ', inp.sonars[4]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
