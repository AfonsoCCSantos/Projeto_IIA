from jogos import *
from jogar import *
from collections import namedtuple
from copy import deepcopy
import random
from math import *

OJogoBT_17 = namedtuple("OJogoBT_17","to_move, board num_plays")

class EstadoBT_17(OJogoBT_17):
    cols = "abcdefgh"
    def action_format(self, old_pos, new_pos):
        col1,row1 = old_pos
        col2,row2 = new_pos
        return self.cols[col1-1]+str(row1)+"-"+self.cols[col2-1]+str(row2)
    
    def pos_disformat(self, pos):
        col = self.cols.index(pos[0])+1
        row = int(pos[1])

        return (col,row)

class JogoBT_17(Game):
    
    cols = "abcdefgh"

    def __init__(self):
        self.initial = EstadoBT_17(1,dict(),0)
        for num in [1,2,7,8]:
            for letter in range(1,len(self.cols)+1):
                self.initial.board[(letter,num)] = "W" if num <=2 else "B"
    
    def display(self, state):
        print("-----------------")   
        for row in range(8,0,-1):
            print(str(row)+"|",end="")
            for col in range(1,len(self.cols)+1):
                pos = (col,row)
                if pos in state.board:
                    print(state.board[pos], end=" ")
                else: 
                    print(".", end=" ")
            print()
        print("-+---------------")
        print(" |", end="")
        [print(col,end=" ") for col in self.cols]  
        print()
        if not self.terminal_test(state):
            print("--NEXT PLAYER: " + ("W" if state.to_move == 1 else "B"))

    def actions(self, state):
        res = list()
        col_moves = [-1,0,1]
        #ex pos "12" col row
        for pos in state.board:
            col,row = pos
            if state.to_move == 1 and state.board[pos] == "W" or state.to_move == 2 and state.board[pos] == "B":
                for dc in col_moves :
                    new_col = col + dc
                    new_row = row + 1 if state.to_move == 1 else row - 1
                    other_piece = "B" if state.to_move == 1 else "W"
                    size = 8
                    # Verificar se esta new_pos esta no board
                    if 0 < new_col <= size and new_row <= size :
                        new_pos = (new_col,new_row)
                        # Verificar se esta uma peca nesta new_pos e se podemos come-la
                        if new_pos not in state.board or (new_pos in state.board
                             and state.board[new_pos] == other_piece and new_col != col):
                            res.append(state.action_format(pos,new_pos))
        res.sort()
        return res
    
    def result(self, state, move):
        old_pos, new_pos = move.split("-")
        new_board = deepcopy(state.board)
        del new_board[state.pos_disformat(old_pos)] 
        new_board[state.pos_disformat(new_pos)] = "W" if state.to_move == 1 else "B"
        new_to_move = 1 if state.to_move == 2 else 2
        return EstadoBT_17(new_to_move,new_board,state.num_plays+1)

    def executa(self, state, actions):
        curr_state = deepcopy(state)
        for action in actions:
            curr_state = self.result(curr_state, action)
        return curr_state   

    def terminal_test(self, state):
        for pos,piece in state.board.items():
            if piece == "W" and pos[1] == 8 or piece == "B" and pos[1] == 1:
                return True
        return False
            
    def utility(self, state, player):
        if not self.terminal_test(state):
            return 0
        if player == state.to_move:
            return -1
        return 1

class Belarmino(JogadorAlfaBeta):

    def __init__(self):
        super().__init__("Belarmino", 2, self.func_aval)

    def func_aval(self, state, player):
        # i^i * count(Bi) = i^i + i^i ..
        piece_player = "W" if player == 1 else "B"
        res = 0
        for pos,piece in state.board.items():
            row = pos[1]
            if piece_player == piece:
                if piece == "W":
                    res += (row**row)
                else:
                    inv = 8 - row + 1
                    res += (inv**inv)
        return res

class BelarminoProMax(JogadorAlfaBeta):
    
    def __init__(self):
        super().__init__("BelarminoProMax", 2, self.func_aval)
    
    def func_aval(self, state, player):
        # i^i * count(Bi) = i^i + i^i ..
        piece_player = "W" if player == 1 else "B"
        res = 0
        for pos,piece in state.board.items():
            row = pos[1]
            if piece_player == piece:
                if piece == "W":
                    res += (row**row) / (state.num_plays**2)
                else:
                    inv = 8 - row + 1
                    res += (inv**inv) / (state.num_plays**2)
        return res



class GigaChad(JogadorAlfaBeta):
    def __init__(self):
        super().__init__("Alexandre", 2, self.func_aval)
    
    def func_aval(self, state, player):
        piece_player = "W" if player == 1 else "B"
        res = 0
        counter = 0
        for pos,piece in state.board.items():
            row = pos[1]
            # Win or lost state
            if (piece == "W" and row == 8) or (piece == "B" and row == 1):
                return (8**8 * 16)-state.num_plays if piece_player == piece else -(8**8 * 16)
            # State where win/lost is guaranteed next round
            if ((piece == "W" and row == 7) or (piece == "B" and row == 2)) and notThreathned(pos,state,piece):
                return (8**8 * 15)-state.num_plays if piece_player == piece else -(8**8 * 15)
            if piece_player == piece:
                if piece == "W":
                    res += (row**row) 
                else:
                    inv = 8 - row + 1
                    res += (inv**inv)
                # Vantagem em numero de pecas
                counter += 1
            else:
                counter -=1
        return res + (res**counter)

def notThreathned(pos,state,piece):
    col,row = pos
    if piece == "W":
        attacker1 = (col-1,row+1)
        attacker2 = (col+1,row+1)
        return attacker1 not in state.board and attacker2 not in state.board
    if piece == "B":
        attacker1 = (col-1,row-1)
        attacker2 = (col+1,row-1)
        return attacker1 not in state.board and attacker2 not in state.board               

class MaisPecas(JogadorAlfaBeta):
    def __init__(self):
        super().__init__("mais pecas", 2, self.func_aval)
    
    def func_aval(self, state, player):
        res = 0
        player_piece = "W" if player == 1 else "B"
        for piece in state.board.values():
            if piece == player_piece:
                res+=1
            else:
                res-=1
        return res

class RandomPlayer(Jogador):

    def __init__(self):
        super().__init__("aleatorio", self.fun)

    def fun(self, game,state):
        return random.choice(game.actions(state))

class Query(Jogador):

    def __init__(self):
        super().__init__("eu", self.fun)
    
    def fun(self, game,state):
        game.display(state)
        return query_player(game,state)


class PecasNoMeio(JogadorAlfaBeta):
    def __init__(self):
        super().__init__("pecas no meio", 2, self.func_aval)
    
    def func_aval(self, state, player):
        piece_player = "W" if player == 1 else "B"
        res = 0
        middle = 4.5
        for pos,piece in state.board.items():
            col,row = pos
            if piece_player == piece:
                if piece == "W":
                    res += ((row**row) / (state.num_plays**2)) / (abs(col-middle) * abs(row-middle))
                else:
                    inv = 8-row
                    res += ((inv**inv) / (state.num_plays**2)) / (abs(col-middle) * abs(row-middle))
        return res
     
jj = JogoBT_17() 

for i in range(0,10):
    a = joga11(jj,GigaChad(),BelarminoProMax())
    print(a[0][a[-1] if a[-1] == -1 else 0])

# print(a)
# mostraJogo(jj,a,True,True)

# valorizar pecas pro meio
# desvalorizar pecas isoladas
        
	
# s= jj.executa(jj.initial,
# ['f2-f3', 'e7-d6', 'd2-e3', 'd6-d5', 'b2-b3', 'd5-c4',
# 'a2-a3', 'c4-b3', 'e3-d4', 'b3-c2', 'e1-f2', 'c2-d1'])
# jj.display(s)
# print(jj.terminal_test(s))