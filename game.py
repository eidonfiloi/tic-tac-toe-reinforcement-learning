#!/usr/bin/env python
# ----------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2015 eidonfiloi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------

""" This file contains a classic (3x3) tic tac toe game implementation.

The board is represented by a 3x3 matrix
having values X, O or EMPTY, with coordinates:

        -------------------------
        |  0,0  |  0,1  |  0,2  |
        |-----------------------|
        |  1,0  |  1,1  |  1,2  |
        |-----------------------|
        |  2,0  |  2,1  |  2,2  |
        -------------------------

Actions are represented by coordinate tuples i, j.
"""

import logging
from copy import deepcopy
from globals import *


class Game(object):
    """ This class represents a single tic tac toe game """

    def __init__(self, player_x, player_o, verbose=False):
        """ Initializes empty board with two players.
        :param player_x: agent playing X
        :param player_o: agent playing O
        :param verbose: if True, steps, moves and game states are logged in each iteration
        """
        self.player_x = player_x
        self.player_x.set_side(VALUES.X)
        self.player_o = player_o
        self.player_o.set_side(VALUES.O)
        self.verbose = verbose
        self.board = Game.setup_board()
        self.step = 0
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def setup_board():
        return [[VALUES.EMPTY for _ in range(3)] for _ in range(3)]

    def play(self):
        """ Simulates the play.
        :return: winner, that is either NOT_FINISHED during game and X, O, or DRAW at game end
        """
        self.step = 0
        winner = Game.game_state(self.board)
        while winner == VALUES.NOT_FINISHED and self.step < 9:
            player = self.next_player()
            move = player.take_action(deepcopy(self.board))
            if self.is_allowed(move):
                self.board[move[0]][move[1]] = player.side
            else:
                raise AgentActionError(player, move)
            winner = self.game_state(self.board)
            self.step += 1
            self.log(
                'step {0} GAME LOG \n'
                'player {1} takes move {2} \n'
                'game state is {3} \n'
                .format(self.step, player, move, winner))
            if self.verbose:
                Game.print_board(self.board)
        self.end_game(winner)
        return winner

    def is_allowed(self, move):
        if move is None or not isinstance(move, tuple):
            return False
        if len(move) != 2:
            return False
        if move[0] < 0 or move[0] > 2 or move[1] < 0 or move[1] > 2:
            return False
        if self.board[move[0]][move[1]] != VALUES.EMPTY:
            return False
        return True

    def next_player(self):
        if self.step < 0 or self.step > 8:
            raise ValueError
        if self.step % 2 == 0:
            return self.player_x
        else:
            return self.player_o

    @staticmethod
    def game_state(board):

        """ The state of the game.

        This method determines the state of the game.
        The state can be a winning state (X or O),
        a draw (DRAW) or not finished (NOT_FINISHED).
        :rtype : object
        :param board:
        :return: X, O, DRAW, or NOT_FINISHED
        """
        for i in range(3):
            if board[i][0] != VALUES.EMPTY and board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]
            if board[0][i] != VALUES.EMPTY and board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]
        if board[0][0] != VALUES.EMPTY and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] != VALUES.EMPTY and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        for i in range(3):
            for j in range(3):
                if board[i][j] == VALUES.EMPTY:
                    return VALUES.NOT_FINISHED
        return VALUES.DRAW

    def end_game(self, winner):

        """A method called by the end of a game.

        This method broadcasts the end state of the game to the players.
        :param winner: X, O or DRAW
        """
        if hasattr(self.player_x, 'end_game'):
            self.player_x.end_game(winner)
        if hasattr(self.player_o, 'end_game'):
            self.player_o.end_game(winner)

    @staticmethod
    def print_board(board):
        cells = []
        for i in range(3):
            for j in range(3):
                cells.append(board[i][j].center(6))
        print BOARD.format(*cells)

    def log(self, s):
        if self.verbose:
            self.logger.debug(s)






