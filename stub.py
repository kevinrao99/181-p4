# Imports.
import numpy as np
import numpy.random as npr
import pygame as pg

from SwingyMonkey import SwingyMonkey


class Learner(object):
    '''
    This agent jumps randomly.
    '''

    def __init__(self):
        # treetop 30, monkeytop 40, treedist 40, vel 70, gravity 4, action 2
        self.matrix = [[[[[[[0] for i in range(2)] for j in range(4)] for k in range(70)] for l in range(40)] for m in range(40)] for n in range(30)]
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.lr = 0.1
        self.eps = 0.1

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def action_callback(self, state):
        '''
        Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.
        '''

        # You might do some learning here based on the current state and the last state.

        # You'll need to select and action and return it.
        # Return 0 to swing and 1 to jump.

        treetop = state['tree']['top'] // 10
        monkeytop = state['monkey']['top'] // 10
        treedist = state['tree']['dist'] // 10
        vel = state['monkey']['vel']
        gravity = 2

        old_treetop = self.last_state['tree']['top'] // 10
        old_monkeytop = self.last_state['monkey']['top'] // 10
        old_treedist = self.last_state['tree']['dist'] // 10
        old_vel = self.last_state['monkey']['vel']

        mymax = max(self.matrix[treetop][monkeytop][treedist][vel][gravity][0], self.matrix[treetop][monkeytop][treedist][vel][gravity][1])

        self.matrix[old_treetop][old_monkeytop][old_treedist][old_vel][gravity][int(self.last_action)] *= (1 - self.lr)
        self.matrix[old_treetop][old_monkeytop][old_treedist][old_vel][gravity][int(self.last_action)] += self.lr * (self.last_reward + mymax)

        if math.random() > self.eps:
            new_action = self.matrix[treetop][monkeytop][treedist][vel][gravity][0] < self.matrix[treetop][monkeytop][treedist][vel][gravity][1]
        else:
            new_action = math.random() > 0.5
        new_state  = state

        self.last_action = new_action
        self.last_state  = new_state

        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''

        self.last_reward = reward


def run_games(learner, hist, iters = 100, t_len = 100):
    '''
    Driver function to simulate learning by having the agent play a sequence of games.
    '''
    for ii in range(iters):
        # Make a new monkey object.
        swing = SwingyMonkey(sound=False,                  # Don't play sounds.
                             text="Epoch %d" % (ii),       # Display the epoch on screen.
                             tick_length = t_len,          # Make game ticks super fast.
                             action_callback=learner.action_callback,
                             reward_callback=learner.reward_callback)

        # Loop until you hit something.
        while swing.game_loop():
            pass
        
        # Save score history.
        hist.append(swing.score)

        # Reset the state of the learner.
        learner.reset()
    pg.quit()
    return


if __name__ == '__main__':

	# Select agent.
	agent = Learner()

	# Empty list to save history.
	hist = []

	# Run games. 
	run_games(agent, hist, 20, 10)

	# Save history. 
	np.save('hist',np.array(hist))


