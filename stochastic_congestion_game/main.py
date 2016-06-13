from __future__ import division
#
from problems import generate_problem
from ddap import define_DDAP
from algorithms import FP_SAP
#
from file_handling import init_inputs_fn
#
def run():
    #
    # Input generation
    #
    num_agents, num_zones, H = 10, 3, 3; save_init_inputs(num_agents, num_zones, H)
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
#     save_problem_policy(num_agents, num_zones, H, fl, Re, Co, d0, _pi)

def save_init_inputs(num_agents, num_zones, H):
    with open(init_inputs_fn, 'w') as f:
        f.write('Initial inputs ---------------------------------------------\n')
        f.write('Number of agents: %d, Number of zones: %d, Time horizon: %d\n' % (num_agents, num_zones, H))

if __name__ == '__main__':
    run()
    
