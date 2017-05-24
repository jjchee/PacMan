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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        return successorGameState.getScore()

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

    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2', w1 = 1, w2 = -20, w3 = -4, w4 = -1.5, w5 = -2, w6 = -2): # Default 'scoreEvaluationFunction'
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        
        # Set the weights to use for each feature in eval function (default manual weights)
        global _w1, _w2, _w3, _w4, _w5, _w6
        _w1 = float(w1)
        _w2 = float(w2)
        _w3 = float(w3)
        _w4 = float(w4)
        _w5 = float(w5)
        _w6 = float(w6)
        
        print 'Using weights:' + str([_w1, _w2, _w3, _w4, _w5, _w6])

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
        """
        "*** YOUR CODE HERE ***"
        # print "depth: " + str(self.depth)
        legalMoves = gameState.getLegalActions(0)
        bestMoves = []
        maxScore = float('-inf')
        for action in legalMoves:
            if action is not Directions.STOP:
                # nextState = gameState.generatePacmanSuccessor(action)
                score = self.getMinMoves(gameState.generateSuccessor(0, action), self.depth, 1)
                if score > maxScore:
                    maxScore = score
                    bestMoves = [action]
                elif score == maxScore:
                    bestMoves.append(action)

        if len(bestMoves) > 1:
            print 'Pick random ' + str(bestMoves) + " score " + str(maxScore)
        elif maxScore > 50000000.0:
            print 'Going to win: ' + str(maxScore)

        return random.choice(bestMoves)

    def getMaxMoves(self, gameState, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legalMoves = gameState.getLegalActions(0)
        maxScore = float('-inf')
        for action in legalMoves:
            if action is not Directions.STOP:
                # nextState = gameState.generatePacmanSuccessor(action)
                score = self.getMinMoves(gameState.generateSuccessor(0, action), depth, 1)
                if score > maxScore:
                    maxScore = score
        return maxScore

    def getMinMoves(self, gameState, depth, agentIndex):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        numGhosts = gameState.getNumAgents() - 1
        legalMoves = gameState.getLegalActions(agentIndex)
        minScore = float('inf')
        if agentIndex == numGhosts:
            for action in legalMoves:
                # nextState = gameState.generateSuccessor(agentIndex, action)
                score = self.getMaxMoves(gameState.generateSuccessor(agentIndex, action), depth - 1)
                if score < minScore:
                    minScore = score
        else:
            for action in legalMoves:
                # nextState = gameState.generateSuccessor(agentIndex, action)
                score = self.getMinMoves(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                if score < minScore:
                    minScore = score

        return minScore


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
        
_w1 =_w2 = _w3 = _w4 = _w5 = _w6 = 0. # The weights to use in the eval function  

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      
      Currently eval score depends on:
          - Current game score
          - Distance to closest food dot
          - Number of food dots left
          - Number of capsule dots remaining
          - Distance to closest active ghost
          - Distance to closest scared ghost
    """
    "*** YOUR CODE HERE ***"
    # Win = Very high score, Lose = Very low score
    if currentGameState.isWin():
        # prioritize walking straight into the win, so not all wins are equal
        return 100000000.0 + currentGameState.getScore()
    elif currentGameState.isLose():
        return float('-inf')
    
    player_position = currentGameState.getPacmanPosition()  # Get the position of the Pacman
    
    def get_manhattan_distances(positions): # Get the manhattan distances from the player for a list of objects
        distances = []
        for p in positions:
            distances.append(util.manhattanDistance(player_position, p.getPosition()))
            
        return distances
    
    # The current game score
    current_score = currentGameState.getScore()
    
    # Get the number of remaining large dots (capsules)
    # The fewer capsules on the board, the higher the score
    num_capsules = len(currentGameState.getCapsules())
    
    # Get the number of remaining small dots (food)
    foods = currentGameState.getFood().asList()
    num_food = len(foods)
    
    # Get the distance to the closest food dot
    dist_closest_food = min(map(lambda p: util.manhattanDistance(player_position, p), foods))
    
    # Get the distance to the nearest scared/active ghost
    ghost_states = currentGameState.getGhostStates()
    scared_ghosts, active_ghosts = [], []
    
    for g in ghost_states: # Divide ghosts into scared and not scared
        if g.scaredTimer:
            scared_ghosts.append(g) # If ghost's scared timer is not (i.e. greater than) 0 add to scared group
        else:
            active_ghosts.append(g) # Else ghost is active add to not scared group         

    dist_closest_active_ghost = dist_closest_scared_ghost = float('-inf')

    if active_ghosts: # If active ghosts is not empty, find dist to closest
        dist_closest_active_ghost = min(get_manhattan_distances(active_ghosts))
    else:
        dist_closest_active_ghost = float('inf')

    # If closest ghost distance is >= 5 it will have the same effect on eval score (adjust this?)
    dist_closest_active_ghost = max(dist_closest_active_ghost, 5)
    
    if scared_ghosts: # If scared ghosts not empty, find dist to closest
        dist_closest_scared_ghost = min(get_manhattan_distances(scared_ghosts))
    else:
        dist_closest_scared_ghost = 0 # If there are no scared ghosts it has no effect on score
    
    # Uses a linear combination of weighted features to determine evaluate score
    
    #evaluation_score = 1 * current_score + -20 * num_capsules + -4 * num_food + -1.5 * dist_closest_food + -2 * (float(1) / dist_closest_active_ghost) + -2 * dist_closest_scared_ghost # Manual evaluation score

    # Multiply each feature by the weight determined using gradient descent (defaults to manual weights)
    evaluation_score = _w1 * current_score + _w2 * num_capsules + _w3 * num_food + _w4 * dist_closest_food + _w5 * (float(1) / dist_closest_active_ghost) + _w6 * dist_closest_scared_ghost
    
    # Note: Weights should be changed to variables so we can modify them with the learning function
    
    return evaluation_score
    
# Abbreviation
better = betterEvaluationFunction

