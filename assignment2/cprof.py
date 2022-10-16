import traceback
import numpy as np
import signal
import re
from sys import stdin, stdout, stderr
from typing import Any, Callable, Dict, List, Tuple

from board_base import (
is_black_white,
BLACK,
WHITE,
EMPTY,
BORDER,
GO_COLOR, GO_POINT,
MAXSIZE,
coord_to_point,
opponent
)
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine

def solve_cmd(self, args: List[str]) -> None:
    self.code_from_board()
    if self.board.current_player == 1:
        current_color = 'b'
        opponent_color = 'w'
    else:
        current_color = 'w'
        opponent_color = 'b'
    
    result = self.negamax()
    #If current player is winner

    if result:
        legal_moves = GoBoardUtil.generate_legal_moves(self.board, self.board.current_player)
        for move in legal_moves:
            self.play_move_eff(move)
            if self.table.get(self.code_from_board()) == current_color:
                self.respond("{} {}".format(current_color, format_point(point_to_coord(move, self.board.size)).lower()))
                return

            self.board.board[move] = EMPTY
            self.board.current_player = opponent(self.board.current_player)
        self.respond(current_color)
    # Winner is opponent
    if result == False:
        self.respond(opponent_color)
        return

    # Cannot solve within timelimit
    #self.respond("unknown")

def negamax(self) -> bool:
    code = self.code_from_board()
    result = self.table.get(code)
    if result != None:
        if self.board.current_player == 1 and result == 'b' or self.board.current_player == 2 and result == 'w':
            return True
        else:
            return False
    legal_moves = GoBoardUtil.generate_legal_moves(self.board, self.board.current_player)
    if len(legal_moves) == 0:
        if self.board.current_player == 1:
            self.table[code] = 'w' 
        else: 
            self.table[code] = 'b' 
        return False
    for move in legal_moves:
        #old = self.board.copy()
        self.play_move_eff(move)
        #self.board.play_move(move, self.board.current_player)
        
        isWin = not self.negamax()

        # Undo the move
        self.board.board[move] = EMPTY
        self.board.current_player = opponent(self.board.current_player)
        #self.board = old

        if (isWin):
            if self.board.current_player == 1:
                self.table[code] = 'b' 
            else: 
                self.table[code] = 'w' 
            return True


    if self.board.current_player == 1:
            self.table[code] = 'w' 
    else: 
        self.table[code] = 'b' 
    return False

def code_from_board(self):
    
    return int('1'+(''.join(map(str, self.board.board.tolist()))).replace("3",""))