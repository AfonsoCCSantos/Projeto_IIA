from jogos import *
from collections import namedtuple
from copy import deepcopy

OJogoBT_17 = namedtuple("OJogoBT_17","to_move, board")

class EstadoJogoBT_17(OJogoBT_17):
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
        self.initial = EstadoJogoBT_17(1,dict())
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
        print("--NEXT PLAYER: " + ("W" if state.to_move == 1 else "B"))

    def actions(self, state):
        res = list()
        col_moves = [-1,0,1]
        #ex pos "12" col row
        for pos,piece in state.board.items():
            col,row = pos
            if state.to_move == 1 and state.board[pos] == "W" or state.to_move == 2 and state.board[pos] == "B" :
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
        return EstadoJogoBT_17(new_to_move,new_board)
        
game = JogoBT_17()
print(game.actions(game.initial)) 
game.display(game.result(game.initial, "a2-a3")) 