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
from memory_profiler import profile
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

visitedStates = set()
expanded = util.Stack()
dfsGoalVisited = set()
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    output = []
    if dfsRecursive(problem, problem.getStartState(), visitedStates,expanded):
        reverse = util.Stack()
        while not expanded.isEmpty():
            reverse.push(expanded.pop())
        while not reverse.isEmpty():
           output.append(reverse.pop()[1])
        visitedStates.clear()
    return output
    util.raiseNotDefined()

def dfsRecursive(problem, state, visitedStates, expanded):# state = (0,0)
    visitedStates.add(state)
    if problem.isGoalState(state) and state not in dfsGoalVisited:
        dfsGoalVisited.add(state)
        return True
    else:
        if len(problem.getSuccessors(state))==0:
            return False # fail, no solution
        for successor in problem.getSuccessors(state): # successor = ((5,4),'South',1)
            if(successor[0] not in visitedStates):# expand successor
                expanded.push(successor)
                if dfsRecursive(problem, successor[0], visitedStates, expanded):
                    return True
                else:
                    expanded.pop()

bfsGoalVisited = set()
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    output = []
    path = bfsHelper(problem, problem.getStartState())
    for p in path[1:]:
        output.append(p[1])
    path = bfsHelper(problem, path[-1][0])
    while path!=[]:
        for p in path[1:]:
            output.append(p[1])
        path = bfsHelper(problem, path[-1][0])  
    return output
    util.raiseNotDefined()

def bfsHelper(problem, state):
    visitedStates = set()
    queue = util.Queue()
    if(problem.isGoalState(state) and state not in bfsGoalVisited):
        bfsGoalVisited.add(state)
        return []
    queue.push([(state,'', 0)])
    while not queue.isEmpty():
        oldPath = queue.pop() # oldpath=[(problem.getStartState,'', 0)]
        if oldPath[-1][0] not in visitedStates:
            for successor in problem.getSuccessors(oldPath[-1][0]):
                newPath = list(oldPath)
                newPath.append(successor)
                queue.push(newPath)
                if problem.isGoalState(successor[0]) and successor[0] not in bfsGoalVisited:
                    bfsGoalVisited.add(successor[0])
                    return newPath
            visitedStates.add(oldPath[-1][0])
    return []


ucsGoalVisited = set()
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    output = []
    path = ucsHelper(problem, problem.getStartState())
    for p in path[1:]:
        output.append(p[1])
    path = ucsHelper(problem, path[-1][0])
    while path!=[]:
        for p in path[1:]:
            output.append(p[1])
        path = ucsHelper(problem, path[-1][0])  
    return output
    util.raiseNotDefined()

def ucsHelper(problem, state):
    visitedStates = set()
    pqueue = util.PriorityQueue()
    if(problem.isGoalState(state) and state not in ucsGoalVisited):
        ucsGoalVisited.add(state)
        return []
    pqueue.push([(state,'')], 0)
    while not pqueue.isEmpty():
        oldPath = pqueue.pop() # oldpath=[(problem.getStartState,'')]
        if oldPath[-1][0] not in visitedStates:
            for successor in problem.getSuccessors(oldPath[-1][0]):
                newPath = list(oldPath)
                newPath.append(successor)
                pqueue.push(newPath, successor[2])
                if problem.isGoalState(successor[0]) and successor[0] not in ucsGoalVisited:
                    ucsGoalVisited.add(successor[0])
                    return newPath
            visitedStates.add(oldPath[-1][0])
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    xy1 = state
    xy2 = problem.goal
    xavg = (xy1[0]+xy2[0])/2
    yavg = (xy1[1]+xy2[1])/2
    return xavg+yavg

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    path = astarHelper(problem, heuristic)
    output = []
    for p in path[1:]:
        output.append(p[1])
    return output
    util.raiseNotDefined()

def astarHelper(problem, heuristic):
    visitedStates = set()
    pqueue = util.PriorityQueue()
    if(problem.isGoalState(problem.getStartState())):
        return []
    pqueue.push([(problem.getStartState(),'', 0)], 0 + heuristic(problem.getStartState(), problem))
    allsolutions = util.PriorityQueue()
    while not pqueue.isEmpty():
        oldPath = pqueue.pop() # oldpath=[(problem.getStartState,'', 0)]
        if oldPath[-1][0] not in visitedStates:
            for successor in problem.getSuccessors(oldPath[-1][0]):
                newPath = list(oldPath)
                newPath.append(successor)
                pqueue.push(newPath, oldPath[-1][2]+successor[2]+heuristic(successor[0], problem))
                if problem.isGoalState(successor[0]):
                    allsolutions.push(newPath, oldPath[-1][2]+successor[2]+heuristic(successor[0], problem))
            visitedStates.add(oldPath[-1][0])
    if allsolutions.isEmpty():
        return []
    return allsolutions.pop()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
