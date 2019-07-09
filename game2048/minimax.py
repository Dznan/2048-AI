import numpy as np
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
    def __init__(self, eval_func, max_depth=20, max_child=None):
        self.eval_func = eval_func
        self.max_depth = max_depth
        self.max_child = max_child
        self.NINF = -1e9
        self.INF = 1e9
    
    def choose_action(self, environment):
        child, _ = self.maximize(environment, self.NINF, self.INF, 0)
        return child
    
    def minimize(self, environment, alpha, beta, depth):
        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment)
                
        min_action, min_value = None, 1e9
        actions = environment.action_space

        if self.max_child is not None and len(actions) > self.max_child:
            # actions_value = []
            # for action in actions:
            #     child = environment.copy()
            #     child.step(action)
            #     actions_value.append((self.eval_func(child), action))
            # actions_value = sorted(actions_value, key=lambda x: x[0])
            # actions = []
            # for i in range(self.max_child):
            #     actions.append(actions_value[i][1])
            actions = select_actions(environment, actions, self.eval_func, self.max_child)

        for action in actions:
            child = environment.copy()
            child.step(action)
            _, value = self.maximize(child, alpha, beta, depth+1)
            if value < min_value:
                min_action, min_value = action, value
            if min_value <= alpha:
                break
            if min_value < beta:
                beta = min_value

        return min_action, min_value
    
    def maximize(self, environment, alpha, beta, depth):
        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment)
        
        max_action, max_value = None, -1e9
        actions = environment.action_space
        if self.max_child is not None and len(actions) > self.max_child:
            actions_value = []
            for action in actions:
                child = environment.copy()
                child.step(action)
                actions_value.append((self.eval_func(child), action))
            actions_value = sorted(actions_value, key=lambda x: x[0], reversed=True)
            actions = []
            for i in range(self.max_child):
                actions.append(actions_value[i][1])

        for action in actions:
            child = environment.copy()
            child.step(action)
            _, value = self.minimize(child, alpha, beta, depth+1)
            if value > max_value:
                max_action, max_value = action, value
            if max_value >= beta:
                break
            if max_value > alpha:
                alpha = max_value
            
        return max_action, max_value
