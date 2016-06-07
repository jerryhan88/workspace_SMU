from __future__ import division
#
from random import randrange, seed
#
seed(1)
#
def generate_problem(num_agents, num_zones, time_horizon):
    #
    # ASSUMETION
    #  Ignore a case when i == j
    #
    fl_t = random_generation(time_horizon, num_zones)
    Re_t = random_generation(time_horizon, num_zones)
    Co_t = random_generation(time_horizon, num_zones)
    d0 = [0] * num_zones
    for _ in xrange(num_agents):
        d0[randrange(num_zones)] += 1
    #
    return fl_t, Re_t, Co_t, d0  

def random_generation(time_horizon, num_zones):
    #
    # t_ij: the first index represents time
    #        the second represents row
    #        the third represents column
    #
    t_ij = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    for t in xrange(time_horizon):
        for i in xrange(num_zones):
            for j in xrange(num_zones):
                if i == j: continue
                t_ij[t][i][j] = randrange(1, 10)
    return t_ij

if __name__ == '__main__':
    num_agents, num_zones = 10, 3
    time_horizon = 5 
    generate_problem(num_agents, num_zones, time_horizon)