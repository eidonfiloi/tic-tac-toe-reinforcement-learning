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

""" This file contains global constructions/definitions needed for the game and for agents."""


class Enum(object):

    def __init__(self, list):
        self.list = list
        self.size = len(self.list)

    def __getattr__(self, name):
        if name in self.list:
            return name
        raise AttributeError

    def __getitem__(self, index):
        if index in range(self.size):
            return self.list[index]
        raise AttributeError


VALUES = Enum(['EMPTY', 'X', 'O', 'DRAW', 'NOT_FINISHED'])

BOARD = "\n" \
        "----------------------------\n" \
        "| {0} | {1} | {2} |\n" \
        "|--------------------------|\n" \
        "| {3} | {4} | {5} |\n" \
        "|--------------------------|\n" \
        "| {6} | {7} | {8} |\n" \
        "----------------------------"

NAMES = [VALUES.EMPTY, VALUES.X, VALUES.O]


class AgentActionError(Exception):

    def __init__(self, agent, move):
        self.agent = agent
        self.move = move

    def __repr__(self):
        return repr('not allowed move {0} from agent {1}'.format(self.move, self.agent))


class IllegalBoardStateError(Exception):

    def __init__(self, board):
        self.board = board

    def __repr__(self):
        return repr('not allowed board state {0}'.format(self.board))




