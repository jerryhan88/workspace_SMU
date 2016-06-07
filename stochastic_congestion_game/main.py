from __future__ import division
#
from problems import generate_problem
from ddap import define_DDAP
from algorithms import FP_SAP
#
from prettytable import PrettyTable 
#
saving_fn = './result.txt'
#
def run():
    #
    # Input generation
    #
    num_agents, num_zones, H = 10, 3, 3
    fl, Re, Co, d0 = generate_problem(num_agents, num_zones, H)
    #
    # Define Decision model for Agent Populations (DDAP)
    #
    PHI, R = define_DDAP(fl, Re, Co)
    #
    # Run Fictitious Play for Symmetric Agent Populations
    #
    _pi = FP_SAP(range(num_agents), range(num_zones), range(num_zones), PHI, R, H, d0)
    #
    # Display a problem and algorithm's result
    #
    save_problem_policy(num_agents, num_zones, H, fl, Re, Co, d0, _pi)
    
def save_problem_policy(num_agents, num_zones, H, fl, Re, Co, d0, _pi):
    with open(saving_fn, 'w') as f:
        f.write('Problem description ---------------------------------------------\n')
        f.write('Number of agents: %d, Number of zones: %d, Time horizon: %d\n' % (num_agents, num_zones, H))
        f.write('----------------------------------- Flow description\n')
        problem_table_representation(f, H, num_zones, fl)
        f.write('----------------------------------- Revenue description\n')    
        problem_table_representation(f, H, num_zones, Re)
        f.write('----------------------------------- Cost description\n')    
        problem_table_representation(f, H, num_zones, Co)
        f.write('----------------------------------- Initial distribution\n')
        _table = PrettyTable([z for z in xrange(num_zones)])
        _table.add_row([d0[z] for z in xrange(num_zones)])
        f.write('%s\n' % _table.get_string())
        #
        f.write('Policy ---------------------------------------------------\n')
        policy_table_representation(f, H, num_zones, _pi)
        

def problem_table_representation(f, H, num_zones, _data):
    f.write('Column represents FROM and Row represents TO\n')
    for t in xrange(H):
        f.write('t = %d,\n' % t)
        _table = PrettyTable([''] + [TO for TO in xrange(num_zones)])
        for FROM in xrange(num_zones):
            _table.add_row([FROM] + [_data[t][FROM][TO] for TO in xrange(num_zones)])
        f.write('%s\n' % _table.get_string())

def policy_table_representation(f, H, num_zones, _pi):
    f.write('Column represents state and Row represents action\n')
    for t in xrange(H):
        f.write('t = %d,\n' % t)
        _table = PrettyTable([''] + [a for a in xrange(num_zones)])
        for s in xrange(num_zones):
            _table.add_row([s] + [_pi[t, s, a] for a in xrange(num_zones)])
        f.write('%s\n' % _table.get_string())

if __name__ == '__main__':
    run()
    
