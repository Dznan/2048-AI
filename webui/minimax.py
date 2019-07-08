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

        min_action, min_value = None, 1e9
        actions = environment.action_space
        environment.render()
        print(environment.turn, actions)
        for action in actions:
            child = environment.copy()
            child.step(action)
            _, value = self.maximize(child, depth+1)
            if value < min_value:
                min_action, min_value = action, value
        
        return min_action, min_value
    
    def maximize(self, environment, depth):
        if depth >= self.max_depth or environment.is_terminal():
            return None, self.eval_func(environment.state)
        
        max_action, max_value = None, -1e9
        actions = environment.action_space
        environment.render()
        print(environment.turn, actions)
        for action in actions:
            child = environment.copy()
            child.step(action)
            _, value = self.minimize(child, depth+1)
            if value > max_value:
                max_action, max_value = action, value
        
        return max_action, max_value
