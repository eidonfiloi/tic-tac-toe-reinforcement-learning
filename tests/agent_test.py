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

import unittest
from agent import *
from game import *


class AgentTest(unittest.TestCase):

    def setUp(self):
        self.agent = WinBlockingRandomAgent()
        self.agent.set_side(VALUES.X)

    def test_check_triple_none(self):
        arr = ['X', 'O', 'EMPTY']
        side, index = self.agent._check_triple(arr)
        self.assertEqual((None, -1), (side, index), 'triple is not homogenous')

    def test_check_triple_x(self):
        arr = ['X', 'X', 'EMPTY']
        side, index = self.agent._check_triple(arr)
        self.assertEqual(('X', 2), (side, index), 'triple should be homogenous')

    def test_check_triple_o(self):
        arr = ['EMPTY', 'O', 'O']
        side, index = self.agent._check_triple(arr)
        self.assertEqual(('O', 0), (side, index), 'triple should be homogenous')

    def test_block_move_win_row(self):
        state = [['X', 'X', 'EMPTY'], ['EMPTY', 'EMPTY', 'O'], ['EMPTY', 'O', 'O']]
        move = self.agent._win_block_move(state)
        self.assertEqual((0, 2), move, 'wrong move...missed win in row')

    def test_block_move_win_col(self):
        state = [['X', 'EMPTY', 'EMPTY'], ['EMPTY', 'EMPTY', 'O'], ['X', 'O', 'O']]
        move = self.agent._win_block_move(state)
        self.assertEqual((1, 0), move, 'wrong move...missed win in column')

    def test_block_move_win_d(self):
        state = [['X', 'EMPTY', 'EMPTY'], ['EMPTY', 'EMPTY', 'O'], ['EMPTY', 'O', 'X']]
        move = self.agent._win_block_move(state)
        self.assertEqual((1, 1), move, 'wrong move...missed win in diagonal')

    def test_block_move_block_row(self):
        state = [['X', 'EMPTY', 'EMPTY'], ['EMPTY', 'X', 'EMPTY'], ['EMPTY', 'O', 'O']]
        move = self.agent._win_block_move(state)
        self.assertEqual((2, 0), move, 'wrong win blocking move')

    def test_block_move_block_col(self):
        state = [['X', 'EMPTY', 'EMPTY'], ['EMPTY', 'EMPTY', 'O'], ['EMPTY', 'X', 'O']]
        move = self.agent._win_block_move(state)
        self.assertEqual((0, 2), move, 'wrong win blocking move')

    def test_block_move_block_d(self):
        state = [['X', 'X', 'O'], ['EMPTY', 'EMPTY', 'O'], ['O', 'EMPTY', 'X']]
        move = self.agent._win_block_move(state)
        self.assertEqual((1, 1), move, 'wrong win blocking move')

    def test_random_agent(self):
        state = [['X', 'X', 'O'], ['O', 'EMPTY', 'X'], ['EMPTY', 'EMPTY', 'O']]
        self.agent.visited_state_actions = {(self.agent.represent_state(state), (2, 0)): 0,
                                            (self.agent.represent_state(state), (1, 1)): 0}
        move = self.agent.take_action(state)
        self.assertEqual((2, 1), move, 'already seen action was taken')

if __name__ == '__main__':
    unittest.main()