import numpy as np
from multiprocessing import Pool
from numba import jit


def select_actions(environment, actions, eval_func, num):
    # np.random.shuffle(actions)
    # return actions[:num]
    actions_value = []
    for action in actions:
        child = environment.copy()
        child.step(action)
        actions_value.append((eval_func(child), action))
    actions_value = sorted(actions_value, key=lambda x: x[0])
    actions = []
    for i in range(num):
        actions.append(actions_value[i][1])
    return actions


class MiniMaxPlayer:
    def __init__(self, eval_func, max_depth=20, max_child=None, random_select=True):
        self.eval_func = eval_func
        self.max_depth = max_depth
        self.max_child = max_child
        self.random_select = True
        self.NINF = -1e9
        self.INF = 1e9

        self.__count = 0
    
    def choose_action(self, environment):
        self.__count = 0
        child, _ = self.maximize(environment, self.NINF, self.INF, 0)
        # child, _ = self.parallel_maximize(environment, self.NINF, self.INF, 0)
        print('Searched {} nodes.'.format(self.__count))
        return child
    
    def minimize(self, environment, alpha, beta, depth):
        self.__count += 1
        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment)

        min_action, min_value = None, 1e9
        actions = environment.action_space
        succs = environment.successors

        if self.max_child is not None and len(succs) > self.max_child:
            if self.random_select:
                np.random.shuffle(succs)
                succs = succs[:self.max_child]
            else:
                eval_value = []
                for i, (child, action) in enumerate(succs):
                    eval_value.append((self.eval_func(child), i))
                eval_value = sorted(eval_value, key=lambda x: x[0])
                sub_succs = []
                for i in range(self.max_child):
                    idx = eval_value[i][1]
                    sub_succs.append(succs[idx])
                succs = sub_succs
        
        for child, action in succs:
            _, value = self.maximize(child, alpha, beta, depth+1)
            if value < min_value:
                min_action, min_value = action, value
            if min_value <= alpha:
                break
            if min_value < beta:
                beta = min_value

        return min_action, min_value
    
    def maximize(self, environment, alpha, beta, depth):
        self.__count += 1

        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment)
        
        max_action, max_value = None, -1e9
        succs = environment.successors

        for child, action in succs:
            _, value = self.minimize(child, alpha, beta, depth+1)
            if value > max_value:
                max_action, max_value = action, value
            if max_value >= beta:
                break
            if max_value > alpha:
                alpha = max_value
            
        return max_action, max_value
    
    def worker(self, params):
        child, action, alpha, beta, depth = params
        return action, self.minimize(child, alpha, beta, depth+1)
    
    def parallel_maximize(self, environment, alpha, beta, depth):
        self.__count += 1

        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment)
        
        max_action, max_value = None, -1e9
        succs = environment.successors
        
        p = Pool(processes=4)
        results = p.map(self.worker, [(child, action, self.NINF, self.INF, depth) for child, action in succs])
        
        for action, value in results:
            if value[-1] > max_value:
                max_action, max_value = action, value[-1]
            
        return max_action, max_value
