from __future__ import division
#
from problems import generate_problem
from ddap import define_DDAP
from algorithms import FP_SAP 
#
def run():
    #
    # Input generation
    #
    num_agents, num_zones, H = 10, 3, 5
    fl, Re, Co, d0 = generate_problem(num_agents, num_zones, H)
    #
    # Define Decision model for Agent Populations (DDAP)
    #
    PHI, R = define_DDAP(fl, Re, Co)
    #
    # Run Fictitious Play for Symmetric Agent Populations
    #
    _pi = FP_SAP(range(num_agents), range(num_zones), range(num_zones), PHI, R, H, d0)
    print _pi

if __name__ == '__main__':
    run()
    
