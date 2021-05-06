# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        '''
        print("successorGameState: ", successorGameState)
        print("newPos: ", newPos)
        print("newFood:", newFood)
        print("newGhostStates: ", newGhostStates)
        print("newScaredTimes: ", newScaredTimes)
        '''

        '''
        worst case： return negative inf (touch a gost | action is stop)
        otherwise: return 
        ''' 
        
        #
        import math
        foods = currentGameState.getFood().asList()
        #print("foods: ", foods)
        
        
        #First check if action is stop (corner case)
        if(action == 'Stop'):
            return (-math.inf)
        #Next, check if:
        #               1. if gost scared time is 0
        #               2. if gost is at the same position as pacman
        for gost in newGhostStates:
            #print("gost position: ", gost.getPosition())
            if((gost.scaredTimer == 0) and (gost.getPosition() == newPos)):
                return (-math.inf)

        #Else
        #Consider the distance of pacman's position to a food's position
        # - the distance of this food's position to gost's position (if the gost is not scared, if scared, dismiss)
        # the score = [the distance of pacman's position to this food's position * -1] + [the distance of this food's position to gost's position]
        # the further the food to the gost, the better
        dis = []
        for food in foods:
            foodDis = manhattanDistance(food, list(newPos)) * -1
            gostDis = 0
            for gost in newGhostStates:
                if(gost.scaredTimer == 0): 
                    gostDis += manhattanDistance(list(gost.getPosition()), food)
            dis.append(foodDis + gostDis)
        
        #print("max dis: ", max(dis))
        return max(dis)
        #return successorGameState.getScore()
        
        
def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        '''
        self.depth
        self.evaluationFunction
        '''

        depth = self.depth
        action = gameState.getLegalActions(0)

        if(len(action) > 0):
            val = max((self._minmaxAgent(gameState.generateSuccessor(0, act), depth, 1), act) for act in action)
            return val[1]
        else:
            return self.evaluationFunction(gameState)


        '''
        #util.raiseNotDefined()
        import math

        def minmaxAction(gameState, depth, agent):
            #Get all agents
            agents = gameState.getNumAgents()
            if(agent >= agents):
                depth -= 1
                agent = 0
            
            #if game is finished or is the leaf, return the score
            if(gameState.isWin() or gameState.isLose() or depth == 0):
                return self.evaluationFunction(gameState)
            #if it is pacman agent, call max agent
        '''
    
    def _minmaxAgent(self, gameState, depth, index):
        #game is finished
        if(depth == 0 or gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)
        
        #if it is pacman, find max
        if(index == 0):
            #if legal actions exist
            action = gameState.getLegalActions(index)
            if(len(action) > 0):
                return max(self._minmaxAgent(gameState.generateSuccessor(0, act), depth, 1) for act in action)
            #no action exist
            else:
                return self.evaluationFunction(gameState)
        #if it is gost, find min
        else:
            action = gameState.getLegalActions(index)
            #find the next agent
            next = (index + 1) % gameState.getNumAgents()
            if(next == 0):
                depth -= 1
            if(len(action) > 0):
                return min(self._minmaxAgent(gameState.generateSuccessor(index, act), depth, next) for act in action)
            else:
                return self.evaluationFunction(gameState)




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #
        import math
        maxVal = -math.inf
        a = -math.inf
        b = math.inf
        fin = None
        #get pacman's actions
        for act in gameState.getLegalActions(0):
            #
            val = self._abjianzhi(gameState.generateSuccessor(0, act), self.depth, 1, a, b)
            if val > maxVal:
                maxVal = val
                fin = act
            a = max(a, maxVal)
        
        return fin
            
    
    def _abjianzhi(self, gameState, depth, index, a, b):
        #
        import math

        if(depth == 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        #pacman, find the max
        elif(index == 0):
            #
            maxVal = - math.inf
            #get legal action
            action = gameState.getLegalActions(index)
            
            for act in action:
                val = self._abjianzhi(gameState.generateSuccessor(0, act), depth, 1, a, b)
                if(val > maxVal):
                    maxVal = val
                if(maxVal > b):
                    #Early rturn
                    return maxVal
                a = max(a, maxVal)
            return maxVal
        
        #gost, find the min
        else:
            next = (index + 1) % gameState.getNumAgents()
            #if the next is pacman agent
            if(next == 0):
                depth -= 1
            
            #
            minVal = math.inf
            #get legal action
            action = gameState.getLegalActions(index)

            for act in action:
                minVal = min(minVal, self._abjianzhi(gameState.generateSuccessor(index, act), depth, next, a, b))
                #Early return
                if(minVal < a):
                    return minVal
                b = min(b, minVal)
            return minVal
        



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def _expecctiMax(self, gameState, depth, index):
        #if game is finished:
        if(depth == 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        #if it is the pacman
        if(index == 0):
            #get legal action
            action = gameState.getLegalActions(index)
            #important: return max
            return max(self._expecctiMax(gameState.generateSuccessor(0, act), depth, 1) for act in action)
        
        #if it is the gost
        else:
            #get legal action
            action = gameState.getLegalActions(index)
            #check if next is the pacman
            next = (index + 1) % gameState.getNumAgents()
            if(next == 0):
                depth -= 1
            val = sum(self._expecctiMax(gameState.generateSuccessor(index, act), depth, next) for act in action)
            #not important: return the avrg
            return val / len(action)


    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #
        import math
        fin = None
        maxVal = -math.inf

        for act in gameState.getLegalActions(0):
            val = self._expecctiMax(gameState.generateSuccessor(0, act), self.depth, 1)
            if(val > maxVal):
                maxVal = val
                fin = act
        
        return fin



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
                *   
                calculate the current position to the food distance first
                then, if the gost is scared
                the closer to the gost, the better
                if the gost is not scared
                the more far away to the gost, the better
                *
                so,
                if the gost is scared, larger the score for the distance from food to gost
                if the gost is not scared, smaller the score for the distance from food to gost
                *
                the total score is the current score + MIN scored food

    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
    #get the position & all foods position
    position = list(currentGameState.getPacmanPosition())
    food = currentGameState.getFood().asList()
    gost = currentGameState.getGhostStates()

    '''
    foodList = []
    
    for f in food:
        fDis = manhattanDistance(f, position) * -1
        gDis = 0
        for g in gost:
            if(g.scaredTimer == 0):
                gDis += manhattanDistance(g.getPosition(), f)
        foodList.append(fDis + gDis)
    
    return max(foodList)
    '''
    
    foodList = []
    gostList = []
    
    for f in food:
        fDis = manhattanDistance(f, position) * -1
        #foodList.append(manhattanDistance(f, position))
        gDis = 0
        for g in gost:
            if(g.scaredTimer == 0):
                gDis -= manhattanDistance(g.getPosition(), f)
            else:
                gDis += manhattanDistance(g.getPosition(), f)
        foodList.append(fDis + gDis)
    
    if(foodList):
        return currentGameState.getScore() + min(foodList)
    
    return currentGameState.getScore()




# Abbreviation
better = betterEvaluationFunction
