# monticarlo AI resau de nuron
#web socet socket.io react flask
from copy import deepcopy
import csv
from math import inf
import math
from random import random
from random import randint
import time
import random

MAX = +1 
MIN = -1

class ConnectFourBoard :

    def __init__(self,board=None,depth=0,piece=MAX): 
        self.board = [[0 for _ in range(7)] for _ in range(6)] if board is None else board
        self.piece = piece # 1 or -1
        self.depth = depth # 1 to depthlim
        self.Action = (0,0)
        self.NextAction = (0,0)
        self.value = 0
        self.alpha = 0
        self.beta = 0
        
    def Win_Value(self,Tie,piece):
        if Tie:
            return 0
        else:
            return piece*100

    def heuristicEval1(self,piece):
        row , col = self.Action
        if col > 3 : 
            col-=6
            col*=-1
        H = 1+col
        if piece == MAX: return -H
        else: return H

    def heuristicEval2(self,piece):
        score = 0
        for row in range(6):
            for col in range(4):
                score += self.score_window([self.board[row][col], self.board[row][col + 1],
                                            self.board[row][col + 2], self.board[row][col + 3]])
        for col in range(7):
            for row in range(3):
                score += self.score_window([self.board[row][col], self.board[row + 1][col],
                                            self.board[row + 2][col], self.board[row + 3][col]])
        for row in range(3, 6):
            for col in range(4):
                score += self.score_window([self.board[row - i][col + i] for i in range(4)])
        for row in range(3, 6):
            for col in range(3, 7):
                score += self.score_window([self.board[row - i][col - i] for i in range(4)])
        if piece == MAX: return -score
        else: return score
    def score_window(self, window):
        if window.count(MAX) == 4:
            return 100
        elif window.count(MAX) == 3 and window.count(0) == 1:
            return 15
        elif window.count(MAX) == 2 and window.count(0) == 2:
            return 8
        elif window.count(MIN) == 2 and window.count(0) == 2:
            return -12
        elif window.count(MIN) == 3 and window.count(0) == 1:
            return -15        
        # contre attack
        elif window.count(MIN) == 3 and window.count(MAX) == 1:
            return 30
        elif window.count(MIN) == 2 and window.count(MAX) == 1 and window.count(0) == 1:
            return 10
        elif window.count(MIN) == 4:
            return -100
        else:
            return 0
    
    def heuristicEval3(self, piece):
        score = 0
        opponent_piece = -piece  # Assuming MAX is 1 and MIN is -1

        # Center control: Encourage having pieces in the center columns (3 and 4)
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == piece:
                    if col == 3 or col == 4:
                        score += 3
                    elif col == 2 or col == 5:
                        score += 2
                    elif col == 1 or col == 6:
                        score += 1

        # Piece distribution: Encourage distributing pieces across different columns
        ai_col_counts = [0] * 7
        opponent_col_counts = [0] * 7
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == piece:
                    ai_col_counts[col] += 1
                elif self.board[row][col] == opponent_piece:
                    opponent_col_counts[col] += 1

        for col in range(7):
            score += (ai_col_counts[col] - opponent_col_counts[col])

        return score  
    
    def heuristicChois(self,piece,HChois):
        match HChois:
            case 1:return self.heuristicEval1(piece)
            case 2:return self.heuristicEval2(piece)
            case 3:return self.heuristicEval3(piece)

    def getPossibleMoves(self,piece):
        succs = list()
        for j in range(7):
            find = False
            for i in range(5, -1, -1):
                if self.board[i][j]==0:
                    find=True
                    successor = deepcopy(self)
                    successor.depth = self.depth+1
                    successor.piece = self.piece*-1
                    successor.Action = (i,j)
                    successor.makeMove(i,j,piece)
                    break
            if find:
                succs.append(successor)
        return succs
    
    def drawBoard(self):
        for i in range(6):
            line =" "
            for j in range(7):
                if self.board[i][j]==MAX:p = 'R'
                elif self.board[i][j]==MIN:p = 'Y'
                else: p = '_'
                line += p+"  "
            print(line)
        print()

    def makeMove(self,row,col,piece):
        self.board[row][col]=piece

    def win(self,piece):
        #Diagonale Right
        for row in range(3, 6):
            for col in range(4):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    return True
        #Diagonale Left
        for row in range(3, 6):
            for col in range(3, 7):
                if all(self.board[row - i][col - i] == piece for i in range(4)):
                    return True
        # Horisontale
        for row in range(6):
            if self.board[row][3] == piece:
                for col in range(4):
                    if all(self.board[row][col+i] == piece for i in range(4)):
                        return True
        # Verticale
        for col in range(7):
            if self.board[2][col] == piece:
                for row in range(3):
                    if all(self.board[row+i][col] == piece for i in range(4)):
                        return True
        return False
    
    @staticmethod
    def wtireWiner(piece):
        if piece==MAX:
            print("Red win")
        else:
            print("Yellow win")

    def Tie(self):
        for j in range(7):
            if self.board[0][j] == 0:
                return False
        return True

    def gameOver(self,piece):
        return self.Tie() or self.win(piece)

    def moveInCol(self,col):
        find = False
        if col >=0 and col <=6:
            for i in range(5, -1, -1):
                if self.board[i][col]==0:
                    find=True
                    break
            if find: return i
            else :return -1
        else : return -2  
# MCTS
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def expand(self, successors):
        for successor in successors:
            child_node = Node(successor, parent=self)
            self.children.append(child_node)

    def ucb1(self, total_visits):
        if self.visits == 0:
            return math.inf
        exploitation = self.value / self.visits
        exploration = math.sqrt(2 * math.log(total_visits) / self.visits)
        return exploitation + exploration

    def select_child(self):
        total_visits = sum(child.visits for child in self.children)
        best_child = max(self.children, key=lambda child: child.ucb1(total_visits))
        return best_child
    
class Play:
    DepthLim = 5
    @staticmethod
    def humanTurn(state) : 
        print("")
        play_row = -1
        while play_row == -1:
            play_col = int(input("your turn\n"))
            play_col -=1
            play_row=state.moveInCol(play_col)
            if play_row == -1: print("col full")
            elif play_row == -2: print("from 1 to 7")
        
        return play_row , play_col
    @staticmethod
    def humanTurn2(state,play_col) :
        err = 0
        play_row=state.moveInCol(play_col)
        if play_row == -1: err = 1
        return play_row , err

    @staticmethod
    def computerTurn1(state) :
        NextAction = Play.mcts(state)
        print(NextAction)
        return NextAction
    
    @staticmethod
    def computerTurn2(state) :
        NextAction , _ = Play.minimaxAlphaBetaPruning(state,Play.DepthLim,-inf,+inf,MAX,2)
        return NextAction
    
    @staticmethod
    def playrandom(state) :
        play_row = -1
        while play_row == -1:
            play_col=randint(0, 6)
            play_row=state.moveInCol(play_col)
        
        return play_row , play_col  
    
    @staticmethod
    def play(state,Turn):
        if Turn == MAX:
            print("AI 1")
            play_row,play_col  = Play.computerTurn1(state)
        else :
            print("AI 2")
            play_row,play_col  = Play.computerTurn2(state)

        return play_col , play_row
    @staticmethod
    def minimaxAlphaBetaPruning(state, depthlim, alpha=-inf, beta=+inf, piece=MAX,HChois=1):
        if state.depth < depthlim :
            if piece==MAX:
                state.value = -inf
                state.alpha = -inf
                state.beta = +inf
                for successor in state.getPossibleMoves(piece):
                    NextAction , NextValue = Play.minimaxAlphaBetaPruning(successor,depthlim,state.alpha,state.beta,MIN,HChois)
                    if state.value < NextValue:
                        state.value = NextValue
                        state.NextAction = NextAction
                    state.alpha = max(state.value,alpha)
                    if state.value >=beta:
                        if state.depth == 0:
                            return state.NextAction , state.value
                        else:
                            return state.Action , state.value 
            else:
                state.value = inf
                state.alpha = -inf
                state.beta = inf
                for successor in state.getPossibleMoves(piece):
                    NextAction , NextValue = Play.minimaxAlphaBetaPruning(successor,depthlim,state.alpha,state.beta,MAX,HChois)
                    if state.value > NextValue:
                        state.value = NextValue
                        state.NextAction = NextAction
                    state.beta = min(state.value,beta)
                    if state.value <=alpha:
                        if state.depth == 0:
                            return state.NextAction , state.value
                        else:
                            return state.Action , state.value 
        else:                
            if state.gameOver(state.piece):
                state.value = state.Win_Value(state.Tie(),state.piece)
            else :
                state.value = state.heuristicChois(state.piece,HChois)
        
        if state.depth == 0:
            return state.NextAction , state.value
        else:
            return state.Action , state.value 
           
    # MCTS
    @staticmethod
    def mcts(root_state, num_simulations=1000):
        root = Node(root_state)

        for _ in range(num_simulations):
            node = root
            state = deepcopy(root_state)  # Create a deepcopy for simulation

            # Selection: Traverse the tree using UCB1 until reaching an unvisited node or a terminal node.
            while not state.gameOver(state.piece):
                if not node.children:
                    break  # If leaf node is reached, break out
                node = node.select_child()
                action = node.state.Action
                state.makeMove(action[0], action[1], state.piece)
                state.piece *= -1

            # Expansion: If the node is unvisited and not terminal, expand it.
            if not node.children and not state.gameOver(state.piece):
                successors = state.getPossibleMoves(state.piece)
                node.expand(successors)
                node = node.select_child()
                action = node.state.Action
                state.makeMove(action[0], action[1], state.piece)
                state.piece *= -1

            # Simulation: Simulate random play from the current state until reaching a terminal state.
            while not state.gameOver(state.piece):
                successors = state.getPossibleMoves(state.piece)
                if not successors:
                    break
                random_successor = random.choice(successors)
                state = deepcopy(random_successor)
                state.piece *= -1

            # Backpropagation: Update values and visit counts
            result = state.heuristicEval1(state.piece)  # Use a heuristic to evaluate the leaf node
            Play.backpropagate(node, result)

        best_action_node = max(root.children, key=lambda child: child.visits)
        return best_action_node.state.Action

    @staticmethod
    def backpropagate(node, result):
        while node:
            node.visits += 1
            node.value += result
            node = node.parent

    @staticmethod
    def backpropagate(node, result):
        while node:
            node.visits += 1
            node.value += result
            node = node.parent

def main():
    playing = True
    Turn = MAX
    state = ConnectFourBoard()
    state.drawBoard()

    while(playing):
        #
        play_col , play_row = Play.play(state,Turn)
        state.makeMove(play_row,play_col,Turn)
        state.drawBoard()
        time.sleep(0.4)
        # end game 
        if state.gameOver(Turn):
            if state.Tie():
                print("tie")
            else :
                ConnectFourBoard.wtireWiner(Turn)
            playing = False
            
        # change player
        Turn*=-1

if __name__ == "__main__":
    main()