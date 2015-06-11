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


class GameTest(unittest.TestCase):

    def setUp(self):
        self.player_x = DummyAgent()
        self.player_o = DummyAgent()
        self.game = Game(self.player_x, self.player_o, verbose=False)
        
    def test_board(self):
        start_board = [['EMPTY', 'EMPTY', 'EMPTY'], ['EMPTY', 'EMPTY', 'EMPTY'], ['EMPTY', 'EMPTY', 'EMPTY']]
        self.assertListEqual(start_board, self.game.board, "no board set up")

    def test_player_sides(self):
        self.assertEqual(VALUES.X, self.player_x.side, 'player x side is incorrect')
        self.assertEqual(VALUES.O, self.player_o.side, 'player o side is incorrect')

    def test_next_player(self):
        self.game.step = 2
        self.assertEqual(self.player_x, self.game.next_player())
        self.game.step = 5
        self.assertEqual(self.player_o, self.game.next_player())

    def test_winner_x(self):
        self.assertEqual(VALUES.X, self.game.play())

    def test_game_test_not_finished1(self):
        state = [['EMPTY', 'EMPTY', 'EMPTY'], ['EMPTY', 'EMPTY', 'EMPTY'], ['EMPTY', 'EMPTY', 'EMPTY']]
        self.assertEqual(VALUES.NOT_FINISHED, self.game.game_state(state), 'game state incorrect')

    def test_game_test_not_finished2(self):
        state = [['EMPTY', 'X', 'EMPTY'], ['EMPTY', 'O', 'EMPTY'], ['X', 'EMPTY', 'EMPTY']]
        self.assertEqual(VALUES.NOT_FINISHED, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_xr1(self):
        state = [['X', 'X', 'X'], ['X', 'O', 'O'], ['O', 'EMPTY', 'EMPTY']]
        self.assertEqual(VALUES.X, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_xr2(self):
        state = [['X', 'O', 'O'], ['X', 'X', 'X'], ['EMPTY', 'EMPTY', 'O']]
        self.assertEqual(VALUES.X, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_xr3(self):
        state = [['X', 'O', 'O'], ['EMPTY', 'EMPTY', 'O'], ['X', 'X', 'X']]
        self.assertEqual(VALUES.X, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_xd1(self):
        state = [['X', 'O', 'EMPTY'], ['O', 'X', 'X'], ['EMPTY', 'O', 'X']]
        self.assertEqual(VALUES.X, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_xd2(self):
        state = [['O', 'O', 'X'], ['EMPTY', 'X', 'EMPTY'], ['X', 'X', 'O']]
        self.assertEqual(VALUES.X, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_xc1(self):
        state = [['X', 'O', 'O'], ['X', 'X', 'O'], ['X', 'EMPTY', 'EMPTY']]
        self.assertEqual(VALUES.X, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_xc2(self):
        state = [['O', 'X', 'X'], ['O', 'X', 'O'], ['EMPTY', 'X', 'EMPTY']]
        self.assertEqual(VALUES.X, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_xc3(self):
        state = [['O', 'O', 'X'], ['EMPTY', 'EMPTY', 'X'], ['EMPTY', 'EMPTY', 'X']]
        self.assertEqual(VALUES.X, self.game.game_state(state), 'game state incorrect')
        
    def test_game_test_winner_or1(self):
        state = [['O', 'O', 'O'], ['X', 'X', 'EMPTY'], ['X', 'EMPTY', 'EMPTY']]
        self.assertEqual(VALUES.O, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_or2(self):
        state = [['X', 'X', 'EMPTY'], ['O', 'O', 'O'], ['X', 'EMPTY', 'EMPTY']]
        self.assertEqual(VALUES.O, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_or3(self):
        state = [['X', 'X', 'EMPTY'], ['X', 'EMPTY', 'EMPTY'], ['O', 'O', 'O']]
        self.assertEqual(VALUES.O, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_od1(self):
        state = [['O', 'X', 'X'], ['X', 'O', 'EMPTY'], ['EMPTY', 'EMPTY', 'O']]
        self.assertEqual(VALUES.O, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_od2(self):
        state = [['X', 'X', 'O'], ['X', 'O', 'EMPTY'], ['O', 'EMPTY', 'EMPTY']]
        self.assertEqual(VALUES.O, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_oc1(self):
        state = [['O', 'X', 'X'], ['O', 'X', 'EMPTY'], ['O', 'EMPTY', 'EMPTY']]
        self.assertEqual(VALUES.O, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_oc2(self):
        state = [['X', 'O', 'EMPTY'], ['X', 'O', 'X'], ['EMPTY', 'O', 'EMPTY']]
        self.assertEqual(VALUES.O, self.game.game_state(state), 'game state incorrect')

    def test_game_test_winner_oc3(self):
        state = [['X', 'X', 'O'], ['X', 'EMPTY', 'O'], ['EMPTY', 'EMPTY', 'O']]
        self.assertEqual(VALUES.O, self.game.game_state(state), 'game state incorrect')

    def test_game_test_draw(self):
        state = [['X', 'O', 'X'], ['X', 'O', 'X'], ['O', 'X', 'O']]
        self.assertEqual(VALUES.DRAW, self.game.game_state(state), 'game state incorrect')

    def test_is_allowed_true(self):
        move = (1, 2)
        self.assertTrue(self.game.is_allowed(move), 'move should be allowed')

    def test_is_allowed_false_index(self):
        move = (-1, 2)
        self.assertFalse(self.game.is_allowed(move), 'move should not be allowed')

    def test_is_allowed_false_state(self):
        board = deepcopy(self.game.board)
        self.game.board = [['X', 'X', 'O'], ['X', 'EMPTY', 'O'], ['EMPTY', 'EMPTY', 'O']]
        move = (0, 2)
        self.assertFalse(self.game.is_allowed(move), 'move should not be allowed')
        self.game.board = board

    def test_is_allowed_none(self):
        move = None
        self.assertFalse(self.game.is_allowed(move), 'move should not be allowed')

    def test_is_allowed_no_tuple(self):
        move = {}
        self.assertFalse(self.game.is_allowed(move), 'move should not be allowed')

    def test_is_allowed_tuple_size(self):
        move = 1, 2, 3
        self.assertFalse(self.game.is_allowed(move), 'move should not be allowed')


if __name__ == '__main__':
    unittest.main()
