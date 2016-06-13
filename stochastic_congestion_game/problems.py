from __future__ import division
#
from random import randrange, seed
from prettytable import PrettyTable
#
from file_handling import flow_fn, revenue_fn, cost_fn, dist_fn
#
#
seed(1)
#
FLOW_LB, FLOW_UB = 1, None 
REWARD_LB, REWARD_UB = 1, 100
#
RESULT_SAVE = True

def generate_problem(num_agents, num_zones, time_horizon):
    global FLOW_UB
    FLOW_UB = int(num_agents * 1.5)
    #
    fl = flow_generation(num_agents, num_zones, time_horizon)
    Re, Co = reward_cost_generation(time_horizon, num_zones)
    d0 = distribution_generation(num_agents, num_zones)
    #
    return fl, Re, Co, d0  

def distribution_generation(num_agents, num_zones):
    d0 = [0] * num_zones
    for _ in xrange(num_agents):
        d0[randrange(num_zones)] += 1
    if RESULT_SAVE:
        _table = PrettyTable([z for z in xrange(num_zones)])
        _table.add_row([d0[z] for z in xrange(num_zones)])
        with open(dist_fn, 'w') as f:
            f.write('----------------------------------- Initial distribution\n')
            f.write('%s\n' % _table.get_string())
    return d0
    
def flow_generation(num_agents, num_zones, time_horizon):
    #
    # fl: the first index represents time
    #        the second represents row
    #        the third represents column
    #
    fl = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    for t in xrange(time_horizon):
        for i in xrange(num_zones):
            for j in xrange(num_zones):
                fl[t][i][j] = randrange(FLOW_LB, FLOW_UB)
    if RESULT_SAVE:
        with open(flow_fn, 'w') as f:
            f.write('Flow description -----------------------------------\n')
            problem_saving_table_representation(f, fl)
    return fl

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
    if RESULT_SAVE:
        with open(revenue_fn, 'w') as f:
            f.write('Revenue description -----------------------------------\n')
            problem_saving_table_representation(f, Re)
        with open(cost_fn, 'w') as f:
            f.write('Cost description -----------------------------------\n')
            problem_saving_table_representation(f, Co)
            f.write('----------------------------------- \n')    
    return Re, Co

def problem_saving_table_representation(f, _data):
    H, num_zones = len(_data), len(_data[0])
    f.write('Column represents FROM and Row represents TO\n')
    for t in xrange(H):
        f.write('t = %d,\n' % t)
        _table = PrettyTable([''] + [TO for TO in xrange(num_zones)])
        for FROM in xrange(num_zones):
            _table.add_row([FROM] + [_data[t][FROM][TO] for TO in xrange(num_zones)])
        f.write('%s\n' % _table.get_string())
    
if __name__ == '__main__':
    num_agents, num_zones = 10, 3
    time_horizon = 5 
    generate_problem(num_agents, num_zones, time_horizon)