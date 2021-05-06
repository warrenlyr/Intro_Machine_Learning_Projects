# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        #in each iter, find max if action exist
        for iter in range(self.iterations):
            #init
            disc = {}
            state = self.mdp.getStates()

            for s in state:
                #get actions
                actions = self.mdp.getPossibleActions(s)
                #store the max
                maxVal = 0

                #if actions exist
                if(actions):
                    thisList = []
                    #append the value, and use the max
                    for act in actions:
                        thisList.append(self.computeQValueFromValues(s, act))
                    maxVal = max(thisList)
                disc[s] = maxVal
            
            #update the max
            for s in state:
                self.values[s] = disc[s]




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        #val += probilities * (nextReward + nextStatesVal * discout)
        val = 0

        #get the next state & the probility
        for s, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            val += prob * (self.mdp.getReward(state, action, s) + self.getValue(s) * self.discount)
            #print("In compute Q val, nextState, probility, qVal: ", s, prob, val)
        
        #print("In compute Q val final: ", val)
        return val

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        import random
        '''
        x = "welcom"
        print(random.choice(x))
        '''

        #get actions
        actions = self.mdp.getPossibleActions(state)

        ### if no action exist ###
        if(not actions):
            return None
        
        ### if actions exist ###
        #compute Q val and get the max 
        thisList = []
        for act in actions:
            thisList.append(self.computeQValueFromValues(state, act))
        maxVal = max(thisList)

        #get the indexs of the max val
        indexList = []
        for i in range(len(thisList)):
            if(thisList[i] == maxVal):
                indexList.append(i)
        #random choice from indexs if several max values are equal
        #print(indexList)
        action = actions[random.choice(indexList)]

        return action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        state = self.mdp.getStates()
        stateLen = len(state)

        for i in range(self.iterations):
            #cycle
            thisState = state[i % stateLen]

            #if it's leagal state
            if(not self.mdp.isTerminal(thisState)):
                thisList = []
                for act in self.mdp.getPossibleActions(thisState):
                    thisList.append(self.computeQValueFromValues(thisState, act))
            
                self.values[thisState] = max(thisList)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        #init
        pre_dec = {}
        thisQueue = util.PriorityQueue()

        for state in self.mdp.getStates():
            maxVal = float('-inf')
            for act in self.mdp.getPossibleActions(state):
                for theNext, prob in self.mdp.getTransitionStatesAndProbs(state, act):
                    #if the predecessor's next not exist, add one
                    if(not pre_dec.get(theNext)):
                        pre_dec[theNext] = set()
                    if(prob > 0):
                        pre_dec[theNext].add(state)
                val = self.computeQValueFromValues(state, act)
                if(val > maxVal):
                    maxVal = val
            
            if(not self.mdp.isTerminal(state)):
                diff = abs(maxVal)
                thisQueue.push(state, -diff)


        for i in range(self.iterations):
            #
            if(thisQueue.isEmpty()):
                break
            
            #else
            thisState = thisQueue.pop()

            if(not self.mdp.isTerminal(thisState)):
                maxVal = 0
                thisList = []
                for act in self.mdp.getPossibleActions(thisState):
                    thisList.append(self.computeQValueFromValues(thisState, act))
                maxVal = max(thisList)
                #update the max
                self.values[thisState] = maxVal

                for pre in pre_dec[thisState]:
                    if(not self.mdp.isTerminal(pre)):
                        thisList = []
                        maxVal = 0
                        for act in self.mdp.getPossibleActions(pre):
                            thisList.append(self.computeQValueFromValues(pre, act))
                        maxVal = max(thisList)
                    
                    diff = abs(self.values[pre] - maxVal)
                    if(diff > self.theta):
                        thisQueue.update(pre, -diff)

