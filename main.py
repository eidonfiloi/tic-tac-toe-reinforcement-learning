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

""" This is a main file for running a demo experiment with trained agents.

Load serialized q-values and save them to a csv file
by un-commenting/using the lines containing deserialize_q_values() and save_q_values_to().
The csv schema is:

        2,2,0,0,1,0,1,0,0,8,0.49

where the first 9 columns are board cell states with value 0: empty, 1: X, 2: O
10th column is cell index of the action
11th column is the q-value of the state, action pair
Indices for cells(actions) are:
        -------------------
        |  0  |  1  |  2  |
        |-----------------|
        |  3  |  4  |  5  |
        |-----------------|
        |  6  |  7  |  8  |
        -------------------
"""

import matplotlib.pyplot as plt
from agent import *
from experiments import calculate_winner_frequency_dict


_LOGGER = logging.getLogger(__name__)


def run_trained_agents(agent1, agent2, num_episodes=100):
    """ Helper method for demo experiment.

    This runs games between
    two agents and plots performance results
    :param agent1: player1
    :param agent2: player2
    :param num_episodes: number of games in an episode
    :return:
    """

    colors = {'agent1_x_win': 'r',
              'agent2_o_win': 'b',
              'agent1_x_agent2_o_draw': 'g',
              'agent2_x_win': 'c',
              'agent1_o_win': 'm',
              'agent2_x_agent1_o_draw': 'y'}

    performance = {'agent1_x_win': [],
                   'agent2_o_win': [],
                   'agent1_x_agent2_o_draw': [],
                   'agent2_x_win': [],
                   'agent1_o_win': [],
                   'agent2_x_agent1_o_draw': []}

    game_counts = range(num_episodes)

    for i in game_counts:
        _LOGGER.info('Episode {0}'.format(i))
        freq_dict = calculate_winner_frequency_dict(agent1, agent2, 100)
        for k, v in freq_dict.items():
            performance[k].append(v)

    for k, v in performance.items():
            plt.plot(game_counts, performance[k], label=k, color=colors[k])

    plt.xlabel('Games')
    plt.ylabel('Probability')
    plt.title('{0} vs. {1}'.format(str(agent1), str(agent2)))
    plt.legend(loc=4)
    plt.show()


def run_agent_against_human(agent):
    """ Helper method for demo experiment.

    This runs games between
    an agent and a human player.
    :param agent: non-human player
    :return:
    """
    while True:
        try:
            human_player = HumanAgent()
            if random.random() < 0.5:
                player_x = agent
                player_o = human_player
            else:
                player_x = human_player
                player_o = agent
            game = Game(player_x=player_x, player_o=player_o)
            winner = game.play()
            Game.print_board(game.board)
            _LOGGER.info('winner is {0}'.format(winner))
        except (KeyboardInterrupt, SystemExit):
            _LOGGER.info('exit')


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # initializing agents
    player_random = RandomAgent()
    player_win_block_random = WinBlockingRandomAgent()
    player_sarsa = SarsaAgent(learning=False, epsilon=0.0)
    player_q = QLearningAgent(learning=False, epsilon=0.0)

    try:
        _LOGGER.info('load q-values of trained agent')
        player_sarsa.deserialize_q_values(
            'trained_agents/SarsaAgent_in_SarsaAgent_vs_SarsaAgent_ep_500_g_500_itself_pre_trained_3.pickle')
    except pickle.PickleError as e:
        player_sarsa.learning = True
        _LOGGER.error(e.message)

    # uncomment if want to save q-values to csv
    #player_sarsa.save_q_values_to('q_values.csv')

    # run a demo experiment with 50 episodes each containing 100 games
    _LOGGER.info('running experiments between Sarsa and a win blocking Random agent...')
    run_trained_agents(player_sarsa, player_win_block_random, 50)



