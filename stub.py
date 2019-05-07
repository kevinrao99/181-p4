# Imports.
import numpy as np
import numpy.random as npr
import pygame as pg
import random
import matplotlib.pyplot as plt

from SwingyMonkey import SwingyMonkey


class Learner(object):
    '''
    This agent jumps randomly.
    '''

    def __init__(self):
        # treetop 30, monkeytop 40, vel 70, self.gravity 4, action 2
        print "instantiating stuff..."
        self.matrix = [[[[[0 for i in range(2)] for j in range(2)] for k in range(70)] for m in range(42)] for n in range(42)]
        print "done with matrix"
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.checkedyet = False
        self.lr = 1.0
        self.eps = 0.5
        self.treetopscale, self.monkeytopscale, self.velscale = 30*1, 40*1, 7*1
        self.gravity = 0
        self.discount = 1

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.gravity = 0
        self.checkedyet = False

    def action_callback(self, state):
        '''
        Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.
        '''

        # You might do some learning here based on the current state and the last state.

        # You'll need to select and action and return it.
        # Return 0 to swing and 1 to jump.

        if self.eps > 0.001:
            self.eps *= 0.9
        if self.lr > 0.1:
            self.lr *= 0.99

        treetop = state['tree']['top'] // self.treetopscale
        monkeytop = state['monkey']['top'] // self.monkeytopscale
        vel = state['monkey']['vel'] // self.velscale

        curr = self.matrix[treetop][monkeytop][vel][self.gravity]
        mymax = max(curr[0], curr[1])

        if self.last_state:
            old_treetop = self.last_state['tree']['top'] // self.treetopscale
            old_monkeytop = self.last_state['monkey']['top'] // self.monkeytopscale
            old_vel = self.last_state['monkey']['vel'] // self.velscale
            if old_vel > vel and not self.checkedyet:
                self.gravity = 1 if old_vel - vel - 1 != 0 else 0
                self.checkedyet = True

            last = self.matrix[old_treetop][old_monkeytop][old_vel][self.gravity]
            df = last[self.last_action] - (self.last_reward + self.discount * mymax)
            self.matrix[old_treetop][old_monkeytop][old_vel][self.gravity][self.last_action] -= self.lr * df

        if state['monkey']['top'] > state['tree']['top']:
            self.matrix[treetop][monkeytop][vel][self.gravity][0] += 0.5
        elif state['monkey']['bot'] < state['tree']['bot']:
            self.matrix[treetop][monkeytop][vel][self.gravity][1] += 0.5

        if random.random() > self.eps:
            new_action = int(curr[0] < curr[1])
        else:
            new_action = int(random.random() > 0.8)
        
        new_state  = state

        self.last_action = new_action
        self.last_state  = new_state

        # print "Action:", new_action
        return new_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''

        self.last_reward = reward


def run_games(learner, hist, iters = 100, t_len = 100):
    '''
    Driver function to simulate learning by having the agent play a sequence of games.
    '''
    for ii in range(iters):
        # Make a new monkey object.
        print "starting", ii
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
    run_games(agent, hist, 200, 1)

    print hist

    # Save history. 
    np.save('hist',np.array(hist))

    plt.scatter(range(len(hist)), hist)
    plt.xlabel("Epoch number")
    plt.title("Score vs. Epochs")
    plt.ylabel("Score")
    plt.show()
