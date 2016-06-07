from __future__ import division
#
from random import randrange, seed
#
seed(1)
#
FLOW_LB, FLOW_UB = 1, None 
REWARD_LB, REWARD_UB = 1, 100

def generate_problem(num_agents, num_zones, time_horizon):
    global FLOW_UB
    FLOW_UB = int(num_agents * 1.5)
    #
    fl = flow_generation(num_agents, num_zones, time_horizon)
    Re, Co = reward_cost_generation(time_horizon, num_zones)
    d0 = [0] * num_zones
    for _ in xrange(num_agents):
        d0[randrange(num_zones)] += 1
    #
    return fl, Re, Co, d0  

def flow_generation(num_agents, num_zones, time_horizon):
    #
    # t_ij: the first index represents time
    #        the second represents row
    #        the third represents column
    #
    t_ij = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    for t in xrange(time_horizon):
        for i in xrange(num_zones):
            for j in xrange(num_zones):
                t_ij[t][i][j] = randrange(FLOW_LB, FLOW_UB)
    return t_ij

def reward_cost_generation(time_horizon, num_zones):
    Re = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    Co = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    for t in xrange(time_horizon):
        for i in xrange(num_zones):
            for j in xrange(num_zones):
                reward = randrange(REWARD_LB, REWARD_UB)
                while reward == REWARD_LB:
                    reward = randrange(REWARD_LB, REWARD_UB)
                cost = randrange(reward)
                Re[t][i][j], Co[t][i][j] = reward, cost
    return Re, Co
    
if __name__ == '__main__':
    num_agents, num_zones = 10, 3
    time_horizon = 5 
    generate_problem(num_agents, num_zones, time_horizon)