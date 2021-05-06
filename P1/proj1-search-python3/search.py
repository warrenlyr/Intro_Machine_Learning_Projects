# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    #Initial
    visited = []
    path = util.Stack()
    curr_path = []
    arr = util.Stack()
    root = problem.getStartState()
    arr.push(root)

    if(problem.isGoalState(root)):
        #Best case maybe?
        return

    '''
    DFS
    Use stack because we are LIFO here for Depth first
    Push the node that is valid move into stack
    Pop the one is not visited one by one until find the path or all nodes are visited
    '''
    while(not arr.isEmpty()):
        
        #Find the node that is not visited yet
        while True:
            node = arr.pop()
            #Find the path related to this node (from the begining to this node)
            if(node is not root):
                curr_path = path.pop()
            if(node not in visited):
                break
            #print("Now pop: ", node)
        
        #End case: if the goal is found
        if(problem.isGoalState(node)):
            break
        
        #Mark this node as visited
        visited.append(node)
        #print("Now visited list: ", visited)

        #Find current node's successors
        successor = problem.getSuccessors(node)
        for state, dir, cost in successor:
            #If it's not visited and a valid move, push to stack array and path stack array
            if(state not in visited and problem.getCostOfActions(curr_path + [dir]) != 999999):
                arr.push(state)
                path.push(curr_path + [dir])
        #print("Now path: ", curr_path)

        #Clean the successor
        successor = []

    return curr_path
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #init
    visited = []
    arr = util.Queue()
    path = util.Queue()
    curr_path = []
    root = problem.getStartState()
    arr.push(root)
    
    if(problem.isGoalState(root)):
        #Best case maybe?
        return
    #print(root)
    '''
    BFS
    Exactly same as DFS
    Except use queue instead of stack, because we are FIFO here
        get all the children of parent first
    '''
    while(not arr.isEmpty()):

        while(True):
            node = arr.pop()
            if(node is not root):
                curr_path = path.pop()
            if(node not in visited):
                break
        #print("Now node is:", node)
        #print("Is it end: ", problem.isGoalState(node))
        if(problem.isGoalState(node)):
            break
                
        visited.append(node)

        successor = problem.getSuccessors(node)
        for state, dir, cost in successor:
            if(state not in visited and problem.getCostOfActions(curr_path + [dir]) != 999999):
                arr.push(state)
                path.push(curr_path + [dir])
        successor = []
            
        
    return curr_path

    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    '''
    UCS
    Use priority queue here, because we are insert the children by it's cost
    Others are the same
    '''
    #init
    visited = []
    arr = util.PriorityQueue()
    path = util.PriorityQueue()
    curr_path = []
    root = problem.getStartState()
    arr.push((root, 0), 0)

    #print("Now root is: ", root)

    if(problem.isGoalState(root)):
        #Best case maybe?
        return

    #
    while(not arr.isEmpty()):

        while(True):
            node = arr.pop()
            #print("Node now is: ", node[0], "and", node[1])
            if(node[0] is not root):
                curr_path = path.pop()
            if(node[0] not in visited):
                break
        
        #print("I am here 111")
        if(problem.isGoalState(node[0])):
            break

        #print("I am here 222")
        visited.append(node[0])

        #print("I am here 333")
        successor = problem.getSuccessors(node[0])
        for state, dir, cost in successor:
            #Should be != 999999 not < 999999
            if(state not in visited and problem.getCostOfActions(curr_path + [dir]) != 999999):
                #print("pushed node: ", node[0], " with cost: ", node[1])
                arr.push((state, node[1] + cost), node[1] + cost)
                path.push(curr_path + [dir], node[1] + cost)
        
        successor = []

    return curr_path



    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    '''
    A* Search
    Same as the UCS
    But use sum(h + g) as the priority to distinguish which node to select
    '''
    #init
    visited = []
    arr = util.PriorityQueue()
    path = util.PriorityQueue()
    curr_path = []
    root = problem.getStartState()
    arr.push((root, 0, heuristic(root, problem)), 0)

    if(problem.isGoalState(root)):
        #Best case maybe?
        return

    #
    while(not arr.isEmpty()):

        while(True):
            node = arr.pop()
            if(node[0] is not root):
                curr_path = path.pop()
            if(node[0] not in visited):
                break
        
        if(problem.isGoalState(node[0])):
            break

        visited.append(node[0])

        successor = problem.getSuccessors(node[0])
        
        for state, dir, cost in successor:
            if(state not in visited and problem.getCostOfActions(curr_path + [dir]) != 999999):
                arr.push((state, node[1] + cost, heuristic(state, problem)), node[1] + cost + heuristic(state, problem))
                '''
                print("Expend: ", state, " , ", node[1] + cost + heuristic(state, problem))
                print("     the cost is: ", cost)
                '''
                #print("     the heru is: ", heuristic(state, problem))
                #print("     privious cost is: ", node[1])
                
                path.push(curr_path + [dir], node[1] + cost + heuristic(state, problem))
        
        successor = []

    return curr_path

    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
