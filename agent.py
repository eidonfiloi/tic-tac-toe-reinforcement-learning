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

""" This file contains classes implementing agents that play tic tac toe. """

import abc
import random
import pickle
import csv
from game import *


class Agent(object):
    """This class is an abstract base class for agents playing tic tac toe.

    Every concrete agent extending this class should implement a take_action method.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.side = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def __repr__(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def take_action(self, state):
        """ The agent takes action in a state.

        Extending agents should implement this abstract method.
        :param state: [[], [], []] a board state
        :return: action: i, j which cell to choose
        """

    @staticmethod
    def random_next_action(state):
        """ A basic random action generation method."""

        possible_moves = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == VALUES.EMPTY:
                    possible_moves.append((i, j))
        return random.choice(possible_moves)

    @staticmethod
    def represent_state(state):
        """ A basic state representation.

        It converts states in list format to hashable (tuple) format (inner lists as well).
        """
        return tuple(state[0]), tuple(state[1]), tuple(state[2])

    def set_side(self, side):
        if side == VALUES.X or side == VALUES.O:
            self.side = side


class RandomAgent(Agent):
    """ This is an agent playing (almost) randomly.

     It keeps track of already played moves in a given state.
     If possible, it chooses a random not-yet-played action
     otherwise it chooses randomly one of the already seen actions.
    """

    def __init__(self, ):
        super(RandomAgent, self).__init__()
        self.winner = None
        self.visited_state_actions = {}

    def take_action(self, state):
        possible_moves = []
        possible_not_visited_moves = []
        hashable_state = self.represent_state(state)
        for i in range(3):
            for j in range(3):
                if state[i][j] == VALUES.EMPTY:
                    possible_moves.append((i, j))
                    if not (hashable_state, (i, j)) in self.visited_state_actions:
                        possible_not_visited_moves.append((i, j))
        random_move = random.choice(possible_not_visited_moves) if len(
            possible_not_visited_moves) > 0 else random.choice(possible_moves)
        self.visited_state_actions[hashable_state, random_move] = 0
        return random_move

    def end_game(self, winner):
        self.winner = winner


class WinBlockingRandomAgent(RandomAgent):
    """ This is a win blocking (semi)random agent.

    It first looks for a winning action,
    then for blocking opponent's win and then a random move.
    """
    def __init__(self):
        super(WinBlockingRandomAgent, self).__init__()

    def take_action(self, state):
        win_block_move = self._win_block_move(state)
        if win_block_move is not None:
            return win_block_move
        return super(WinBlockingRandomAgent, self).take_action(state)

    @staticmethod
    def _check_triple(arr):
        """ This is a private static helper method.

        It determines if arr contains
        exactly 2 occupied cells of a player and an empty cell
        and returns the side of this player and the index of the empty cell
        :param arr: a row, a column or a diagonal
        :return: side, index
        """

        count_x = 0
        count_o = 0
        count_empty = 0
        for idx, el in enumerate(arr):
            if el == VALUES.X:
                count_x += 1
            elif el == VALUES.O:
                count_o += 1
            elif el == VALUES.EMPTY:
                count_empty += 1
        if count_x == 2 and count_o == 0 and count_empty == 1:
            return VALUES.X, arr.index(VALUES.EMPTY)
        elif count_o == 2 and count_x == 0 and count_empty == 1:
            return VALUES.O, arr.index(VALUES.EMPTY)
        else:
            return None, -1

    def _win_block_move(self, state):
        """ This is a private helper method.

        It tries to find first a winning move
        then a move blocking the opponent's win,
        otherwise returns None.
        :param state:
        :return: win_block move
        """
        block_moves = []
        for i in range(3):
            side, index = self._check_triple(state[i])
            if index != -1:
                if side == self.side:
                    return i, index
                else:
                    block_moves.append((i, index))
            side, index = self._check_triple([state[0][i], state[1][i], state[2][i]])
            if index != -1:
                if side == self.side:
                    return index, i
                else:
                    block_moves.append((index, i))

        side, index = self._check_triple([state[0][0], state[1][1], state[2][2]])
        if index != -1:
            if side == self.side:
                return index, index
            else:
                block_moves.append((index, index))
        side, index = self._check_triple([state[0][2], state[1][1], state[2][0]])
        if index != -1:
            if side == self.side:
                return index, 2 - index
            else:
                block_moves.append((index, 2 - index))
        if len(block_moves) > 0:
            return random.choice(block_moves)
        else:
            return None


class DummyAgent(Agent):
    """ This is a simple linearly playing agent.

    It always takes the next possible move
    in a row of smallest index and a column of smallest index.
    """

    def __init__(self):
        super(DummyAgent, self).__init__()
        self.winner = None

    def take_action(self, state):
        move = None
        for i in range(3):
            for j in range(3):
                if state[i][j] == VALUES.EMPTY:
                    return i, j
        return move

    def end_game(self, winner):
        self.winner = winner


class HumanAgent(Agent):

    """ A human agent.

    She plays by typing moves in the format i, j on the console.
    """

    def __init__(self):
        super(HumanAgent, self).__init__()
        self.winner = None

    def take_action(self, state):
        Game.print_board(state)
        not_allowed = True
        error_trial = 0
        action = None
        while not_allowed and error_trial < 3:
            error_trial += 1
            raw_action_input = raw_input('Your move? ').split(',')
            action = int(raw_action_input[0]), int(raw_action_input[1])
            check_state = state[action[0]][action[1]]
            if check_state == VALUES.EMPTY:
                not_allowed = False
            else:
                self.logger.info('not allowed move. choose an empty cell')
        return action

    def end_game(self, winner):
        self.winner = winner
        if self.winner == VALUES.DRAW:
            self.logger.info('The game ended with a DRAW.')
        elif self.winner == self.side:
            self.logger.info('You won the game.')
        else:
            self.logger.info('The opponent won the game.')


class BaseQAgent(Agent):
    """ This is a base class for TD learning agents.

    The class implements the epsilon greedy policy and
    temporal difference learning with action values (Q-values)
    """

    def __init__(self,
                 q_values=None,
                 alpha=0.1,
                 epsilon=0.1,
                 epsilon_decay=None,
                 gamma=0.9,
                 verbose=False,
                 learning=True,
                 win=1.0,
                 draw=0.0,
                 lose=-1.0,
                 not_finished=0.0):
        """
            :param q_values: a dictionary holding Q(s,a) values
            :param alpha: step size parameter in the TD update formula
            :param epsilon: the exploration probability of epsilon-greedy
            :param epsilon_decay: decay factor for epsilon (e.g. 1/sqrt(timestep))
            :param gamma: discount coefficient for future rewards
            :param verbose: logging or not logging
            :param learning: if True Q-values are updated after each step
            :param win: win reward
            :param draw: draw reward
            :param lose: lose reward
            :param not_finished: not_finished reward
            :rtype: BaseQAgent
            """
        super(BaseQAgent, self).__init__()
        self.q_values = {} if q_values is None else q_values
        self.verbose = verbose
        self.learning = learning
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.alpha = alpha
        self.gamma = gamma
        self.win = win
        self.draw = draw
        self.lose = lose
        self.not_finished = not_finished
        self.prev_state = None
        self.prev_action = None
        self.prev_q_val = 0
        self.count = 0
        self.side = None
        self.winner = VALUES.NOT_FINISHED

    def take_action(self, state):
        """ An epsilon greedy action selection method.

        With probability epsilon it takes a random exploration move,
        otherwise takes a greedy exploitation move.
        :param state
        :return: action
        """
        if self.epsilon_decay is not None:
            self.epsilon *= self.epsilon_decay
        if random.random() < self.epsilon:
            action = super(BaseQAgent, self).random_next_action(state)
            self.log('exploration move: {0}'.format(str(action)))
        else:
            action = self.greedy_next_action(state)
            self.log('exploitation move: {0}'.format(str(action)))
        return action

    def q_value(self, (state, action)):
        """ The Q-value Q(s,a) for a state, action pair

        For a given state, action pair (s, a) it returns the current Q-value Q(s,a) if exists,
        else it creates it using a basic reward value for state s.
        :param state, action:
        :return: q_value
        """
        hashable_state = self.represent_state(state)
        if not (hashable_state, action) in self.q_values:
            self.q_values[hashable_state, action] = self.reward(Game.game_state(state))
        return self.q_values[hashable_state, action]

    def update_q_values(self, state, value):
        """ Update method for Q-values in learning

        A TD agent has a general update formula of

            Q(s, a) := Q(s, a) + alpha * [reward + gamma * value - Q(s,a)]

        The agent keeps track of prev_state, prev_action and prev_q_value,
        and when next state (s') comes, it computes the reward for that
        and updates the Q-value of prev_state, prev_action according to the formula above.
        :param state: s' (the next state)
        :param value: value used in the update formula of the temporal difference learning
        :return:
        """
        if self.prev_state is not None and self.learning:
            reward = self.reward(Game.game_state(state))
            self.q_values[self.represent_state(self.prev_state), self.prev_action] += self.alpha * (
                reward + self.gamma * value - self.prev_q_val)

    def end_game(self, winner):
        """Clean up method for game end.

        It updates the Q-value of the last state (s), action (a) pair using the formula
            Q(s,a) = Q(s,a) + alpha * (reward - Q(s,a))
        and resets keep track variables (prev_state, prev_action, prev_q_value, winner)
        """
        reward = self.reward(winner)
        if self.learning:
            self.q_values[self.represent_state(self.prev_state), self.prev_action] += self.alpha * (
                reward - self.prev_q_val)
        self.log("the winner is {0}".format(winner))
        self.prev_state = None
        self.prev_action = None
        self.prev_q_val = 0
        self.winner = VALUES.NOT_FINISHED

    def greedy_next_action(self, state):
        """ Method for greedy action selection.

        This is an implementation of the greedy part of epsilon-greedy used in the take_action method.
        If there is no exploration then it exploits current knowledge
        by choosing an action a' that has a maximum Q(s',a') from state (s') (randomly if there is more)
        """
        max_val = float('-inf')
        if self.verbose:
            cells = []
        max_candidates = {}
        for i in range(3):
            for j in range(3):
                if state[i][j] == VALUES.EMPTY:
                    val = self.q_value((state, (i, j)))
                    if val >= max_val:
                        max_val = val
                        max_move = (i, j)
                        max_candidates[max_move] = val
                    if self.verbose:
                        cells.append('{0:.3f}'.format(val).center(6))
                elif self.verbose:
                    cells.append(state[i][j].center(6))
        if self.verbose:
            self.logger.info(BOARD.format(*cells))
        possible_actions = [k for k, v in max_candidates.items() if v == max_val]
        action = random.choice(possible_actions) if len(possible_actions) > 0 else None
        return action

    def reward(self, winner):
        """ A reward scheme for states.
        :param winner: the current winner of the game (NOT_FINISHED during game ... X, O or DRAW at game end
        :return: reward for game state
        """
        if winner == self.side:
            return self.win
        elif winner == VALUES.NOT_FINISHED:
            return self.not_finished
        elif winner == VALUES.DRAW:
            return self.draw
        else:
            return self.lose

    def print_q_values(self):
        """ A prettifier log method.

        A method for drawing actual game states
        with current Q-values of possible actions from that state
        e.g.:
        ----------------------------
        | 0.500  | 0.500  | 0.500  |
        |--------------------------|
        | 0.500  | 0.950  |   O    |
        |--------------------------|
        |   X    |   O    |   X    |
        ----------------------------
        """
        values = deepcopy(self.q_values)
        for (state, action) in values:
            cells = []
            for i in range(3):
                for j in range(3):
                    if state[i][j] == VALUES.EMPTY:
                        state[i][j] = self.side
                        cells.append(str(self.q_values[self.represent_state(state), action]).center(3))
                        state[i][j] = VALUES.EMPTY
                    else:
                        cells.append(NAMES[state[i][j]].center(3))
            self.logger.info(BOARD.format(*cells))

    def log(self, s):
        if self.verbose:
            self.logger.debug(s)

    def set_side(self, side):
        self.side = side

    def update_winner(self, winner):
        self.winner = winner

    def save_q_values_to(self, path):
        rows = []
        for (state, action), v in self.q_values.items():
            row = []
            for i in range(3):
                for j in range(3):
                    if state[i][j] == VALUES.EMPTY:
                        row.append(0)
                    elif state[i][j] == VALUES.X:
                        row.append(1)
                    else:
                        row.append(2)
            row.append(3 * action[0] + action[1])
            row.append(v)
            rows.append(row)
        with open(path, 'wb') as out:
            wr = csv.writer(out, quoting=csv.QUOTE_NONE)
            for row in rows:
                wr.writerow(row)

    def serialize_q_values(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.q_values, f)

    def deserialize_q_values(self, path):
        with open(path, 'rb') as f:
            q_vals = pickle.load(f)
            self.load_q_values(q_vals)

    def load_q_values(self, q_vals):
        if q_vals is not None:
            self.q_values = q_vals


class SarsaAgent(BaseQAgent):
    """ This agent implements SARSA learning.

    Sarsa learning is an on-policy TD control algorithm with update formula

        Q(s,a) = Q(s,a) + alpha * [reward(s') + gamma * Q(s',a') - Q(s,a)]

    where s' is the next state after taking action a in state s
    and a' is the action to take by agent's policy (e.g. epsilon greedy)

    more information @ http://webdocs.cs.ualberta.ca/~sutton/book/ebook/node64.html
    """
    def __init__(self,
                 q_values=None,
                 alpha=0.1,
                 epsilon=0.1,
                 epsilon_decay=None,
                 gamma=0.9,
                 verbose=False,
                 learning=True,
                 win=1.0,
                 draw=0.0,
                 lose=-1.0,
                 not_finished=0.0):
        """
            :param q_values: a dictionary holding Q(s,a) values
            :param alpha: step size parameter in the TD update formula
            :param epsilon: the exploration probability of epsilon-greedy(ness)
            :param epsilon_decay: decay factor for epsilon
            :param gamma: discount coefficient for future rewards
            :param verbose: logging or not logging
            :param learning: if True Q-values are updated after each step
            :param win: win reward
            :param draw: draw reward
            :param lose: lose reward
            :param not_finished: not_finished reward
            :rtype: SarsaAgent
        """
        super(SarsaAgent, self).__init__(q_values=q_values,
                                         alpha=alpha,
                                         epsilon=epsilon,
                                         epsilon_decay=epsilon_decay,
                                         gamma=gamma,
                                         verbose=verbose,
                                         learning=learning,
                                         win=win,
                                         draw=draw,
                                         lose=lose,
                                         not_finished=not_finished)

    def take_action(self, state):
        """Override method for SARSA agent for taking action in a given state.

        It is epsilon-greedy, i.e. with probability epsilon we choose a random action,
        otherwise we choose a greedy action.
        if learning enabled we update the Q-value of prev_state (s), prev_action (a)
        with the Q-value of state (s'), and the generated action (a') according to the formula

            Q(s,a) = Q(s,a) + alpha * [reward(s') + gamma * Q(s',a') - Q(s,a)]

        :param state: the next action s'
        :return: epsilon-greedy action a' from state s'
        """
        action = super(SarsaAgent, self).take_action(state)
        if self.learning:
            self.update_q_values(state, self.q_value((state, action)))
            self.prev_state = state
            self.prev_action = action
            self.prev_q_val = self.q_values[self.represent_state(self.prev_state), self.prev_action]
            self.log("size of q_values {0}\nprev state {1}\nprev action {2}\nprev q-val {3}"
                     .format(len(self.q_values), self.prev_state, self.prev_action, self.prev_q_val))
        return action


class QLearningAgent(BaseQAgent):
    """This agent implements the Q-learning algorithm.

    It is an off-policy TD control algorithm with update formula

        Q(s,a) = Q(s,a) + alpha * [reward(s') + gamma * max(Q(s',a_)) - Q(s,a)]

    where s' is the next state after taking action a in state s
    and max(Q(s',a_)) is the max of all the Q-values having state s'.

    more information @ http://webdocs.cs.ualberta.ca/~sutton/book/ebook/node65.html
    """
    def __init__(self,
                 q_values=None,
                 alpha=0.1,
                 epsilon=0.1,
                 epsilon_decay=None,
                 gamma=0.9,
                 verbose=False,
                 learning=True,
                 win=1.0,
                 draw=0.0,
                 lose=-1.0,
                 not_finished=0.0):
        """
            :param q_values: a dictionary holding Q(s,a) values
            :param alpha: step size parameter in the TD update formula
            :param epsilon: the exploration probability of epsilon-greedy(ness)
            :param epsilon_decay: decay factor for epsilon
            :param gamma: discount coefficient for future rewards
            :param verbose: logging or not logging
            :param learning: if True Q-values are updated after each step
            :param win: win reward
            :param draw: draw reward
            :param lose: lose reward
            :param not_finished: not_finished reward
            :rtype: QLearningAgent
        """
        super(QLearningAgent, self).__init__(q_values=q_values,
                                             alpha=alpha,
                                             epsilon=epsilon,
                                             epsilon_decay=epsilon_decay,
                                             gamma=gamma,
                                             verbose=verbose,
                                             learning=learning,
                                             win=win,
                                             draw=draw,
                                             lose=lose,
                                             not_finished=not_finished)
        self.max_action_values = {}

    def take_action(self, state):

        """Override method for Q-learning agent for taking action in a given state.

        It is epsilon-greedy, i.e. with probability epsilon we choose a random action,
        otherwise we choose a greedy action.
        If learning is enabled we update the Q-value of prev_state (s), prev_action (a)
        with the max Q-value having state (s') according to the formula

            Q(s,a) = Q(s,a) + alpha * [reward(s') + gamma * max(Q(s',a_)) - Q(s,a)]

        for fast lookup, we keep track of and update current maximum Q-values for each encountered state

        :param state: the next action s'
        :return: epsilon-greedy action a' from state s'
        """
        action = super(QLearningAgent, self).take_action(state)
        hashable_state = self.represent_state(state)
        if self.learning:
            max_q_val = 0 if not hashable_state in self.max_action_values else self.max_action_values[hashable_state]
            self.update_q_values(state, max_q_val)
            self.prev_state = state
            self.prev_action = action
            self.prev_q_val = self.q_value((state, action))
            self.log("size of q_values {0}\nprev state {1}\nprev action {2}\nprev q-val {3}"
                     .format(len(self.q_values), self.prev_state, self.prev_action, self.prev_q_val))
        q_val = self.q_value((state, action))
        if hashable_state in self.max_action_values:
            if q_val > self.max_action_values[hashable_state]:
                self.max_action_values[hashable_state] = q_val
        else:
            self.max_action_values[hashable_state] = q_val
        return action