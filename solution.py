class Solution:

    solutions = {} 

    def __init__(self,data,state,accuracy=0):
        self.data = data
        self.accuracy = accuracy
        self.state = state
        self.solutions[self.str_sol(self.state)] = self 

    def get_accuracy(self,state):
        if (self.str_sol(state) in self.solutions):
            if (self.solutions[self.str_sol(state)].accuracy == 0) :
                self.solutions[self.str_sol(state)].set_accuracy(state)
        else :
            self.solutions[self.str_sol(state)] = Solution(self.data,state=state)
            self.solutions[self.str_sol(state)].set_accuracy(state)

        return self.solutions[self.str_sol(state)].accuracy

    def get_state(self):
        return self.state.copy()

    def set_accuracy(self,state):
        self.solutions[self.str_sol(state)].accuracy = self.data.evaluate(state)       
    
    def set_state(self,state):
        if (self.str_sol(state) in self.solutions): 
            self.solutions[self.str_sol(state)].state = state.copy()
        else :
            self.solutions[self.str_sol(state)] = Solution(self.data,state=state)

    def str_sol(self,mlist):
        result = ''
        for element in mlist:
            result += str(element)
        return result
