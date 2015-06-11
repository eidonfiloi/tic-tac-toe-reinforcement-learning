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

"""This file contains methods for running experiments between agents and plotting their performance."""

from agent import *
import matplotlib.pyplot as plt
from math import sqrt


def calculate_average_reward(agent1, agent2, num_games, epsilon1=0.1, epsilon2=0.1, win=1.0, draw=0.0, lose=-1.0):
    """ A helper method for experiments.

    This method runs games between two agents, both agents playing both sides
    and returns the average rewards they got.
    :param agent1: player1
    :param agent2: player2
    :param num_games: how many games to play in an episode
    :param epsilon1: exploration rate for player1
    :param epsilon2: exploration rate for player2
    :param win: win reward
    :param draw: draw reward
    :param lose: loss reward
    :return: dictionary containing average rewards for both players
    """
    agent1.epsilon = epsilon1
    agent2.epsilon = epsilon2
    reward_map = {'agent1_x': 0,
                  'agent2_o': 0,
                  'agent1_o': 0,
                  'agent2_x': 0}
    for _ in range(num_games):
        game1 = Game(player_x=agent1, player_o=agent2)
        winner1 = game1.play()
        if winner1 == VALUES.X:
            reward_map['agent1_x'] += win / num_games
            reward_map['agent2_o'] += lose / num_games
        elif winner1 == VALUES.O:
            reward_map['agent2_o'] += win / num_games
            reward_map['agent1_x'] += lose / num_games
        else:
            reward_map['agent1_x'] += draw / num_games
            reward_map['agent2_o'] += draw / num_games
    for _ in range(num_games):
        game2 = Game(player_x=agent2, player_o=agent1)
        winner2 = game2.play()
        if winner2 == VALUES.X:
            reward_map['agent2_x'] += win / num_games
            reward_map['agent1_o'] += lose / num_games
        elif winner2 == VALUES.O:
            reward_map['agent1_o'] += win / num_games
            reward_map['agent2_x'] += lose / num_games
        else:
            reward_map['agent2_x'] += draw / num_games
            reward_map['agent1_o'] += draw / num_games
    return reward_map


def calculate_winner_frequency_dict(agent1, agent2, num_games):
    """A helper method for experiments.

    This method runs games between two agents, both agents playing both sides
    and returns the probability of win-draw-lose for both players in both side.
    :param agent1: player1
    :param agent2: player2
    :param num_games: mumber of games in an episode
    :return: dictionary of win-draw-lose frequencies for both players in both side
    """
    winner_counts = {'agent1_x_win': 0,
                     'agent2_o_win': 0,
                     'agent1_x_agent2_o_draw': 0,
                     'agent2_x_win': 0,
                     'agent1_o_win': 0,
                     'agent2_x_agent1_o_draw': 0}
    for _ in range(num_games):
        game1 = Game(player_x=agent1, player_o=agent2)
        winner1 = game1.play()
        if winner1 == VALUES.X:
            winner_counts['agent1_x_win'] += 1.0 / num_games
        elif winner1 == VALUES.O:
            winner_counts['agent2_o_win'] += 1.0 / num_games
        else:
            winner_counts['agent1_x_agent2_o_draw'] += 1.0 / num_games
    for _ in range(num_games):
        game2 = Game(player_x=agent2, player_o=agent1)
        winner2 = game2.play()
        if winner2 == VALUES.X:
            winner_counts['agent2_x_win'] += 1.0 / num_games
        elif winner2 == VALUES.O:
            winner_counts['agent1_o_win'] += 1.0 / num_games
        else:
            winner_counts['agent2_x_agent1_o_draw'] += 1.0 / num_games
    return winner_counts

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    # set reward scheme
    WIN = 1.0
    DRAW = 0.0
    LOSE = -1.0
    NOT_FINISHED = 0.0

    # initialize different players
    player_random = RandomAgent()
    player_winblock_random = WinBlockingRandomAgent()
    player_sarsa = SarsaAgent(verbose=True,
                              epsilon=0.1,
                              win=WIN,
                              draw=DRAW,
                              lose=LOSE,
                              not_finished=NOT_FINISHED)
    player_q = QLearningAgent(verbose=True,
                              epsilon=0.1,
                              win=WIN,
                              draw=DRAW,
                              lose=LOSE,
                              not_finished=NOT_FINISHED)

    # load serialized Q values if necessary
    player_sarsa.deserialize_q_values(
        'trained_agents/SarsaAgent_in_SarsaAgent_vs_SarsaAgent_ep_500_g_500_itself_pre_trained_3.pickle')

    player_q.deserialize_q_values(
        'trained_agents/QLearningAgent_in_QLearningAgent_vs_QLearningAgent_ep_500_g_500_itself_pre_trained_3.pickle')

    # set player_x and player_o
    player_x = player_q
    player_o = player_sarsa

    """
    set if q-values should be serialized after experiment
    and/or performance plots should be saved
    with unique name ending
    """

    serialize_x = False
    serialize_o = False
    save_image = False
    name_append = 'against_pre_trained_3'

    # set plot colors and dict's holding data for plot
    colors_reward = {'agent1_x': 'r',
                     'agent2_o': 'b',
                     'agent1_o': 'g',
                     'agent2_x': 'c'}

    colors_prob = {'agent1_x_win': 'r',
                   'agent2_o_win': 'b',
                   'agent1_x_agent2_o_draw': 'g',
                   'agent2_x_win': 'c',
                   'agent1_o_win': 'm',
                   'agent2_x_agent1_o_draw': 'y'}


    performance_reward = {'agent1_x': [],
                          'agent2_o': [],
                          'agent1_o': [],
                          'agent2_x': []}

    performance_prob = {'agent1_x_win': [],
                        'agent2_o_win': [],
                        'agent1_x_agent2_o_draw': [],
                        'agent2_x_win': [],
                        'agent1_o_win': [],
                        'agent2_x_agent1_o_draw': []}

    """
    set number of episodes and number of games in each episode
    run all episodes
    plot results
    save plot images and serialize q-values
    """
    num_episodes = 300
    num_games_in_episodes = 200

    episode_counts = range(num_episodes)
    for i in range(num_episodes):
            print 'Episode: {0}'.format(i)
            epsilon_x = 0.1 if i < 350 else 0.1 / sqrt(i/100)
            rewards = calculate_average_reward(agent1=player_x,
                                               agent2=player_o,
                                               num_games=num_games_in_episodes,
                                               epsilon1=epsilon_x)
            for k, v in rewards.items():
                performance_reward[k].append(v)

    for k, v in performance_reward.items():
            plt.plot(episode_counts, performance_reward[k], label=k, color=colors_reward[k])

    plt.xlabel('Episodes')
    plt.ylabel('Reward')
    plt.title('{0} vs. {1}'.format(str(player_x), str(player_o)))
    plt.legend(loc=4)

    if save_image:
        plt.savefig('plots/RPE_{0}_vs_{1}_ep_{2}_g_{3}_{4}.png'
                    .format(str(player_x), str(player_o), num_episodes, num_games_in_episodes, name_append))

    if serialize_x:
        if hasattr(player_x, 'serialize_q_values'):
            player_x.serialize_q_values(
                'trained_agents/{0}_in_{0}_vs_{1}_ep_{2}_g_{3}_{4}.pickle'
                .format(str(player_x), str(player_o), num_episodes, num_games_in_episodes, name_append))
    if serialize_o:
        if hasattr(player_o, 'serialize_q_values'):
            player_o.serialize_q_values(
                'trained_agents/{1}_in_{0}_vs_{1}_ep_{2}_g_{3}_{4}.pickle'
                .format(str(player_x), str(player_o), num_episodes, num_games_in_episodes, name_append))

    plt.show()



