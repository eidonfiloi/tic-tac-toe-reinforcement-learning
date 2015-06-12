# tic-tac-toe-reinforcement-learning

This project contains a simple tic-tac-toe game implementation with classical settings (3x3 board with player X and O etc.). 

I wanted to keep the game implementation as simple as possible and tried to concentrate more on the agents. There are surely places of improvements at how to represent the game and the play (I made some thoughts about base 3 number representation, or as binary numbers etc.), but I stayed at the 3x3 matrix representation with "enum" values. I implemented SARSA and Q-learning and other (mostly variants of random) agents as test opponents. I tried to run many experiments (mostly 1500 episodes with 1000 game in each). I trained both a Sarsa agent and a Q-learning agent (with reward scheme win=1, draw=0, loss=-1) against a simple random agent, then against a win blocking random agent, then against themselves and then against each other.

The main.py contains a demo experiment that runs a trained Sarsa agent against the win blocking random agent. As one can see, the trained agent does not lose a game. In the trained_agents directory I included many pickled q-value dictionaries that can be loaded in main.py too. I saved two q-value dicts as csv files (format is described in main.py) in order to be able to load them in other environments as well. 

In the plots directory one can find plots showing average reward per episodes in various experiments. In the root directory I included 2 plots showing win-draw-lose probabilities in demo experiments.
