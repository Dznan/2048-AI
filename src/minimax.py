class MiniMaxPlayer:
    def __init__(self, eval_func, max_depth=20):
        self.eval_func = eval_func
        self.max_depth = max_depth
    
    def choose_action(self, environment):
        child, _ = self.maximize(environment, 0)
        return child
    
    def minimize(self, environment, depth):
        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment.state)

        min_child, min_value = None, 1e9
        for child in environment.successors:
            _, value = self.maximize(child, depth+1)
            if value < min_value:
                min_child, min_value = child, value
        
        return min_child, min_value
    
    def maximize(self, environment, depth):
        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment.state)
        
        max_child, max_value = None, -1e9
        for child in environment.successors:
            _, value = self.minimize(child, depth+1)
            if value > max_value:
                max_child, max_value = child, value
        
        return max_child, max_value
