class MiniMaxPlayer:
    def __init__(self, eval_func, max_depth=20):
        self.eval_func = eval_func
        self.max_depth = max_depth
        self.NINF = -1e9
        self.INF = 1e9
    
    def choose_action(self, environment):
        child, _ = self.maximize(environment, self.NINF, self.INF, 0)
        return child
    
    def minimize(self, environment, alpha, beta, depth):
        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment.state)

        min_action, min_value = None, 1e9
        actions = environment.action_space
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
            return None, self.eval_func(environment.state)
        
        max_action, max_value = None, -1e9
        actions = environment.action_space
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
