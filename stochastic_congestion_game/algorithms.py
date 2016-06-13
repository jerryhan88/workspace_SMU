from __future__ import division
#
from gurobipy import *
from random import random
from prettytable import PrettyTable
#
from file_handling import policy_prefix, x_prefix, dist_prefix, lp_prefix
#
P, S, A, PHI, R, H, d0 = None, None, None, None, None, None, None
#
GAMMA = 0.99
#
RESULT_SAVE = True
#
def FP_SAP(_P, _S, _A, _PHI, _R, _H, _d0):
    #
    # Initialize algorithm inputs
    #
    global P, S, A, PHI, R, H, d0
    P, S, A, PHI, R, H, d0 = _P, _S, _A, _PHI, _R, _H, _d0
    #
    # Run the algorithm 
    #
    pi0 = GET_RANDOM_POLICY()
    i = 0
    x = {k:0 for k in pi0.keys()}
    while True:
        d = GET_DIST(pi0, i)
        _x = SOLVE_MDP(d, i)
        x = update_x(i, x, _x)
        pi1 = update_pi(x, i)
        i += 1
        if pi0 == pi1:
            print 'Break?'
            break
        else:
            print '...ing'
            print i
            pi0 = pi1
    return pi0

def policy_saving(_pi, postfix):
    with open('%s%s.txt' % (policy_prefix, postfix), 'w') as f:
        f.write('Policy -----------------------------------\n')
        f.write('Column represents state and Row represents action\n')
        for t in xrange(H):
            f.write('t = %d,\n' % t)
            _table = PrettyTable([''] + [a for a in A])
            for s in S:
                _table.add_row([s] + [_pi[t, s, a] for a in A])
            f.write('%s\n' % _table.get_string())

def update_pi(x, i):
    pi1 = {}
    for t in xrange(H):
        for s in S:
            sum_a = sum(x[t, s, a] for a in A)
            for a in A:
                pi1[t, s, a] = x[t, s, a] / sum_a
    if RESULT_SAVE:
        policy_saving(pi1, i)
    return pi1

def update_x(i, x, _x):
    for t in xrange(H):
        for s in S:
            for a in A:
                x[t, s, a] = (i * x[t, s, a] + _x[t, s, a]) / (i + 1)
    if RESULT_SAVE:
        with open('%s%d.txt' % (x_prefix, i), 'w') as f:
            f.write('x -----------------------------------\n')
            f.write('Column represents state and Row represents action\n')
            for t in xrange(H):
                f.write('t = %d,\n' % t)
                _table = PrettyTable([''] + [a for a in A])
                for s in S:
                    _table.add_row([s] + [x[t, s, a] for a in A])
                f.write('%s\n' % _table.get_string())
    return x

def GET_RANDOM_POLICY():
    _pi = {}
    for t in xrange(H):
        for s in S:
            rates = [random() for _ in A]
            for a in A:
                _pi[t, s, a] = rates[a] / sum(rates) 
    if RESULT_SAVE:
        policy_saving(_pi, 'init')
    return _pi

def GET_DIST(_pi, i):
    _delta0 = [d0[s] / len(P) for s in S]
    #
    d = [d0]
    t = 0
    while t < H - 1:
        _delta1 = []
        for s0 in S:
            rate = 0
            for s1 in S:
                rate += _delta0[s1] * sum(_pi[t, s1, a] * PHI(t, d[-1], s1, a, s0) for a in A) 
            _delta1.append(rate)
        _d1 = [_delta1[s] * len(P) for s in S]
        #
        _delta0 = _delta1[:]
        d.append(_d1)
        t += 1
    if RESULT_SAVE:
        _table = PrettyTable([s for s in S])
        _table.add_row([d0[s] for s in S])
        with open('%s%d.txt' % (dist_prefix, i), 'w') as f:
            f.write('----------------------------------- Initial distribution\n')
            f.write('%s\n' % _table.get_string())
    return d

def SOLVE_MDP(d, i):
    def _delta(t, s):
        return d[t][s] / sum(d[t])
    # Create optimization model
    m = Model('SOLVE_MDP')
     
    # Create variables
    x = {}
    for t in xrange(H):
        for s in S:
            for a in A:
                x[t, s, a] = m.addVar(name='x_%d_(%d,%d)' % (t, s, a))
    m.update()
    # Constraints
    for t in xrange(H):
        for s1 in S:
            m.addConstr(quicksum(x[t, s1, a] for a in A)
             - GAMMA * quicksum(x[t, s0, a] * PHI(t, d[t], s0, a, s1) for a in A for s0 in S) == _delta(t, s1))
    for t in xrange(H):
        for s in S:
            for a in A:
                m.addConstr(x[t, s, a] >= 0, 'x_%d_(%d,%d)__Constr' % (t, s, a))
    
    # Objective
    obj = LinExpr()
    for t in xrange(H):
        for s in S:
            for a in A:
                obj += R(t, s, a, d[t]) * x[t, s, a] 
    m.setObjective(obj, GRB.MAXIMIZE);
    #
    m.optimize()
    #
    _x = {}
    if m.status == GRB.Status.OPTIMAL:
        #
        m.write('%s%d.lp' % (lp_prefix, i))
        
        for t in xrange(H):
            for s in S:
                for a in A:
                    _x[t, s, a] = x[t, s, a].x
    else:
        print 'Errors while optimization'
        assert False
    return _x
            
if __name__ == '__main__':
    pass
    
