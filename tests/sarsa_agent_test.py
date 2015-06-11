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


class SarsaAgentTest(unittest.TestCase):

    def setUp(self):
        self.a = 0.1
        self.eps = 0.0
        self.g = 0.9
        self.agent = SarsaAgent(alpha=self.a,
                                epsilon=self.eps,
                                gamma=self.g,
                                learning=False,
                                win=1.0,
                                draw=0.0,
                                lose=-1.0,
                                not_finished=0.0)
        self.agent.set_side(VALUES.X)
        #
        # ----------------------------
        # |   X    |   O    | 0.748  |
        # |--------------------------|
        # | 0.871  | 1.194  | 0.500  |
        # |--------------------------|
        # | 0.500  |   O    | 0.500  |
        # ----------------------------
        #
        self.s_1 = [['X', 'O', 'EMPTY'], ['EMPTY', 'EMPTY', 'EMPTY'], ['EMPTY', 'O', 'EMPTY']]
        self.s1 = self.agent.represent_state(self.s_1)
        self.a11 = (0, 2)
        self.q11 = 0.748
        self.a12 = (1, 0)
        self.q12 = 0.871
        self.a13 = (1, 1)
        self.q13 = 1.194
        self.a14 = (1, 2)
        self.q14 = 0.5
        self.a15 = (2, 0)
        self.q15 = 0.5
        self.a16 = (2, 2)
        self.q16 = 0.5
        #
        # ----------------------------
        # |   X    |   O    |   O    |
        # |--------------------------|
        # |  0.2   |   X    | -0.25  |
        # |--------------------------|
        # | -0.25  |   O    |  0.75  |
        # ----------------------------
        self.s_2 = [['X', 'O', 'O'], ['EMPTY', 'X', 'EMPTY'], ['EMPTY', 'O', 'EMPTY']]
        self.s2 = self.agent.represent_state(self.s_2)
        self.a21 = (1, 0)
        self.q21 = 0.2
        self.a22 = (1, 2)
        self.q22 = -0.25
        self.a23 = (2, 0)
        self.q23 = -0.25
        self.a24 = (2, 2)
        self.q24 = 0.75

        q_values = {(self.s1, self.a11): self.q11,
                    (self.s1, self.a12): self.q12,
                    (self.s1, self.a13): self.q13,
                    (self.s1, self.a14): self.q14,
                    (self.s1, self.a15): self.q15,
                    (self.s1, self.a16): self.q16,
                    (self.s2, self.a21): self.q21,
                    (self.s2, self.a22): self.q22,
                    (self.s2, self.a23): self.q23,
                    (self.s2, self.a24): self.q24}

        self.agent.q_values = q_values

    def test_next_action(self):
        next_action = self.agent.take_action(self.s1)

        self.assertEqual(self.a13, next_action,
                         "next action {0} has not highest q-value".format(next_action))

    def test_update_q_value(self):
        self.agent.learning = True
        self.agent.prev_state = self.s_1
        self.agent.prev_action = self.a13
        self.agent.prev_q_val = self.q13

        next_state = self.s_2
        next_value = self.agent.q_values[(self.s2, self.a24)]

        reward = 0

        q_val_should_be = self.q13 + self.a*(reward + self.g*self.q24 - self.q13)
        self.agent.update_q_values(next_state, next_value)
        q_val_calculated = self.agent.q_values[self.s1, self.agent.prev_action]

        self.assertEqual(q_val_should_be, q_val_calculated, 'update q-value is incorrect')

    def test_update_q_value_randomized(self):
        self.agent.learning = True
        self.agent.prev_state = self.s_1
        self.agent.prev_action = self.a13
        self.agent.prev_q_val = self.q13

        next_state = self.s_2
        next_action = self.a24
        del self.agent.q_values[self.s2, self.a24]
        next_value = self.agent.q_value((self.s2, next_action))

        reward = 0.0
        value = 0.0

        q_val_should_be = self.q13 + self.a*(reward + self.g*value - self.q13)
        self.agent.update_q_values(next_state, next_value)
        q_val_calculated = self.agent.q_values[self.s1, self.agent.prev_action]

        self.assertEqual(q_val_should_be, q_val_calculated, 'update q-value is incorrect')


if __name__ == '__main__':
    unittest.main()