import numpy as np


class MiniMaxPlayer:
    def __init__(self, eval_func, max_depth=20, max_child=None, prune_mini_step=False, prune_max_step=False):
        self.eval_func = eval_func
        self.max_depth = max_depth
        self.max_child = max_child
        self.prune_mini_step = prune_mini_step
        self.prune_max_step = prune_max_step
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

        if self.prune_mini_step:
            for action in actions:
                child = environment.copy()
                child.step(action)
                value = self.eval_func(child)

                if value < min_value:
                    min_action, min_value = action, value
        else:  
            if self.max_child is not None and len(actions) > self.max_child:
                np.random.shuffle(actions)
                actions = actions[:self.max_child]

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
        if self.prune_max_step:
            for action in actions:
                child = environment.copy()
                child.step(action)
                value = self.eval_func(child)

                if value > max_value:
                    max_action, max_value = action, value
        else:
            if self.max_child is not None and len(actions) > self.max_child:
                np.random.shuffle(actions)
                actions = actions[:self.max_child]

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
